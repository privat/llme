"""Tools: the @tool registry and the built-in tools (shell, file editing, images)."""

import inspect
import json
import logging
import os
import re
import subprocess

from termcolor import cprint

from .errors import AppError, QuitEvent
from .terminal import ChunkPrinter, Spinner

logger = logging.getLogger('llme')
# The dict of all registered tools
all_tools = {}

# Conversion between python and json-schema types
type_map = {int: "integer", str: "string"}


class Tool:
    """A tool usable by the LLM. Create them wit the `@tool` decorator"""
    def __init__(self, fun, has_parts=False):
        self.name = fun.__name__
        self.fun = fun
        self.doc = fun.__doc__
        self.has_parts = has_parts # Might return an array  of content parts
        all_tools[self.name] = self
        self.build_schema()

    def build_schema(self):
        """Build the schema of the tool used to communicate with the LLM"""
        signature = inspect.signature(self.fun)
        self.signature = signature
        logger.info("Tool: %s%s", self.name, signature)
        params = {}
        reqs = []
        for n, p in signature.parameters.items():
            res = {}
            params[n] = res
            if p.annotation != inspect._empty:
                res["type"] = type_map[p.annotation]
            if p.default == inspect._empty:
                reqs.append(n)
            else:
                res["default"] = p.default

        self.schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.doc,
                "parameters": {
                    "type": "object",
                    "properties": params,
                    "required": reqs,
                }
            }
        }

def tool(fun, **kwargs):
    """ Tool decorator. This registers a function to be usable by the LLM."""
    tool = Tool(fun, **kwargs)
    return fun

class ToolError(Exception):
    """Exception raised by tools intended to the assistant.
    Other exceptions raised by tools are send-back to the user.
    You can wrap an existing exception e for the assistant with:

        raise ToolError() from e
    """
    pass

class Asset:
    "A loaded file"
    def __init__(self, path):
        self.path = path
        try:
            with open(path, 'rb') as f:
                self.raw_content = f.read()
        except OSError as e:
                raise AppError(f"Can't load file {path}: {e}")
        if len(self.raw_content) == 0:
            logger.info("Empty file %s", path)
            self.mime_type = "inode/x-empty"
            return
        import magic
        self.mime_type = magic.from_buffer(self.raw_content, mime=True)
        logger.info("File %s is %s", path, self.mime_type)

    def is_image(self):
        return self.mime_type.startswith("image/")

    def content_part(self):
        """Return the content part for the user message"""
        import base64
        if self.is_image():
            data = base64.b64encode(self.raw_content).decode()
            url = f"data:{self.mime_type};base64,{data}"
            return {"type": "image_url", "image_url": {"url": url}}
        else:
            data = base64.b64encode(self.raw_content).decode()
            return {"type": "file", "file": {"file_data": data, "filename": self.path}}

def list_tools():
    for name in all_tools:
        tool = all_tools[name]
        lines = tool.doc.splitlines()
        print(f"{name}{tool.signature} {lines[0]}")
        for line in lines[1:]:
            print(f"  {line}")

class ToolsMixin:
    """LLME mixin: built-in tools (run_command, file editing, assets)."""
    def cat_write(self, file, stdin):
        if not os.path.exists(file):
            return

        import difflib
        with open(file, "r") as f:
            old = f.readlines()
        new = stdin.splitlines(keepends=True)
        for line in difflib.unified_diff(old, new, file, file):
            if line[0] == '+':
                color = "green"
            elif line[0] == '-':
                color = "red"
            else:
                color = "white"
            cprint(line.rstrip("\n"), color=color)


    def run_command(self, command: str, stdin: str = ""):
        """Execute a standard shell command and return its result.
        If needed, the input content can be provided.
        To run python code, use `python` as command and the code in `stdin`.
        To write file use `cat > "filepath"` as command and the content in `stdin`.
        To patch a file, use `patch "originalfile"` as command and the unified diff in `stdin`.
        To fetch a website use `w3m -dump "https://example.com/foo.html"` as command and no stdin.
        To fetch a page use `curl -L "https://example.com/foo.html"` as command and no stdin.
        Etc.
        """

        command = command.strip()
        if command == "":
            command = "sh" # assume shell

        import shlex
        try:
            cmd = shlex.split(command, posix=True)
        except ValueError:
            # no closing quotation. Let subprocess handle and returns the error
            cmd = None

        # special known commands
        need_confirm = True
        if not cmd:
            pass
        elif len(cmd) <= 2 and cmd[0] in ["cat", "ls", "pwd", "echo"]:
            need_confirm = False
        elif len(cmd) == 3 and cmd[0] == "cat" and cmd[1] == ">":
            self.cat_write(cmd[2], stdin)

        default = ""
        if self.message_index is not None:
            need_confirm = True # Always confirm when replaying a specific message
            message = self.history[self.message_index]
            if message.role() == "user":
                default = message.content()

        if need_confirm:
            prompt = f"{self.prompt_prefix()} RUN {command.splitlines()[0]}"
            if not self.confirm(prompt, default=default):
                return None

        if self.config.box:
            cmd = shlex.split(self.config.box, posix=True)
            cmd.append(command)
        else:
            cmd = ["bash", "-c", command]

        if self.config.timeout_tool:
            cmd = ["timeout", "--verbose", str(self.config.timeout_tool)] + cmd

        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="backslashreplace", # Avoid encoding errors in the output
            bufsize=1,  # line-buffered
            env=env,
        )
        logger.debug("Starting sub-process %s", command)

        # send data to stdin
        # FIXME: avoid deadlock...
        # It's weird there isn't a lib or something to do this properly...
        proc.stdin.write(stdin)
        proc.stdin.close()

        content = ''
        cp = ChunkPrinter()
        with Spinner("light_yellow", self.config.plain) as am:
            while line := proc.stdout.readline():
                am.stop()
                cp.print(line, 'white', 'on_grey')
                content += line
        cp.end()
        proc.wait()

        command_name = command.splitlines()[0]
        if len(command_name) > 60:
            command_name = command_name[:60] + "..."

        result = f"command: {command_name}\nexitcode: {proc.returncode}\n"

        lencontent = len(content)
        if self.config.max_tool_len and lencontent > self.config.max_tool_len:
            import tempfile
            temp = self.new_tempfile("command_output-")
            self.write_file(temp, content)
            lines = len(content.splitlines())
            warning = f"warning: truncated because excessive length ({lines} lines or {lencontent} bytes; max is {self.config.max_tool_len} bytes). Full content is stored at {temp}. Extract useful content with grep, sed, head, etc."
            result += warning +  "\n"
            content = content[:self.config.max_tool_len]
            cprint(warning, "light_red")

        if proc.returncode != 0:
            cprint(f"EXIT {proc.returncode}", "light_red")

        result += f"stdout:\n{content}\n"

        return result

    def direct_run_command(self, command, input="", check=True):
        """Because of possible (sand)boxing, access to the agent environment must be indirect"""
        if self.config.box:
            import shlex
            cmd = shlex.split(self.config.box, posix=True)
            cmd.append(command)
        else:
            cmd = ["bash", "-c", command]
        logger.debug("Direct run %s", cmd)
        result = subprocess.run(cmd, input=input, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if check:
            result.check_returncode()
        return result.stdout

    def new_tempfile(self, prefix="", suffix=""):
        """Create an empty tempfile for the agent"""
        if not prefix:
            prefix = "llme-temp-"
        import shlex
        pattern = shlex.quote(prefix + "XXXXXX" + suffix)
        temp = self.direct_run_command(f"mktemp --tmpdir -- {pattern}").decode().strip()
        logger.info("Created tempfile %r", temp)
        return temp

    def read_file(self, path):
        """Read a file for the agent"""
        import shlex
        path = shlex.quote(path)
        return self.direct_run_command(f"cat {path}")

    def write_file(self, path, contents):
        """Write a file for the agent"""
        import shlex
        path = shlex.quote(path)
        if contents.__class__ == str:
            contents = contents.encode()
        self.direct_run_command(f"cat > {path}", contents)

    def update_file(self, path: str, regexp: str, new_content: str):
        """Update the content of a file.

        `regexp` matches the exact part to replace.
        `new_content` is the new block of text, used verbatim.

        Python re syntax is used with the flag re.MULTILINE (so ^ and $ match the begin and the end of a line)

        `regexp` must match exactly once in the original file or an error is thrown.
        The use of anti-greed operator `?` helps to select small parts.

        example:

        * `update_file("README.md","^# Introduction$(.|\n)*?^# Usage$", "# Introduction\n\nlorem ipsum...\n\n# Usage")`
        """

        data = self.read_file(path)

        regexp = re.compile(regexp.encode(), re.MULTILINE)
        matches = list(regexp.finditer(data))
        if len(matches) == 0:
            raise Exception("regexp not matched")
        if len(matches) > 1:
            spans = ', '.join([str(m.span()) for m in matches])
            raise Exception(f"multiple matches; found {len(matches)} spans {spans}")
        new_data = regexp.sub(new_content.encode(), data)
        deletions=matches[0].group()[:-1].count(b'\n')+1
        insertions=new_content[:-1].count('\n')+1
        self.write_file(path, new_data)
        message = f"{insertions} insertions(+), {deletions} deletions(-)"
        cprint(message, color="yellow")
        return [message]

    def image_description(self, path: str):
        """Returns a description of the given image. Useful for OCR, general description or any meaningful information."""
        # FIXME: work with sandbox
        if not os.path.exists(path):
            return f"Error: path {path} not found"
        file = Asset(path)
        if not file.is_image():
            return f"Error: {path} is not an image but {file.mime_type}"
        content_part = file.content_part()
        if not content_part:
            return f"Error: cannot access content of {path}"
        return [content_part]


    def run_tool(self, tool_call):
        """Run a tool and return the result as a message"""
        function = tool_call["function"]
        tool = all_tools.get(function["name"])
        if not tool:
            cprint(f"Unknown tool {function['name']}", color="red")
            message = {"role": "tool", "content": f"Error: unknown tool {function['name']}. Available tools: {', '.join(all_tools)}", "tool_call_id": tool_call["id"]}
            return message
        try:
            args = json.loads(function["arguments"])
        except json.JSONDecodeError as e:
            logger.debug("Tool arguments error: %r", e)
            cprint(f"{self.prompt_prefix()}: Bad tool arguments for {function['name']}: {e}", color="red")
            message = {"role": "tool", "content": f"Error: bad tool arguments {function['name']}. {e}", "tool_call_id": tool_call["id"]}
            return message
        logger.info(f"CALL %s(%s)", tool.name, args)
        try:
            result = tool.fun(**args)
        except KeyboardInterrupt:
            raise
        except QuitEvent:
            raise
        except Exception as e: # Just catch anything else
            logger.debug("Tool error: %r", e)
            if e.__cause__:
                e = e.__cause__
            cprint(f"Error during {function['name']}: {e}", color="red")
            message = {"role": "tool", "content": f"Error during {function['name']}: {e}", "tool_call_id": tool_call["id"]}
            self.add_message(message)
            return message
        if result is None:
            return None

        if not tool.has_parts:
            result = str(result)
        message = {"role": "tool", "content": result, "tool_call_id": tool_call["id"]}
        return message

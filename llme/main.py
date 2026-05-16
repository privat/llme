#!/usr/bin/env python3

# Copyright (C) 2025 Jean Privat, based from the work of Dory
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""A command-line assistant for local LLMs"""

import argparse
import argcomplete
import inspect
import itertools
import json
import logging
import os
import re
import subprocess
import sys
import threading
import time
import tomllib

from . import skills

import prompt_toolkit
import requests
from termcolor import colored, cprint
try:
    from termcolor import can_colorize # Exported since v3.2.0
except ImportError:
    from termcolor.termcolor import _can_do_colour as can_colorize # Was private before v3.2.0

# The global logger of the module
logger = logging.getLogger('llme')


class LLME:
    """The God class of the application."""

    def __init__(self, config):
        self.config = config
        self.model = config.model
        self.prompts = config.prompts # Initial prompts to process
        self.raw_messages = [] # the sequence of messages really communicated with the LLM server to work-around their various API limitations
        self.history = [] # A parallel history of messages with generations information
        self.full_history = [] # The full history with forks (append only!)
        self.generations = [] # the messages causing new generations (forks). They are the non-first children of messages
        self.roots = [] # The first system messages (roots without parent)
        self.current_generation = 0 # The generation number of the current conversation (for prompt prefix)
        self.message_index = None # The current message in the history (for /undo and history navigation)
        self.files = [] # Attached file for the next request.
        self.answering_model = None
        self.chat_output_file = None

        self.slash_commands = [
            "/file FILE    attach a file for the next prompt",
            "/models       list available models",
            "/tools        list available tools",
            "/metrics      list current metrics",
            "/compact      summarize the history and restart fresh",
            "/history      list condensed conversation history",
            "/full-history list hierarchical conversation history (with forks)",
            "/redo         cancel and regenerate the last assistant message",
            "/undo         cancel the last user message (and the response) [PageUp]",
            "/pass         go forward in history (cancel /undo) [PageDown]",
            "/edit         run EDITOR on the chat (save,editor,load)",
            "/save FILE    save chat",
            "/load FILE    load chat",
            "/clear        clear the conversation history",
            "/goto M       jump at message M (e.g `/goto 5c` or just `/5c`",
            "/config       list configuration options",
            "/set OPT=VAL  change a config option",
            "/quit         exit the program",
            "/skills       list available skills",
            "/help         show this help",
        ]

        self.warmup = None
        if self.config.batch or not sys.stdin.isatty() or not sys.stdout.isatty():
            # prompt_toolkit is disabled in batch mode
            # and need a tty
            self.session = None
        else:
            kb = prompt_toolkit.key_binding.KeyBindings()
            kb.add("pageup")(self.on_pageup)
            kb.add("pagedown")(self.on_pagedown)
            # We invert the default prompt_toolkit key bindings on multilines
            kb.add("enter")(self.on_enter)
            # shift-enter is not a TTY standard and requires specific terminal
            # alt-enter send the same TTY sequence as escape+enter. use it for now
            kb.add("escape","enter")(self.on_alt_enter)
            kb.add("c-c")(self.on_control_c)
            history = prompt_toolkit.history.FileHistory(config.history_filename)
            self.session = prompt_toolkit.PromptSession(
                    complete_while_typing=True,
                    key_bindings=kb,
                    completer=SlashCompleter(self),
                    complete_style=prompt_toolkit.shortcuts.CompleteStyle.MULTI_COLUMN,
                    history=history,
                    multiline=True,
            )
        self.failsafe = False # when True, its mean we are failing. this variable helps to prevent a loop of failure on the catch-all error handling

        self.api_headers = {} # additional headers for the server
        if self.config.api_key:
            self.api_headers["Authorization"] = f"Bearer {self.config.api_key}"

        self.metrics = Metrics()


    def cancel_prompt(self, app):
        """Cancel the current prompt and go back to the main loop"""
        app.erase_when_done = True
        app.exit(exception=CancelEvent())

    def on_pageup(self, event):
        """Keybinding for /undo"""
        if not self.rollback():
            return
        self.cancel_prompt(event.app)

    def on_pagedown(self, event):
        """Keybinding for /pass"""
        if not self.rollforward():
            return
        self.cancel_prompt(event.app)

    def on_enter(self, event):
        """Keybinding for validate"""
        event.current_buffer.validate_and_handle()

    def on_alt_enter(self, event):
        """Keybinding for newline"""
        event.current_buffer.insert_text('\n')

    def on_control_c(self, event):
        """Clear or leave"""
        if event.current_buffer.text == "":
            event.app.exit(exception=KeyboardInterrupt)
        else:
            event.app.current_buffer.reset()

    def build_message_object(self, message):
        """Add a message to the history"""

        n = len(self.history)
        append = True
        meta = message.get("llme-meta")
        if meta is not None:
            if parent_id := meta.get("parent"):
                parent = self.get_message_by_id(parent_id)
                if parent is None:
                    logger.error("Parent message not found: %s", parent_id)
                else:
                    gen = parent.generation
                    sibling = parent.children
                    if n > 0 and parent != self.history[n-1]:
                        append = False
        if n > 0:
            parent = self.history[n-1]
            gen = parent.generation
            sibling = parent.children
        else:
            parent = None
            gen = 0
            sibling = self.roots

        if sibling:
            for s in sibling:
                if s.data == message:
                    # Already known, reuse it
                    if append:
                        self.history.append(s)
                        self.current_generation = s.generation
                    return s
            # Need a new generation number
            self.generations.append(message)
            gen = len(self.generations)

        message_obj = Message(message, parent, n, gen)
        self.full_history.append(message_obj)
        sibling.append(message_obj)
        if self.config.chat_output:
            if self.chat_output_file is None:
                self.chat_output_file = open(self.config.chat_output, "w")
            self.chat_output_file.write(json.dumps(message) + "\n")
            self.chat_output_file.flush()
        if append:
            self.history.append(message_obj)
            self.current_generation = gen
        return message_obj

    def add_message(self, message):
        """
        Append a new message.
        Add it as is in message but transform it in raw_messages.
        """

        self.fork_if_required()

        logger.debug("Add %s message: %s", message['role'], message)
        result = self.build_message_object(message)
        if self.history[-1] != result:
            return result

        raw_message = json.loads(json.dumps(message))
        if "llme-meta" in raw_message:
            del raw_message["llme-meta"]
        if "channel" in raw_message:
            del raw_message["channel"] # Groq adds it but refuse it. Weird
        self.filter_file(raw_message)

        if raw_message["role"] == "tool" and self.config.tool_mode != "native":
            raw_message["role"] = "user"

        self.raw_messages.append(raw_message)
        return result

    def filter_file(self, message):
        """Filter that handle how file are transmitted.
        See --file-mode"""
        if not isinstance(message.get("content"), list):
            return
        if self.config.file_mode == "part":
            return

        text_content = []
        # unpack file content parts
        for part in message["content"]:
            if part["type"] == "text":
                text_content.append(part["text"])
            elif part["type"] == "image_url":
                # sorry, images need parts
                return
            elif part["type"] != "file":
                logger.warning("unknown content part type %s", part["type"])
                return
            elif self.config.file_mode == "json":
                # serialize the part as is
                text_content.append(json.dumps(part['file']))
            elif self.config.file_mode == "path":
                # replace the part with the path.
                path = part['file']['filename']
                if self.config.sandbox:
                    dirname = os.path.dirname(path)
                    filename = os.path.basename(path)
                    basename, extension = os.path.splitext(filename)
                    tempname = self.new_tempfile(basename + "_", extension)
                    b64 = part['file']['file_data']
                    import base64
                    data = base64.b64decode(b64)
                    self.write_file(tempname, data)
                    path = tempname
                text_content.append(f"The path of the file is {path}. You can cat its content.")
            else:
                logger.warning("unknown file_mode %s", self.config.file_mode)
                return

        message["content"] = "\n\n".join(text_content)

    def fork_if_required(self):
        """Fork the conversation to a new generation, if required.
        This will reset the conversation history"""
        if self.message_index is None:
            return
        # Here we need to reset the current conversation to fork it
        # And replace the "message_index" wit a new one
        if self.message_index > 0:
            self.reset_to_history(self.history[self.message_index-1])
        else:
            self.reset_messages([])
        logger.debug(f"Fork performed. New history: %s", self.history)


    def get_models(self):
        """List the available models"""
        if self.config.dummy:
            return ['dummy']
        url = f"{self.config.base_url}/models"
        logger.info("Get models from %s", url)
        try:
            response = requests.get(url, headers=self.api_headers, timeout=self.config.timeout_http)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Error getting models: %s", extract_requests_error(e))
            return None
        models = response.json()
        ids = [m["id"] for m in models["data"]]
        for m in models["data"]:
            # llama.cpp give a status field
            m["state"] = m.get("status", {}).get("value")
        logger.info("Available models: %s", ids)
        return models["data"]


    def prompt_prefix(self):
        """Return the prefix number to use in the prompt"""
        res = str(len(self.history))
        if self.message_index is not None:
            res = f"{self.message_index}/{res}"
        return res

    def confirm(self, question, default=""):
        """Ask a yes/no confirmation to the user"""
        if self.config.yolo and self.message_index is None:
            cprint(f"{question}: YOLO!", color="light_yellow")
            return True
        if self.config.batch:
            raise AppError("Confirmation unavailable in batch mode")
        try:
            if self.session:
                x = self.session.prompt([("#ff0000", f"{question}? ")], placeholder=[("#7f7f7f", "Enter to confirm, or give a prompt to cancel")], default=default, rprompt="")
            else:
                x = input(colored(f"{question}? ", "light_yellow"))
            self.failsafe = False # user input still alive
            if x == "":
                return True
            self.prompts.insert(0, x)
            return False
        except KeyboardInterrupt:
            raise QuitEvent("Confirmation interrupted")

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

        if self.config.sandbox:
            cmd = shlex.split(self.config.sandbox, posix=True)
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
        """Because of possible sandboxing, access to the agent environment must be indirect"""
        if self.config.sandbox:
            import shlex
            cmd = shlex.split(self.config.sandbox, posix=True)
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

    def write_file(self, path, contents):
        """Write a file for the agent"""
        import shlex
        path = shlex.quote(path)
        if contents.__class__ == str:
            contents = contents.encode()
        self.direct_run_command(f"cat > {path}", contents)

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


    def next_asset(self):
        """Get the next asset from the user. or None"""
        if len(self.prompts) == 0:
            return None

        # peek a the next "prompt" to see if it's a file
        user_input = self.prompts[0]
        if not os.path.exists(user_input):
            return None

        # it's a file, so remove it from prompts and add it to files
        self.prompts.pop(0)
        file = Asset(user_input)
        # Test to handle input redirection from /dev/null
        if len(file.raw_content) > 0:
            return file
        return None


    def input_prompt(self):
        """Return a prompt from stdim"""
        try:
            if self.warmup:
                self.warmup.start()
            if self.message_index is not None:
                default = self.history[self.message_index].content()
            else:
                default = ""
            prompt = f"{self.prompt_prefix()}> "
            if self.session:
                rprompt = []
                if self.files:
                    for f in self.files:
                        if rprompt:
                            rprompt.append(("", " "))
                        s = ("bg:grey", os.path.basename(f.path))
                        rprompt.append(s)

                user_input = self.session.prompt([("#00ff00", prompt)], default=default, placeholder=[("#7f7f7f", "A prompt, /h for help, Ctrl-C to interrupt. Alt-Enter for multi-line")], rprompt=rprompt)
            else:
                user_input = input(colored(prompt, "light_green"))
            self.failsafe = False
            if self.warmup:
                self.warmup.stop()
                # No more needed. We are on our own
                self.warmup = None
            return user_input
        except KeyboardInterrupt:
            raise QuitEvent("interrupted")


    def next_input(self):
        """ Get the next prompt or slash command"""
        if len(self.prompts) > 0:
            user_input = self.prompts.pop(0)
            if not self.config.plain:
                print(colored(f"{self.prompt_prefix()}>", "light_green"), user_input)
        elif self.config.batch:
            raise QuitEvent("end of batch")
        else:
            user_input = self.input_prompt()
        return user_input

    def next_prompt(self):
        """Get the next prompt from the user.
        Returns None or a user message"""
        logger.debug("Get the next prompt. Prompts queue: %d", len(self.prompts))

        while file := self.next_asset():
            self.files.append(file)

        user_input = self.next_input()

        if user_input == '':
            return None
        if user_input[0] == '/':
            self.slash_command(user_input)
            return None

        while file := self.next_asset():
            self.files.append(file)

        content_parts = []
        for asset in self.files:
            content_part = asset.content_part()
            if content_part:
                content_parts.append(content_part)
        self.files = []
        if len(content_parts) > 0:
            content_parts.insert(0, {"type": "text", "text": user_input})
            return {"role": "user", "content": content_parts}
        else:
            return {"role": "user", "content": user_input}


    def post_chat_completion(self, tools=None):
        """Prepare and send the POST request.
        Returns a response"""
        url = f"{self.config.base_url}/chat/completions"
        data = {
            "model": self.model,
            "messages": self.raw_messages,
            "stream": not self.config.bulk,
            "stream_options": {"include_usage": True},
        }
        if self.config.tool_mode == "native":
            data_tools = []
            for n, tool in all_tools.items():
                if tools is not None and n not in tools:
                    continue
                data_tools.append(tool.schema)
            if tools:
                for n in tools:
                    if not n in all_tools:
                        logger.warning("Unknown tool %s", n)
            if data_tools:
                data["tools"] = data_tools

        if self.config.temperature is not None:
            data["temperature"] = self.config.temperature
        if(self.config.extra_body):
            data.update(self.config.extra_body)
        if self.config.raw_request_dump:
            with open(self.config.raw_request_dump, "w") as f:
                json.dump(data, f, indent=2)
        logger.debug("Sending %d raw messages to %s", len(self.raw_messages), url)
        return requests.post(
            url,
            json=data,
            headers=self.api_headers,
            stream=not self.config.bulk,
            timeout=self.config.timeout_http,
        )

    def receive_chat_completion_message(self, response):
        """Process the server response to extract and return the message.
        This function handle; stream mode, tools, thinking, metrics, etc."""

        if self.answering_model is None:
            self.answering_model = self.model

        start_time = time.perf_counter()
        message = {} # The whole message
        meta = {} # LLME specific metadata
        last_chunk = None
        first_token = True
        cp = ChunkPrinter()
        for data in SSEReader(response):
            processed = False
            choices = data.get("choices")
            if not choices:
                # assume an empty chunk. This avoids None tests below
                choices = [{"delta":{}}]
            elif len(choices) > 1:
                logger.warning("chunk: too much choices: %s", data)
            choice0 = choices[0]

            # A whole message is just a big delta! So reuse the whole code path
            delta = choice0.get('message')
            if not delta:
                delta = choice0['delta']

            # last_chunk is used for debugging, it's usually too much to print each chunk
            last_chunk = data
            self.completion_metrics["chunk_n"] += 1

            chunk_update(message, delta)

            # Some openai-api provider have a reasoning_content field, with various names
            # It's non-standard but helps to distinguish the reasoning content from the main content
            for label in ["reasoning_content", "reasoning"]:
                reasoning_content = delta.get(label)
                if reasoning_content:
                    break # We found one
            if reasoning_content:
                processed = True
                cp.print(reasoning_content, "light_magenta", id='reasoning_content')

            content = delta.get("content")
            if content:
                processed = True
                cp.print(content, id='content')

            tool_calls = delta.get("tool_calls")
            if tool_calls:
                processed = True
                for tool_call in tool_calls:
                    idx = tool_call.get("index")
                    f = tool_call["function"]
                    if "name" in f:
                        cp.print(f["name"], color="yellow", id=idx)
                    cp.print_escaped(f["arguments"], color="yellow", string_color="light_yellow", id=idx)

            finish_reason = choice0.get('finish_reason')
            if finish_reason:
                processed = True
                # About: finish_reason
                # We do nothing with it for the moment
                # Some servers give Null for continue and "" for the uneventful finish reason
                # Some other gives "" for continue and a non empty string for finish reason
                # So do not trust anybody and continue the connection until the server closes it
                logger.info("Chunk: finish reason: %s", finish_reason)

            timings = data.get("timings")
            if timings:
                processed = True
                self.completion_metrics.update(timings)

            usage = data.get("usage")
            if usage:
                processed = True
                self.completion_metrics.update(usage)

            model = data.get("model")
            if model and self.answering_model != model:
                logger.warning("Unexpected answering model: got %s instead of %s", model, self.model)
                self.answering_model = model

            if not processed:
                logger.info("Chunk: Unexpected content: %s", data)
                continue
            elif first_token:
                first_token_time = time.perf_counter()
                self.completion_metrics["first_token_ms"] = (first_token_time - start_time) * 1000.0
                first_token = False

            #FIXME: this is fragile and ugly.
            if self.config.tool_mode == "markdown" and message.get('content'):
                cb = re.search(r"^```run([^\n]*)\n(.*?)^```$", message['content'], re.DOTALL | re.MULTILINE)
                if not cb:
                    continue
                tool_calls = message.get("tool_calls")
                if tool_calls is None:
                    tool_calls = message['tool_calls'] = []
                arguments = {"command": cb[1], "stdin": cb[2]}
                tool_call = {
                    "id": f"toolcallid-{len(self.history)}-len(tool_calls)",
                    "type": "function",
                    "function": {"name": "run_command", "arguments": json.dumps(arguments)}}
                tool_calls.append(tool_call)
                # Force the LLM to stop once a tool call is found
                break

        cp.end()
        logger.debug("Chunk: Last one: %s", last_chunk)
        response.close()
        if self.config.raw_response_dump:
            with open(self.config.raw_response_dump, "w") as f:
                json.dump(message, f, indent=2)
        meta["model"] = self.model
        meta["answering_model"] = self.answering_model
        message["llme-meta"] = meta
        return message


    def chat_completion(self, tools=None):
        """Post messages and get a response from the LLM."""
        self.completion_metrics = {}
        start_time = time.perf_counter()
        self.completion_metrics["chunk_n"] = 0
        self.completion_metrics["message_n"] = 1 # only one

        with Spinner("light_blue", self.config.plain):
            response = self.post_chat_completion(tools)
            response.raise_for_status()

        response_time = time.perf_counter()
        self.completion_metrics["response_ms"] = (response_time - start_time) * 1000.0

        if not self.config.plain:
            cprint(f"{self.prompt_prefix()}< ", "light_blue", end='', flush=True)

        message = self.receive_chat_completion_message(response)
        message_time = time.perf_counter()
        self.completion_metrics["total_ms"] = (message_time - start_time) * 1000.0
        meta = message["llme-meta"]
        meta["metrics"] = self.update_metrics()
        return message


    def update_metrics(self):
        """Display metrics information, and update the global metrics information"""
        data = self.completion_metrics
        logger.info("metrics: %s", data)
        if not "first_token_ms" in data:
            data["first_token_ms"] = 0.0
        data["last_token_ms"] = data["total_ms"] - data["first_token_ms"] - data["response_ms"]
        self.metrics.update(data)

        cprint(self.metrics.infoline(data, self), "light_grey")

        if self.config.export_metrics:
            try:
                with open(self.config.export_metrics, "w") as file:
                    json.dump({"total": self.metrics.total, "history": self.metrics.history}, file, indent=2)
            except OSError as e:
                raise AppError(f"Can't save metrics to {self.config.export_metrics}") from e
        return data


    def do_user(self):
        """Add the user prompt to the conversation"""
        prompt = self.next_prompt()
        if prompt:
            self.add_message(prompt)
        return prompt

    def do_assistant(self, **kwargs):
        if self.config.dummy:
            content = "I'm assistant."
            print(colored(f"{self.prompt_prefix()}<", "light_blue"), content)
            self.add_message({"role": "assistant", "content": content})
            return
        """Add the assistant response to the conversation"""
        self.fork_if_required()
        message = self.chat_completion(**kwargs)
        if message:
            self.add_message(message)
        return message

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

    def do_tools(self, tool_calls):
        """Run all the tools in the list, and add results to the conversation"""
        if not tool_calls:
            return
        for tool_call in tool_calls:
            message = self.run_tool(tool_call)
            if message:
                self.add_message(message)
            else:
                # The user cancelled the tool execution. Let they answer instead of the tool
                self.do_user()

    def do_role(self, oneround=False, tools=None):
        """Process the next role (user, assistant, tool...)"""
        if not self.history:
            self.do_user()
            return None

        if self.message_index:
            previous_message = self.history[self.message_index-1]
        else:
            previous_message = self.history[-1]
        previous_role = previous_message.role()
        if previous_role == "user" or previous_role == "tool":
            if self.token_budget and self.token_budget_start + self.token_budget <= self.metrics.predicted_n():
                self.add_message({"role": "user", "content": "final answer now. No more tools available. You have to conclude."})
                tools=[]
            self.do_assistant(tools=tools)
        elif previous_role == "system":
            self.do_user()
        elif previous_role == "assistant":
            tool_calls = previous_message.tool_calls()
            if not tool_calls and oneround:
                return previous_message
            if self.config.auto_compact and len(self.history) > self.config.auto_compact:
                cprint(f"{self.prompt_prefix()}> Auto-compaction", color="light_cyan")
                self.compact()
            elif tool_calls:
                self.do_tools(tool_calls)
            else:
                self.do_user()
        return None

    def do_sleep(self, delay):
        """Throttling server"""
        try:
            if self.config.plain:
                cprint(f"Throttled for {delay}s...", "light_cyan")
                time.sleep(delay)
                return
            with Spinner("light_cyan", self.config.plain):
                for i in range(delay, 0, -1):
                    cprint(f"  Throttled for {i}s... ", "light_cyan", end="")
                    time.sleep(1)
        except KeyboardInterrupt:
            logger.warning("Interrupted by user.")
            self.rollback()

    def get_throttling_delay(self, e):
        """Extract throttling delay from headers"""
        if e.response is None:
            return
        for h in ['retry-after', 'x-ratelimit-reset-requests', 'x-ratelimit-reset-tokens']:
            v = e.response.headers.get(h)
            if not v:
                continue
            logger.debug("throttling header %s=%s", h, v)
            if v[-1] == 's':
                v = v[:-1]
            try:
                return int(v)
            except:
                pass
        if e.response.status_code == 429:
            # Default throttling
            return 60
        return None


    def loop(self, oneround=False, tools=None, token_budget=None):
        """The main ping-pong loop between the user and the assistant"""
        if token_budget is not None:
            self.token_budget_start = self.metrics.predicted_n()
            self.token_budget = token_budget
        while True:
            try:
                response = self.do_role(oneround, tools=tools)
                if response is not None:
                    return response.data
                continue
            except requests.exceptions.RequestException as e:
                logger.error("Server error: %s", extract_requests_error(e))
                delay = self.get_throttling_delay(e)
                if delay:
                    self.do_sleep(delay)
                    continue
                if self.config.batch:
                    raise
                if e.response is not None and e.response.status_code == 404:
                    models = self.get_models()
                    if self.model not in (m["id"] for m in models):
                        cprint(f"Info: current model ({self.model}) is not in the list. Check with /models, chose with /set model=...", "light_cyan")
                self.rollback()
            except CancelEvent:
                self.session.app.erase_when_done = False
                logger.debug("Cancelled")
                continue
            except KeyboardInterrupt:
                logger.warning("Interrupted by user.")
                self.rollback()
            except QuitEvent as e:
                logger.info("Quitting: %s", str(e))
                break
            except AppError as e:
                # We got wrapped error to show.
                if self.config.batch:
                    raise
                logger.error("%s", e)
            except Exception as e:
                # catch-all in interactive session
                # it's not supposed to happen
                # but, at least, it allows the user to recover its work.
                if self.config.batch or self.failsafe:
                    raise
                self.failsafe = True
                import traceback
                traceback.print_exc()
                logger.error("Unexpected and uncatched exception: %s\nllme might be now, proceed with caution.", e)
                self.rollback()
            if self.config.batch:
                break


    def prepare_system_prompt(self):
        """Build the system message"""
        system_prompt = self.config.system_prompt
        if self.config.tool_mode == "markdown":
            tool = all_tools["run_command"]
            system_prompt += f"""\n## Tool run_command\n\nRun shell commands with a fenced code block and a `run` label. Format:\n\n```run $command\n$stdin\n```\n\nExample 1, list files:\n\n```run ls\n```\n\nExample 2, read file.txt:\n\n```run cat file.txt\n```\n\nExample 3, write "Hello" to file.txt\n\n```run cat > file.txt\nHello\n```\n\nExample 4, run a python script:\n\n```run python\nprint('Hello World')\n```\n\n"""
            system_prompt += tool.doc

        self.skills = skills.discover_skills(self.config.skills_path)
        if self.skills:
            system_prompt += "\n" + skills.prompt_for_skills(self.skills)

        date = self.direct_run_command("date").decode().strip()
        pwd = self.direct_run_command("pwd").decode().strip()
        system_prompt += f"\n## Contextual information\n\ndate: {date}\npwd: {pwd}\n"

        return {"role": "system", "content": system_prompt.strip()}


    def start(self):
        """Start, work, and terminate"""
        tool(self.run_command)
        tool(self.image_description, has_parts=True)

        models = None
        if not self.model:
            models = self.get_models()
            for m in models:
                if m["state"] == "loaded":
                    self.model = m["id"]
                    logger.info("Chose first loaded model from server: {self.model}")
                    break
            if not self.model:
                self.model = models[0]["id"]
                logger.info("Chose first model from server: {self.model}")
        if self.config.list_models:
            self.list_models()
            return
        logger.info("Use model %s from %s", self.model, self.config.base_url)

        self.start_session()

        if self.config.chat_input:
            self.load_chat(self.config.chat_input)
        elif self.config.system_prompt:
            self.add_message(self.prepare_system_prompt())

        stdinfile = None
        if self.config.batch:
            if len(self.prompts) > 0:
                if not sys.stdin.isatty():
                    # There are prompts, so use stdin as data for the first prompt
                    import tempfile
                    stdinfile = tempfile.NamedTemporaryFile(mode='wb', delete=False)
                    with stdinfile as f:
                        f.write(sys.stdin.buffer.read())
                    self.prompts.insert(0, stdinfile.name)
            else:
                # No prompts, so use whole stdin as single prompt.
                self.prompts = [sys.stdin.read()]

        if len(self.prompts) == 0 and not self.config.dummy:
            if not models:
                self.get_models()
            self.warmup = Warmup(self)

        try:
            self.loop()
        finally:
            if stdinfile:
                os.unlink(stdinfile.name)

        if self.metrics.total:
            cprint(f"Total: {self.metrics.infoline(self.metrics.total, self)}", "light_grey")
        if self.config.session:
            cprint(f"Continue this session with --session {self.config.session}", "light_cyan")

    def start_session(self):
        if self.config.no_session:
            return
        session_root_directory = os.path.expanduser("~/.config/llme/sessions")
        import time
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        if self.config.session:
            if os.path.exists(self.config.session):
                session_directory = self.config.session
            else:
                session_directory = os.path.join(session_root_directory, self.config.session)
                if not os.path.exists(session_directory):
                    raise AppError(f"Session {self.config.session} not found (also tried {session_directory})")
            if not self.config.chat_input:
                chat_file = os.path.join(session_directory, "chat.jsonl")
                if os.path.exists(chat_file):
                    self.config.chat_input = chat_file
            logger.info("Resuming session in %s", session_directory)
        else:
            os.makedirs(session_root_directory, exist_ok=True)
            self.config.session = timestamp
            session_directory = os.path.join(session_root_directory, timestamp)
            os.makedirs(session_directory, exist_ok=False)
            logger.info("New session in %s", session_directory)
        if not self.config.chat_output:
            self.config.chat_output = os.path.join(session_directory, "chat.jsonl")
        if not self.config.export_metrics:
            self.config.export_metrics = os.path.join(session_directory, f"{timestamp}-metrics.json")
        if not self.config.raw_request_dump:
            self.config.raw_request_dump = os.path.join(session_directory, f"{timestamp}-request.json")
        if not self.config.raw_response_dump:
            self.config.raw_response_dump = os.path.join(session_directory, f"{timestamp}-response.json")
        conf_file = os.path.join(session_directory, f"{timestamp}-config.json")
        with open(conf_file, "w") as f:
            json.dump(vars(self.config), f, indent=2)
        logfile = os.path.join(session_directory, f"{timestamp}.log")
        filehandler = logging.FileHandler(logfile)
        filehandler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        filehandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(filehandler)

    def load_chat(self, file, format=None):
        logger.info("Loading conversation from %s", file)
        if not format:
            format = self.chat_file_format(file)
        try:
            with open(file, "r") as f:
                if format == "yaml":
                    import yaml
                    messages = yaml.safe_load(f)
                if format == "jsonl":
                    messages = []
                    for line in f:
                        line = line.strip()
                        if line:
                            messages.append(json.loads(line))
                else:
                    if format != "json":
                        logger.error("Unknown format %s. Default as json", format)
                    messages = json.load(f)
            self.reset_messages(messages)
        except OSError as e:
            raise AppError(f"Can't load chat from {file}") from e

    def get_message_by_id(self, message_id):
        """Get a message by its id"""
        for m in self.full_history:
            if m.id == message_id:
                return m
        return None

    def reset_messages(self, messages):
        self.message_index = None
        self.history.clear()
        self.raw_messages.clear()
        id_map = {}
        for message in messages:
            orig_id = message.get("id")
            if orig_id is not None:
                del message["id"]
                orig_parent = message.get("parent")
                if orig_parent:
                    del message["parent"]
                    dest_parent = id_map.get(orig_parent)
                    if not dest_parent:
                        logger.error("Parent %s not found for %s", orig_parent, orig_id)
                    else:
                        message["parent"] = dest_parent
            m = self.add_message(message)
            if orig_id is not None:
                id_map[orig_id] = m.id
        logger.info("Reset %d messages", len(self.history))

    def chat_file_format(self, file):
        """Return the format of a chat file"""
        if file.endswith(".yaml") or file.endswith(".yml"):
            return "yaml"
        elif file.endswith(".jsonl"):
            return "jsonl"
        else:
            if not file.endswith(".json"):
                logger.error("Unknown format extension for %s. Default to json", file)
            return "json"

    def save_chat(self, file, messages=None, format=None):
        if messages is None:
            messages = self.full_history
        if not format:
            format = self.chat_file_format(file)
        logger.info("Dumping %s messages to %s", len(messages), file)
        try:
            all_messages = [m.data for m in messages]
            with open(file, "w") as f:
                if format == "yaml":
                    import yaml
                    yaml.dump(all_messages, f, default_flow_style=False, default_style="", width=65536)
                elif format == "jsonl":
                    for m in all_messages:
                        json.dump(m, f)
                        f.write('\n')
                else:
                    if format != "json":
                        logger.error("Unknown format %s. Saved as json", format)
                    json.dump(all_messages, f, indent=2)
        except OSError as e:
            raise AppError(f"Can't save chat to {file}") from e

    def list_skills(self):
        """List skills"""
        skills.list_skills(self.skills)

    def list_models(self):
        "Print the list of models"
        print(f"Models of {self.config.base_url}:")
        models = self.get_models()
        models.sort(key = lambda x: x["id"])
        found = False
        for m in models:
            if m["id"] == self.model:
                sel = "-> "
                found = True
            else:
                sel = "   "
            status = m["state"]
            if status is None or status == "unloaded":
                status = ""
            else:
                status = f" ({status})"
            print(f"{sel}{m['id']}{status}")
        if self.model and models and not found:
            logger.warning("Selected model %s not listed", self.model)
        return models

    def print_message(self, i, message, before=""):
        role = message.role()
        if before:
            colors = {"system": "yellow", "user": "green", "assistant": "blue", "tool": "yellow"}
        else:
            colors = {"system": "light_yellow", "user": "light_green", "assistant": "light_blue", "tool": "light_yellow"}
        color = colors[role]
        content = message.content()
        tools = message.tool_calls()
        if tools:
            content += f"[tools: {', '.join(t['function']['name']+str(t['function']['arguments']) for t in tools)}]"
        content = re.sub(r"\s+", " ", content).strip()
        import shutil
        size = shutil.get_terminal_size()
        prefix = f"{i} {role}: "
        width = size.columns - len(prefix) - 5 - len(before)
        if len(content) > width:
            content = content[:width].rstrip() + "..."
        if before != "":
            content = colored(content, "light_grey")
        print(before + colored(prefix, color) + content)


    def list_history(self):
        "Print the history of messages"
        for i, message in enumerate(self.history):
            if self.message_index and i >= self.message_index:
                break
            self.print_message(i, message)

    def list_full_history(self):
        "Print the full history with nice indentation."
        siblings = self.roots
        for i, message in enumerate(self.history):
            if self.message_index and i >= self.message_index:
                break
            self.print_tree(siblings, "", message)
            self.print_message(message.prefix(), message)
            siblings = message.children # next siblings
        self.print_tree(siblings, "", True)

    def print_tree(self, messages, prefix="", special=None):
        if not messages:
            return
        if special:
            last = -1
        else:
            last = len(messages) - 1
        for i, child in enumerate(messages):
            if child == special:
                continue
            cid = child.prefix()
            self.print_message(cid, child, prefix + ("├─" if i != last else ""))
            self.print_tree(child.children, prefix + ("│ " if i != last else ""))

    def slash_command(self, user_input):
        "Execute a slash command"
        #FIXME too much hardcoded
        args = user_input.split(None, 1)
        cmd = args.pop(0)
        arg = args[0].strip() if args else None
        if cmd in "/help" or cmd in "/?":
            for h in self.slash_commands:
                print(h)
        elif cmd in "/file":
            import shlex
            args = shlex.split(arg)
            if not args:
                raise AppError("/file: Missing paths")
            for f in args:
                asset = Asset(f)
                self.files.append(asset)
        elif cmd in "/tools":
            list_tools()
        elif cmd in "/config":
            for k, v in vars(self.config).items():
                print(f"{k}: {repr(v)}")
        elif cmd in "/compact":
            self.compact()
        elif cmd in "/models":
            self.list_models()
        elif cmd in "/history":
            self.list_history()
        elif cmd in "/full-history":
            self.list_full_history()
        elif cmd in "/redo":
            if not self.rollback("assistant"):
                raise AppError("/redo: No assistant message to redo")
            self.list_history()
        elif cmd in "/undo":
            if not self.rollback():
                raise AppError("/undo: No user message to undo")
            self.list_history()
        elif cmd in "/pass":
            if not self.rollforward():
                raise AppError("/pass: Already at latest message")
            self.list_history()
        elif cmd in "/edit":
            self.edit()
        elif cmd in "/save":
            if not arg:
                raise AppError("/save: Missing filename")
            self.save_chat(arg)
        elif cmd in "/load":
            if not arg:
                raise AppError("/load: Missing filename")
            self.load_chat(arg)
        elif cmd in "/clear":
            self.reset_messages([self.prepare_system_prompt()])
        elif cmd in "/goto":
            if not arg:
                raise AppError("/goto: Missing message label")
            self.goto(arg)
        elif cmd in "/metrics":
            for k, v in self.metrics.total.items():
                print(f"{k}: {repr(v)}")
        elif cmd in "/set":
            if not arg:
                raise AppError("/set: Missing setting")
            args = arg.split('=', 1)
            if len(args) != 2:
                raise AppError("/set: Syntax error, expected name=value")
            else:
                self.set_config(*args)
        elif cmd in "/skills":
            self.list_skills()
        elif cmd in "/quit":
            raise QuitEvent("/quit")
        elif re.match(r"/\d+\w*", cmd):
            # goto shortuct
            self.goto(cmd[1:])
        else:
            raise AppError(f"{user_input}: Unknown slash command. Use /help for help.")

    def rollback(self, roles = ["user", "tool"]):
        "Move message_index to the previous message of role, return the message on success"
        candidate = None
        for i, message in enumerate(self.history):
            if self.message_index and i >= self.message_index:
                break
            if message.role() in roles:
                candidate = i
        if not candidate:
            return None
        self.message_index = candidate
        return self.history[candidate]

    def rollforward(self, roles = ["user", "tool"]):
        "Move message_index to the next message of role, return the message on success"
        if self.message_index is None:
            return None
        for i, message in enumerate(self.history[self.message_index+1:]):
            if message.role() in roles:
                self.message_index = i + self.message_index + 1
                return message
        self.message_index = None
        return True


    def edit(self):
        "Save the chat in a tmpfile, edit it, and load it back"
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix=".yaml", delete=True) as tmp:
            import shlex
            self.save_chat(tmp.name, self.history, format="yaml")
            editor = os.environ.get("EDITOR", "editor")
            try:
                cmd = shlex.split(editor) + [tmp.name]
            except ValueError as e:
                raise AppError("Invalid editor command %s" % editor) from e
            logger.info( "Running %s", cmd)
            try:
                subprocess.run(cmd, check=True)
            except Exception as e:
                raise AppError("/edit") from e
            self.load_chat(tmp.name)


    def reset_to_history(self, message):
        """Reset the conversation to after a message in the full history"""
        self.current_generation = message.generation
        messages = []
        while message:
            messages.insert(0, message.data)
            message = message.parent
        self.reset_messages(messages)

    def find_label_in_history(self, n):
        """Return a labeled message from the full history"""
        match = re.match(r"(\d+)\s*([a-z]*)", n)
        if not match:
            raise AppError(f"Invalid message label {n}")
        num = int(match.group(1))
        if not match.group(2):
            # no gen, look in the local history first
            if num < len(self.history):
                message = self.history[num]
                logger.debug("goto %d -> %r", num, message)
                return message
            gen = self.current_generation
        else:
            gen = unbase26ish(match.group(2))

        message = self.find_in_history(num, gen)
        logger.debug("goto %s -> %d %d -> %r", n, num, gen, message)
        return message

    def goto(self, n):
        """Jump after a message in the full history"""
        message = self.find_label_in_history(n)
        if not message:
            raise AppError(f"Message {n} not found")
        if message not in self.history:
            self.reset_to_history(message)
        self.message_index = message.number

    def find_in_history(self, num, gen, messages = None):
        """Search a message in the full history with its number and generation."""
        if messages is None:
            messages = self.roots
        for message in messages:
            if message.number == num and message.generation == gen:
                return message
            found = self.find_in_history(num, gen, message.children)
            if found:
                return found
        return None

    def compact(self):
        """Force the summarization of the conversation"""
        compaction_prompt = self.config.compaction_prompt
        message = {"role": "user", "content": compaction_prompt}
        self.add_message(message)

        # Temporally disable tools
        response = self.do_assistant(tools=[])
        if response["content"] == "":
            logger.error("Agent did not compact. Bad agent!")
            return
        system_prompt = self.prepare_system_prompt()
        system_prompt["content"] += "\n\n" + response["content"]
        self.reset_messages([system_prompt])

    def set_config(self, opt, val):
        "Dynamically change a config option"
        opt = opt.strip()
        val = val.strip()
        config = vars(self.config)
        opts = [ k for k in config  if k.startswith(opt)]
        if not opts:
            raise AppError(f"Unknown setting: {opt}")
        if len(opts) > 1:
            raise AppError(f"Ambiguous setting: {opt} could match {', '.join(opts)}")
        opt = opts[0]

        if opt == "verbose":
            val = int(val)
            set_verbose(val)
        elif opt == "model":
            self.model = val
        logger.info("set %s: %r", opt, val)
        # FIXME this is a bit of a hack
        setconf(self.argparser, self.config, opt, val)


class CancelEvent(Exception):
    """Raised when the prompt is cancelled."""
    pass

class QuitEvent(Exception):
    """Raised when the user wants to quit or there is nothing more to do."""
    pass


class ChunkPrinter:
    """Print chunks of text and gracefully handle scope change, newlines, and partial unicode"""

    def __init__(self):
        self.last = None
        self.id = None
        self.inside_string = False

    def print(self, s, color=None, on_color=None, id=None):
        """Print a colored text, no '\n', forced flush.
        If id is set, then a different id will force a newline."""
        if not s:
            return
        if id != self.id:
            self.end()
            self.id = id
        cprint(s, color, on_color, end="", flush=True)
        self.last = s

    def print_escaped(self, s, color=None, string_color=None, on_color=None, id=None):
        """Assume that s contains strings with escaped content. We un-escape and change the color"""
        items = re.split(r"(\\[n\"\\]|\")", s)
        for i in items:
            if not i:
                continue
            elif i == "\"":
                self.inside_string = not self.inside_string
                self.print(i, color, on_color, id=id)
            elif i == "\\n":
                self.print("\n", color, on_color, id=id)
            else:
                if i[0] == "\\":
                    i = i[1:]
                c = string_color if self.inside_string else color
                self.print(i, c, on_color, id=id)

    def end(self):
        """Add possible final newline"""
        if self.last and self.last[-1] != '\n':
            print("")
            self.last = None
        self.inside_string = False


class Spinner:
    """A simple context manager for a spinner animation.
    It gives the user a feedback on long computation or network request.

    :param color: color of the spinner with termcolor nomenclature.
    :param disabled: if True, Spinner do nothing. The default is `not sys.stdout.isatty()`. Use False to force the spin.
    :param sequence: string of characters to animate.
    :param speed: animation speed in Hz.

    Usage:
        with Spinner("blue"):
            do_something()
    """
    def __init__(self, color="white", disabled=None, sequence="⠋⠙⠹⠽⠼⠴⠦⠧⠇⠏", speed=10):
        self.color = color
        if disabled is None:
            disabled = not sys.stdout.isatty()
        self.disabled = disabled
        self.sequence = sequence
        self.speed = speed
        self.stop_event = None
        self.animation_thread = None

    def _animate(self):
        """Animation loop, run in a thread."""
        for c in itertools.cycle(self.sequence):
            if self.stop_event.is_set():
                break
            sys.stdout.write(f"\r{colored(c, self.color)} ")
            sys.stdout.flush()
            time.sleep(1/self.speed)
        sys.stdout.write('\r')
        sys.stdout.flush()

    def stop(self):
        """Manually stop the spin."""
        if self.disabled:
            return
        if not self.stop_event.is_set():
            self.stop_event.set()
            self.animation_thread.join()

    def __enter__(self):
        if not self.disabled:
            self.stop_event = threading.Event()
            self.animation_thread = threading.Thread(target=self._animate)
            self.animation_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stop()


def base26ish(n):
    """Convert an integer to a base26ish string. Used to name generations.
    0 is 'a', 25 is 'z', 26 is 'aa', 27 is 'ab', etc.
    In genuine base26, 26 should be 'ba' since a stands for 0 and b for 1.
    """
    result = ""
    while n >= 0:
        result = chr(ord('a') + (n % 26)) + result
        n //= 26
        n -= 1
    return result

def unbase26ish(s):
    """Convert a base26ish string to an integer. Inverse of base26ish()."""
    result = 0
    for c in s:
        result = result * 26 + (ord(c) - ord('a')) + 1
    return result - 1

class Message:
    """A message in the conversation full history. This class is used to track message generations and children."""
    def __init__(self, data, parent, n, gen):
        self.data = data # The raw json data for the openai API
        self.parent = parent # The parent message in the conversation tree
        self.number = n # The message number in the conversation
        self.generation = gen # The generation number of the message
        self.id = f"{self.number}{base26ish(self.generation)}" # The unique id of the message
        self.children = [] # The children messages of this message
        meta = data.get("llme-meta")
        if meta is None:
            meta = {}
            self.data["llme-meta"] = meta
        meta["id"] = self.id
        if parent:
            meta["parent"] = parent.id

    def role(self):
        return self.data["role"]

    def content(self):
        """The text content of a message"""
        content = self.data["content"]
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        for c in content:
            if c["type"] == "text":
                return c["text"]

    def tool_calls(self):
        return self.data.get("tool_calls")

    def prefix(self):
        """Return the prefix for the message"""
        return self.id

    def __repr__(self):
        return self.prefix()

def deep_update(orig, delta):
    """Deep update (only dicts, other are replaced)"""
    for k, v in delta.items():
        if isinstance(v, dict) and isinstance(orig.get(k), dict):
            deep_update(orig[k], v)
        else:
            orig[k] = v
    return orig

CHUNK_FIXED_FIELDS = ["role", "model", "channel"]

def chunk_update(orig, delta, path=""):
    """Deep update for chunks in streamed messages. This only appends information and should never changes it.
    This is global chunk merging approach. I hove weird open-api providers will not be too much insane."""
    import copy
    delta = copy.deepcopy(delta)
    for k, v in delta.items():
        ov = orig.get(k)
        if isinstance(v, dict) and isinstance(ov, dict):
            chunk_update(ov, v, f"{path}.{k}")
        elif (isinstance(v, str) and isinstance(ov, str)
              # Do not concatenate str values in some root elements as some provider (groq and ollama at least) repeat values in those keys
              and not (path == "" and k in CHUNK_FIXED_FIELDS)):
            orig[k] += v
        elif isinstance(v, list) and isinstance(ov, list):
            for item in v:
                # Special case, extension of an existing element in an array
                if isinstance(item, dict):
                    idx = item.get("index")
                    if idx is not None:
                        if idx < len(ov):
                            chunk_update(ov[idx], item, f"{path}[{idx}]")
                            continue
                        while len(ov) < idx:
                            logger.warning("Broken server? Chunked array needs empty slots (%r)[%s] = %r", ov, idx, item)
                            ov.append({})
                        ov.append(item)
                        continue
                # Otherwise, just append
                ov.append(item)
        else:
            if ov is not None and v != ov:
                logger.error("Broken server? Chunk update issue %s.%s override %r by %r", path, k, ov, v);
            orig[k] = v
    return orig

def add_in_dict(total, delta):
    """Deep increase of all values in total"""
    for key, value in delta.items():
        if key in total:
            if isinstance(value, dict):
                add_in_dict(total[key], value)
            elif isinstance(value, int) or isinstance(value, float):
                total[key] += value
            else:
                logger.warning("Metrics: unmanaged type for key %s: %r", key, value)
        else:
            total[key] = value


class Metrics:
    """Help accounting various metrics"""
    def __init__(self):
        self.total = {}
        self.history = []

    def predicted_n(self):
        return self.total.get("predicted_n", 0)

    def update(self, d):
        """Add all"""
        self.history.append(d)
        add_in_dict(self.total, d)

    def infoline(self, d, llme=None):
        """Write a concise infoline"""
        info = []
        if llme and llme.token_budget:
            used = self.predicted_n() - llme.token_budget_start
            if total != 0:
                info.append(f"budget:%dt/%dt %.0f%%" % (used, llme.token_budget, used*100/llme.token_budget))
        if "cache_n" in d:
            info.append(f"cache:%dt prompt:%dt %.2ft/s predicted:%dt %.2ft/s" % (
                d["cache_n"],
                d["prompt_n"],
                1000.0 * d["prompt_n"] / d["prompt_ms"],
                d["predicted_n"],
                1000.0 * d["predicted_n"] / d["predicted_ms"],
            ))
        elif "prompt_tokens" in d:
            info.append(f"prompt:%dt predicted:%dt" % (
                d["prompt_tokens"],
                d["completion_tokens"],
            ))
        info.append(f"resp:%.2fs + 1st:%.2fs + last:%.2fs = %.2fs" % (
            d["response_ms"] / 1000.0,
            d["first_token_ms"] / 1000.0,
            d["last_token_ms"] / 1000.0,
            d["total_ms"] / 1000.0,
        ))
        return " ".join(info)


class SSEReader:
    """Utility class to read the Server-Sent Events (SSE) used in stream mode"""
    def __init__(self, response):
        self.iter_lines = response.iter_lines()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            line = next(self.iter_lines)
            if not line:
                continue
            if line[0] == 0x7b: # '{'
                # special case of no streaming
                data = json.loads(line.decode())
                return data
            # Handle classic SSE
            data = line.split(b':', 1)
            if len(data) != 2:
                logger.warning(f"Chunk: Unexpected: %s", line)
                continue
            event, data = data
            if event != b'data':
                logger.warning(f"Chunk: Unexpected event type: %s", line)
                continue
            if data in [b'[DONE]', b' [DONE]']:
                # We continue the connection until the server closes it. We do not trust it.
                continue
            try:
                data = json.loads(data.decode())
                return data
            except:
                logger.warning("Chunk: Got a weird one: %s", data)


class Warmup:
    """ A small empty chat request.
    It loads the model (if meeded) and checks that the server/model is ok.  Run in background while the user is typing its first prompt."""

    def __init__(self, llm):
        """The thread is started a soon as possible.
        But no signal is sent before start"""
        self.llm = llm
        self.thread = threading.Thread(target=self._process)
        self.thread.daemon = True
        self.message = None
        self.lock = threading.Lock()
        self.started = False
        self.stopped = False
        self.thread.start()


    def start(self):
        """Stop the program if the warmup failed.
        Or start the watch."""
        with self.lock:
            if self.message is not None:
                logger.error(self.message)
                sys.exit(1)
            self.started = True
        return


    def stop(self):
        """Stop caring about the warmup now.
        There is no clean way in Python to stop the running process or its requests. So just let ignore it and let it die."""
        with self.lock:
            self.stopped = True


    def _process(self):
        """ Thread,function.
        It justs wait for the completion of a small request.
        If everything is fine then the thread will just terminate.Otherwise it will signal am event for the main thread.
        Note: because of requests limitation there is no real way to cancel the request. This is mildly annoying.
        Maybe use httpx.AsyncClient or something else"""

        url = f"{self.llm.config.base_url}/chat/completions"
        json = {
            "model": self.llm.model,
            "messages": self.llm.raw_messages, # use the raw message with system prompt for warmup
            "max_completion_tokens":1,
            "max_tokens":1,
            "temperature":0,
            "stream": True,
        }
        logger.info("warmup %s", url)
        try:
            with requests.post(url=url, headers=self.llm.api_headers, json=json, stream=True) as response:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # store, signal or ignore
            with self.lock:
                logger.info("warmup: raise %s", e)
                if self.stopped: # ignore
                    return

                self.message = extract_requests_error(e)
                if not self.started: # stored
                    return

                # signal
                logger.error("%s", self.message)
                # sys.stdin.clode() don't cancel readline
                # sys.exit(1) don't stop the process
                # both approaches are not that much thread-safe
                # The remaining route is to send a signal that will interrupt the main thread
                import signal
                os.kill(os.getpid(), signal.SIGQUIT)
                return
        logger.info("warmup: completed")


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

class AppError(Exception):
    """Application error to give feedback to the user."""
    def __str__(self):
        if self.__cause__:
            return f"{super().__str__()}: {self.__cause__}"
        else:
            return super().__str__()

class SlashCompleter(prompt_toolkit.completion.Completer):
    """A completer for slash commands.
    For some reasons, the provided completers do not like 'words' with / at the beginning"""
    def __init__(self, llme):
        self.llme = llme # Strongly coupled, I allow it
        self.nesting = {}
        for command in self.llme.slash_commands:
            words = command.split()
            command = words[0][1:]
            if words[1] == "FILE":
                self.nesting[command] = prompt_toolkit.completion.PathCompleter(expanduser=True)
            else:
                self.nesting[command] = None
        notsettable = ["config", "plugins", "version", "dump_config", "list_tools", "list_models", "prompts"]
        settings = {x + "=" for x in vars(self.llme.config) if x not in notsettable}
        self.nesting["set"] = settings

        self.completer = prompt_toolkit.completion.NestedCompleter.from_nested_dict(self.nesting)

    def get_completions(self, document, complete_event):
        if not document.text.startswith("/"):
            return
        new_document = prompt_toolkit.document.Document(text=document.text[1:], cursor_position=len(document.text)-1)
        yield from self.completer.get_completions(new_document, complete_event)


def extract_requests_error(e):
    """Common handling of requests error"""
    logger.debug("requests error: %s", e)
    if e.request is None:
        return str(e)
    if e.response is None:
        return f"{e} ({e.request.url})"
    logger.debug("response headers: %s", e.response.headers)

    """Server may format their error in plain text or json"""
    text = e.response.text
    if text and text[0] == '{':
        logger.debug("full error response: %s", text)
        try:
            data = json.loads(text)
        except:
            data = {}
        if "error" in data:
            data = data["error"]
            text = data
        if "message" in data:
            text = data["message"]

    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 200:
        text = text[:200] + "..."

    message = f"{text.strip()} ({e.response.status_code} {e.response.request.url})"
    return message


def apply_config(parser, args, config, path):
    """Apply a config dict to an args namespace without overwriting existing values (precedence).
    The method is a little ugly but it works... """
    #TODO check types
    variables = vars(args)
    for k in variables:
        if variables[k] is None and k in config:
            setconf(parser, args, k, config[k])
    for k in config:
        if k not in variables:
            logger.warning("%s: Unknown config key %s", path, k)

def apply_env(parser, args):
    """Apply environment variables to an args namespace without overwriting existing values (precedence)."""
    variables = vars(args)
    for k in variables:
        var = f"LLME_{k.upper()}"
        env = os.environ.get(var)
        if variables[k] is None and env:
            # TODO type conversion
            setconf(parser, args, k, env)
    for k in os.environ:
        m = re.match(r'LLME_(.*)', k)
        if m and m[1].lower() not in variables:
            logger.warning("Unknown environment variable %s", k)

config_dirs = [
    os.path.expanduser("~/.config/llme"),
    os.path.dirname(os.path.abspath(__file__)),
]

def load_config_file(path):
    """Load a TOML config file."""

    # Load simple names in config directories
    if not os.path.exists(path) and not '/' in path:
        for directory in config_dirs:
            trypath = os.path.join(directory, path + ".toml")
            if os.path.exists(trypath):
                path = trypath
                break

    logger.debug("Loading config from %s", path)
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except OSError as e:
        raise AppError(f"Can't load config file {path}") from e
    except tomllib.TOMLDecodeError as e:
        raise AppError(f"Invalid config file {path}") from e

def resolve_config(parser, args):
    """Compute config in order of precedence"""
    # 1. args have the highest precedence

    # 2. then explcit --config files in reverse order (last wins)
    if args.config:
        for path in reversed(args.config):
            config = load_config_file(path)
            apply_config(parser, args, config, path)

    # 3. Then environment variables
    apply_env(parser, args)

    # 4. The default config files: user, then system
    for directory in config_dirs:
        path = os.path.join(directory, "config.toml")
        if os.path.exists(path):
            config = load_config_file(path)
            apply_config(parser, args, config, path)

    # 5. ultimate defaults where argparse default value is None
    if args.tool_mode is None:
        args.tool_mode = "native"
    if args.file_mode is None:
        args.file_mode = "path"
    if args.batch is None and not sys.stdin.isatty():
        logger.debug("no tty: activate batch mode")
        args.batch = True
    if args.skills_path is None:
        args.skills_path = []
    if not args.no_skills:
        for i in config_dirs + ["."]:
            d = os.path.join(i,"skills")
            if os.path.isdir(d):
                args.skills_path.append(d)
    if args.timeout_tool is None:
        args.timeout_tool = 600 # 10 min
    if args.timeout_http is None:
        args.timeout_http = 600
    if args.max_tool_len is None:
        args.max_tool_len = 100000


    logger.debug("Final config: %s", {k:v for k,v in vars(args).items() if v is not None})

def str2bool(s):
    "Convert a boolean value from a string in a config file or env var"
    if isinstance(s, bool):
       return s
    s = s.lower()
    if s in ('yes', 'true', '1', 'y', 't'):
        return True
    if s in ('no', 'false', '0', 'n', 'f'):
        return False
    if s == "":
        return None
    raise ValueError(f"Invalid boolean value: {s}")

def search_action(parser, name):
    "Return the first action according its dest name"
    for action in parser._actions:
        if action.dest and action.dest == name:
            return action
    return None

def setconf(parser, args, name, value):
    "Update a setting according to its type"
    action = search_action(parser, name)
    if not action:
        raise AppError(f"Unknown setting {name}")
    if action.type == bool or isinstance(action, argparse._StoreTrueAction):
        # Special case for bool, as the action just store True
        value = str2bool(value)
        setattr(args, action.dest, value)
        return
    elif action.type:
        value = action.type(value)
    action(parser, args, value)


def load_module(path):
    """Just load a random python file. I'm not sure why its so complex"""
    import importlib.machinery
    basename = os.path.basename(path)
    name, ext = os.path.splitext(basename)
    try:
        return importlib.machinery.SourceFileLoader(name, path).load_module()
    except OSError as e:
        raise AppError(f"Can't load plugin {path}") from e

def load_plugin(path):
    """Load a single python module, or all python modules of a directory."""
    if os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith(".py"):
                filepath = os.path.join(path, filename)
                load_module(filepath)
    else:
        load_module(path)

def list_tools():
    for name in all_tools:
        tool = all_tools[name]
        lines = tool.doc.splitlines()
        print(f"{name}{tool.signature} {lines[0]}")
        for line in lines[1:]:
            print(f"  {line}")

def show_version():
    """Print the version number.
    Note: version information with importlib.metadata is garbage as this mishandle both "dev" installation, and a possible concurrent old version. So we do it the old way with git and a _version file"""
    try:
        dirname = os.path.dirname(__file__)
        version = subprocess.check_output(["git", "-C", dirname, "describe", "--tags", "--dirty"], text=True, stderr=subprocess.DEVNULL).strip()
        print(f"llme development version: {version}")
    except subprocess.CalledProcessError:
        try:
            from . import _version
            print(f"llme version {_version.version}")
        except ImportError:
            print(f"llme standalone version")

def set_verbose(level):
    "Assign a global verbose level (in number of -v)"
    if level is None:
        level = 0
    consolehandler = logging.StreamHandler(sys.stderr)
    consolehandler.setFormatter(ColorFormatter())
    logger.addHandler(consolehandler)
    logging_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    logging_level = logging_levels[min(level, len(logging_levels) - 1)]
    logger.setLevel(logging_level)
    consolehandler.setLevel(logging_level)
    consolehandler.setFormatter(ColorFormatter())
    logger.info("Log level set to %s", logging.getLevelName(logger.level))

class ColorFormatter(logging.Formatter):
    """A simple colored formatter."""

    COLORS = [
        (logging.DEBUG, 'light_grey'),
        (logging.INFO, 'cyan'),
        (logging.WARNING, 'light_cyan'),
        (logging.ERROR, 'light_red'),
    ]

    def color(self, record):
        for level, color in self.COLORS:
            if record.levelno <= level:
                return color
        return 'white' # default color

    def format(self, record):
        return f"{colored(record.levelname, self.color(record))}: {record.getMessage()}"

class YAMLAction(argparse.Action):
    """Special action that takes, parse and deep-merge YAML-ish arguments"""
    def __call__(self, parser, namespace, values, option_string=None):
        import yaml
        orig = getattr(namespace, self.dest)
        if orig is None:
            orig = {}
            setattr(namespace, self.dest, orig)
        # QOL hack
        delta = yaml.safe_load(values)
        if type(delta) != dict:
            s = json.dumps(delta)
            raise ValueError(f"Expected JSON object, got {s}")
        deep_update(orig, delta)

def config_completer(prefix, **kwargs):
    """completer on --config for argcomplete"""
    file_completer = argcomplete.completers.FilesCompleter('*.toml')
    paths = []
    import glob
    for directory in config_dirs:
        for path in glob.glob(os.path.join(directory, f"{prefix}*.toml")):
            paths.append(os.path.basename(path)[:-5])
    return paths + file_completer(prefix, **kwargs)

def model_completer(prefix, parsed_args, parser, **kwargs):
    """completer on --model for argcomplete"""
    # Models list depend on the other options (config and url), so parse them before!
    resolve_config(parser, parsed_args)
    llme = LLME(parsed_args)
    llme.argparser = parser # FIXME too much hacky
    models = llme.get_models()
    if not models:
        return ()
    return (m["id"] for m in models if m["id"].startswith(prefix))

def process_args():
    """Handle command line arguments and envs."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options...] [prompts...]',
        description="OpenAI-compatible chat CLI.",
        epilog="Boolean flags can be negated with `--no-`. Example `--no-plain` to force colors in a non TTY",
    )
    # Trick: "store_true" options are defaulted to None, so we can distinguish between explicit --foo (True), --no-foo (False) and unset (None)
    parser.add_argument("-u", "--base-url", metavar="URL", help="API base URL [base_url]")
    parser.add_argument("-m", "--model", metavar="NAME", help="Model name or identifier [model]").completer = model_completer
    parser.add_argument(      "--list-models", action="store_true", default=None, help="List available models then exit")
    parser.add_argument(      "--api-key", metavar="SECRET", help="The API key [api_key]")
    parser.add_argument("-b", "--batch", action="store_true", default=None, help="Run non-interactively. Implicit if stdin is not a tty [batch]")
    parser.add_argument("-p", "--plain", action="store_true", default=None, help="No colors or tty fanciness. Implicit if stdout is not a tty [plain]")
    parser.add_argument(      "--bulk", action="store_true", default=None, help="Disable stream-mode. Not that useful but it helps debugging APIs [bulk]")
    parser.add_argument("-o", "--chat-output", metavar="FILE", help="Export the full conversation in json")
    parser.add_argument("-i", "--chat-input", metavar="FILE", help="Continue a previous (exported) conversation")
    parser.add_argument(      "--export-metrics", metavar="FILE", help="Export metrics, usage, etc. in json")
    parser.add_argument("-s", "--system", dest="system_prompt", help="System prompt [system_prompt]")
    parser.add_argument(      "--session", type=str, default=None, help="Resume a previous session")
    parser.add_argument(      "--no-session", action="store_true", default=None, help="Do not save the session")
    parser.add_argument(      "--auto-compact", type=int, help="Automatically compact when that much rounds is reached (0 for disabled) [auto_compact]")
    parser.add_argument(      "--temperature", type=float, help="Temperature of predictions [temperature]")
    parser.add_argument(      "--extra-body", metavar="YAML", action=YAMLAction, help="YAML/JSON element merged with requests (ex: `--extra-body 'top_p: 0.95'`) [extra_body]")
    parser.add_argument(      "--no-skills", action="store_true", default=None, help="Disable defaults skills (excepts those from --skills-path)")
    parser.add_argument(      "--skills-path", metavar="DIR", action="append", help="Add a skills directory for skill recursive search")
    parser.add_argument(      "--list-skills", action="store_true", default=None, help="List all discoverable agent skills then exit")
    parser.add_argument(      "--tool-mode", choices=["markdown", "native"], help="How tools and functions are given to the LLM [tool_mode]")
    parser.add_argument(      "--sandbox", type=str, help="The sandbox tool used to run commands [sandbox]")
    parser.add_argument(      "--max-tool-len", type=int, help="Maximum size of tool output in bytes (0 for unlimited) [max_tool_len]")
    parser.add_argument(      "--timeout-tool", type=int, help="Maximum duration in seconds of tool runs (0 for unlimited) [timeout_tool]")
    parser.add_argument(      "--timeout-http", type=int, help="Timeout of LLM connexion (0 for unlimited) [timeout_http]")
    parser.add_argument(      "--file-mode", choices=["part", "path","json"], help="How (non image) files are given to the LLM [file_mode]")
    parser.add_argument("-c", "--config", metavar="FILE", action="append", help="Custom configuration files").completer = config_completer
    parser.add_argument(      "--list-tools", action="store_true", default=None, help="List available tools then exit")
    parser.add_argument(      "--dump-config", action="store_true", default=None, help="Print the effective config and quit")
    parser.add_argument(      "--raw-request-dump", metavar="FILE", help="Export the full POSTed json payload [raw_request_dump]")
    parser.add_argument(      "--raw-response-dump", metavar="FILE", help="Export the full json message response [raw_response_dump]")
    parser.add_argument(      "--plugin", metavar="PATH", action="append", dest="plugins", help="Add additional tool (python file or directory) [plugins]")
    parser.add_argument("-H", "--history-filename", metavar="FILE", help="Read/write command history from FILE [history_filename]")
    parser.add_argument("-v", "--verbose", action="count", help="Increase verbosity level (can be used multiple times)")
    parser.add_argument(      "--log-file", metavar="FILE", help="Write logs to a file [log_file]")
    parser.add_argument("-Y", "--yolo", action="store_true", default=None, help="UNSAFE: Do not ask for confirmation before running tools. Combine with --batch to reach the singularity.")
    parser.add_argument(      "--version", action="store_true", default=None, help="Display version information and quit")
    parser.add_argument(      "--completion", action="store_true", default=None, help="Print shell completion script")
    parser.add_argument(      "--dummy", action="store_true", default=None, help=argparse.SUPPRESS) # Disable LLM for testing the UI alone
    parser.add_argument(      "--compaction-prompt", default=None, help=argparse.SUPPRESS)
    parser.add_argument("prompts", nargs='*', help="An initial list of prompts")
    # Trick: iterate on store_true options to add the --no- variants
    for action in parser._actions:
        if action.const is True:
            for name in action.option_strings:
                if name.startswith("--") and not name.startswith("--no-"):
                    x=parser.add_argument("--no" + name[1:], dest=action.dest, action="store_false", help=argparse.SUPPRESS)

    argcomplete.autocomplete(parser)

    args = parser.parse_intermixed_args()
    if args.version:
        show_version()
        sys.exit(0)

    # We need to that first because `can_colorize()` is cached.
    # So we need to "guess" the environment before printing anything, including logs
    args_plain = args.plain
    if args_plain is None:
        args_plain = not can_colorize()
    elif args_plain:
        # For termcolor and subprocesses
        os.environ["NO_COLOR"] = "True" # https://no-color.org/
    else:
        # For termcolor and subprocesses
        os.environ["FORCE_COLOR"] = "True" # https://force-color.org/

    set_verbose(args.verbose)
    logger.debug("Given arguments %s", {k:v for k,v in vars(args).items() if v is not None})

    args.plain = args_plain
    if args.log_file:
        try:
            filehandler = logging.FileHandler(args.log_file)
        except OSError as e:
            raise AppError(f"Can't open log file {args.log_file}") from e
        filehandler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        filehandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(filehandler)

    resolve_config(parser, args)

    if args.dump_config:
        json.dump(vars(args), sys.stdout, indent=2)
        sys.exit(0)

    if args.completion:
        print(argcomplete.shell_integration.shellcode(["llme"]))
        sys.exit(0)

    if args.list_skills:
        sks = skills.discover_skills(args.skills_path)
        skills.list_skills(sks)
        sys.exit(0)

    if args.plugins:
        for plugin in args.plugins:
            load_plugin(plugin)

    if not args.base_url:
        logger.error("Error: --base-url required and not defined the config file.")
        sys.exit(2)

    if args.history_filename is None:
        args.history_filename = os.path.expanduser("~/.config/llme/history")

    return parser, args


def main():
    """The main CLI entry point."""
    try:
        argparser, config = process_args()
        llme = LLME(config)
        llme.argparser = argparser # FIXME too much hacky
        if config.list_tools:
            list_tools()
            sys.exit(0)

        llme.start()
    except AppError as e:
        logger.error("%s", e)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        logger.error("Server error: %s", extract_requests_error(e))
        raise e


if __name__ == "__main__":
    sys.exit(main())

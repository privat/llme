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

import prompt_toolkit
import requests
from termcolor import colored, cprint

# The global logger of the module
logger = logging.getLogger(__name__)

class LLME:
    """The God class of the application."""

    def __init__(self, config):
        self.config = config
        self.model = config.model
        self.prompts = config.prompts # Initial prompts to process
        self.messages = [] # the sequence of messages with the LLM
        self.raw_messages = [] # the sequence of messages really communicated with the LLM server to work-around their various API limitations

        self.slash_commands = [
            "/models       list available models",
            "/tools        list available tools",
            "/metrics      list current metrics",
            "/retry        cancel and regenerate the last assistant message",
            "/undo         cancel the last user message (and the response)",
            "/edit         run EDITOR on the chat (save,editor,load)",
            "/save FILE    save chat",
            "/load FILE    load chat",
            "/config       list configuration options",
            "/set OPT=VAL  change a config option",
            "/quit         exit the program",
            "/help         show this help",
        ]

        self.warmup = None
        if self.config.batch:
            self.session = None
        else:
            self.session = prompt_toolkit.PromptSession(complete_while_typing=True)

        self.api_headers = {} # additional headers for the server
        if self.config.api_key:
            self.api_headers["Authorization"] = f"Bearer {self.config.api_key}"

        self.metrics = Metrics()

    def slash_completer(self):
        """Return a completer for slash commands"""
        words = [word.split()[0] for word in self.slash_commands]
        notsettable = ["config", "plugins", "version", "dump_config", "list_tools", "list_models", "prompts"]
        for c in vars(self.config):
            if c not in notsettable:
                words.append(f"/set {c}=")

        return prompt_toolkit.completion.WordCompleter(words, sentence=True)

    def add_message(self, message):
        """
        Append a new message.
        Add it as is in message but transform it in raw_messages.
        """

        logger.debug("Add %s message: %s", message['role'], message)
        self.messages.append(message)

        # Special filtering for some models/servers
        # TODO make it configurable and modular
        if isinstance(message["content"], list):
            text_content = []
            # unpack file content parts
            for part in message["content"]:
                if part["type"] == "text":
                    text_content.append(part["text"])
                if part["type"] == "file":
                    # replace the file content with its path.
                    text_content.append(f"The file is {part['file']['filename']}. You can cat its content.")
                if part["type"] == "image_url":
                    self.raw_messages.append(message)
            self.raw_messages.append({"role": message["role"], "content": "\n".join(text_content)})
            return

        self.raw_messages.append(message)

    def get_models(self):
        """List the available models"""
        url = f"{self.config.base_url}/models"
        logger.info("Get models from %s", url)
        try:
            response = requests.get(url, headers=self.api_headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(extract_requests_error(e))
            sys.exit(1)
        models = response.json()
        ids = [m["id"] for m in models["data"]]
        logger.info("Available models: %s", ids)
        return ids


    def confirm(self, question, color):
        """Ask a yes/no confirmation to the user"""
        if self.config.yolo:
            cprint(f"{question}: YOLO!", color)
            return True
        if self.config.batch:
            raise EOFError("No confirmation in batch mode") # ugly
        try:
            if self.session:
                x = prompt_toolkit.prompt([(color, f"{question} [Yn]? ")]).strip()
            else:
                x = input(f"{question} [Yn]? ").strip()
            if x in ['', 'y', 'Y']:
                return True
            if len(x) > 3:
                # the user is writing to much.
                # they may have missed this is a confirmation prompt.
                # but we are nice and store the message
                self.prompts.insert(0, x)
            return False
        except KeyboardInterrupt:
            raise EOFError("Confirmation interrupted") # ugly


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

        if not self.confirm(f"{len(self.messages)} RUN {command}", "#ff0000"):
            return None

        # hack for unbuffered python
        if command == "python":
            cmd = "python -u"
        else:
            cmd = command

        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # line-buffered
        )
        logger.debug("Starting sub-process %s", command)

        # send data to stdin
        # FIXME: avoid deadlock...
        # It's weird there isn't a lib or something to do this properly...
        proc.stdin.write(stdin)
        proc.stdin.close()

        content = ''
        with AnimationManager("light_red", self.config.plain) as am:
            while line := proc.stdout.readline():
                am.stop()
                print(line, end='', flush=True)
                content += line
        proc.wait()
        printn(content)

        if proc.returncode != 0:
            cprint(f"EXIT {proc.returncode}", "light_red")

        return f"command: {command}\nexitcode: {proc.returncode}\nstdout:\n{content}\n"


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
            if self.session:
                user_input = self.session.prompt([("#00ff00", "> ")], placeholder=[("#7f7f7f", "A prompt, /h for help, Ctrl-C to interrupt")])
            else:
                user_input = input()
            if self.warmup:
                self.warmup.stop()
                # No more needed. We are on our own
                self.warmup = None
            return user_input
        except KeyboardInterrupt:
            raise EOFError("interrupted") # ugly


    def next_input(self):
        """ Get the next prompt or slash command"""
        if len(self.prompts) > 0:
            user_input = self.prompts.pop(0)
            if not self.config.plain:
                print(colored(f"{len(self.messages)}>", "light_green"), user_input)
        elif self.config.batch:
            raise EOFError("end of batch") # ugly
        else:
            user_input = self.input_prompt()
        return user_input

    def next_prompt(self):
        """Get the next prompt from the user.
        Returns None or a user message"""
        logger.debug("Get the next prompt. Prompts queue: %d", len(self.prompts))

        files = [] # the list of files to send to the LLM for the next prompt
        while file := self.next_asset():
            files.append(file)

        while True:
            user_input = self.next_input()

            if user_input == '':
                return None
            if user_input[0] != '/':
                break
            try:
                self.slash_command(user_input)
            except EOFError as e:
                # was likely /quit
                raise e
            except Exception as e:
                # Allow the user to recover from errors
                logger.error("%s", e)

        while file := self.next_asset():
            files.append(file)

        content_parts = []
        for asset in files:
            content_part = asset.content_part()
            if content_part:
                content_parts.append(content_part)
        if len(content_parts) > 0:
            content_parts.insert(0, {"type": "text", "text": user_input})
            return {"role": "user", "content": content_parts}
        else:
            return {"role": "user", "content": user_input}


    def post_chat_completion(self):
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
            data["tools"] = [tool.schema for tool in all_tools.values()]
        if self.config.temperature is not None:
            data["temperature"] = self.config.temperature
        logger.debug("Sending %d raw messages to %s", len(self.raw_messages), url)
        return requests.post(
            url,
            json=data,
            headers=self.api_headers,
            stream=not self.config.bulk,
            timeout=600,  # high enough
        )


    def receive_chat_completion_message(self, response):
        """Process the server response to extract and return the message.
        This function handle; stream mode, tools, thinking, metrics, etc."""

        start_time = time.perf_counter()
        full_content = ''
        full_reasoning_content = ''
        full_tool_calls = []
        mode = None # reasoning, content or none
        message = None # The whole message, if any
        last_chunk = None
        first_token = True
        reasoning_label = None
        for data in SSEReader(response):
            processed = False
            choices = data.get("choices")
            if not choices:
                # assume an empty chunk. This avoids None tests below
                choices = [{"delta":{}}]
            elif len(choices) > 1:
                logger.warning("chunk: too much choices: %s", data)
            choice0 = choices[0]

            message = choice0.get('message')
            if message:
                # A whole message is just a big delta! So reuse the whole code path
                delta = message
            else:
                delta = choice0['delta']

            # last_chunk is used for debugging, it's usually too much to print each chunk
            last_chunk = data
            self.completion_metrics["chunk_n"] += 1

            # Some reasoning models like qwen3 of gpt-oss have a reasoning_content field, with various names
            # It's non-standard but helps to distinguish the reasoning content from the main content
            for label in ["reasoning_content", "reasoning"]:
                reasoning_content = delta.get(label)
                if reasoning_content:
                    reasoning_label = label
                    break # We found one
            if reasoning_content:
                processed = True
                if mode and mode != full_reasoning_content:
                    printn(mode)
                full_reasoning_content += reasoning_content
                mode = full_reasoning_content
                cprint(reasoning_content, "light_magenta", end='', flush=True)

            content = delta.get("content")
            if content:
                processed = True
                if mode and mode != full_content:
                    printn(mode)
                full_content += content
                mode = full_content
                print(content, end='', flush=True)

            tool_calls = delta.get("tool_calls")
            if tool_calls:
                processed = True
                i =- 1
                for tool_call in tool_calls:
                    i = i + 1
                    idx = tool_call.get("index", i)
                    f = tool_call["function"]
                    while len(full_tool_calls) <= idx:
                        full_tool_calls.append(None)
                    if "name" in f:
                        full_tool_calls[idx] = tool_call
                    else:
                        full_tool_calls[idx]["function"]["arguments"] += f["arguments"]

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

            if not processed:
                logger.info("Chunk: Unexpected content: %s", data)
                continue
            elif first_token:
                first_token_time = time.perf_counter()
                self.completion_metrics["first_token_ms"] = (first_token_time - start_time) * 1000.0
                first_token = False

            #FIXME: this is fragile and ugly.
            if self.config.tool_mode == "markdown":
                cb = re.search(r"^```run ([\w+-]*)\n(.*?)^```$", full_content, re.DOTALL | re.MULTILINE)
                if not cb:
                    continue
                arguments = {"command": cb[1], "stdin": cb[2]}
                tool_call = {
                    "id": f"toolcallid-{len(self.messages)}",
                    "type": "function",
                    "function": {"name": "run_command", "arguments": json.dumps(arguments)}}
                full_tool_calls.append(tool_call)
                # Force the LLM to stop once a tool call is found
                break

        if mode:
            printn(mode)
        logger.debug("Chunk: Last one: %s", last_chunk)
        response.close()

        if not message:
            # construct the message from the deltas
            message = {"role": "assistant", "content": full_content}
            if full_reasoning_content:
                message[reasoning_label] = full_reasoning_content
            if full_tool_calls:
                message["tool_calls"] = full_tool_calls
        return message


    def chat_completion(self):
        """Post messages and get a response from the LLM."""
        self.completion_metrics = {}
        start_time = time.perf_counter()
        self.completion_metrics["chunk_n"] = 0
        self.completion_metrics["message_n"] = 1 # only one

        with AnimationManager("light_blue", self.config.plain):
            response = self.post_chat_completion()
            response.raise_for_status()

        response_time = time.perf_counter()
        self.completion_metrics["response_ms"] = (response_time - start_time) * 1000.0

        if not self.config.plain:
            cprint(f"{len(self.messages)}< ", "light_blue", end='', flush=True)

        message = self.receive_chat_completion_message(response)
        message_time = time.perf_counter()
        self.completion_metrics["total_ms"] = (message_time - start_time) * 1000.0

        self.update_metrics()

        self.add_message(message)

        full_tool_calls = message.get("tool_calls")
        if full_tool_calls:
            for tool_call in full_tool_calls:
                function = tool_call["function"]
                tool = all_tools.get(function["name"])
                if not tool:
                    logger.error("Unknown tool %s", function["name"])
                    message = {"role": "tool", "content": f"Error: unknown tool {function["name"]}. Available tools: {", ".join(all_tools)}", "tool_call_id": tool_call["id"]}
                    self.add_message(message)
                    continue
                args = json.loads(function["arguments"])
                cprint(f"CALL {tool.name}({args})", "light_red")
                if tool.need_self:
                    args = {"self": self} | args
                result = tool.fun(**args)
                if result is None:
                    return None
                message = {"role": "tool", "content": str(result), "tool_call_id": tool_call["id"]}
                self.add_message(message)
            return True
        return None


    def update_metrics(self):
        """Display metrics information, and update the global metrics information"""
        data = self.completion_metrics
        logger.info("metrics: %s", data)
        data["last_token_ms"] = data["total_ms"] - data["first_token_ms"] - data["response_ms"]
        self.metrics.update(data)

        cprint(self.metrics.infoline(data), "light_grey")

        if self.config.export_metrics:
            with open(self.config.export_metrics, "w") as file:
                json.dump({"total": self.metrics.total, "history": self.metrics.history}, file, indent=2)


    def loop(self):
        """The main ping-pong loop between the user and the assistant"""
        while True:
            try:
                prompt = self.next_prompt()
                if prompt:
                    self.add_message(prompt)
                while self.chat_completion():
                    pass
            except requests.exceptions.RequestException as e:
                logger.error(extract_requests_error(e))
                sys.exit(1)
            except KeyboardInterrupt:
                logger.warning("Interrupted by user.")
                if self.config.batch:
                    break
            except EOFError as e:
                logger.info("Quiting: %s", str(e))
                break


    def prepare_system_prompt(self):
        """Build the system message"""
        system_prompt = self.config.system_prompt
        if self.config.tool_mode == "markdown":
            tool = all_tools["run_command"]
            system_prompt += f"""## Tool\n\nRun shell commands with a fenced code block and a `run` label. Format:\n\n```run command\nstdin\n```\n\nExemple:\n\n```run python\nprint('Hello World')\n```\n\n"""
            system_prompt += tool.doc

        return {"role": "system", "content": system_prompt}


    def start(self):
        """Start, work, and terminate"""

        models = None
        if not self.model:
            models = self.get_models()
            self.model = models[0]
        if self.config.list_models:
            self.list_models()
            return
        logger.info("Use model %s from %s", self.model, self.config.base_url)

        if self.config.chat_input:
            self.load_chat(self.config.chat_input)
        elif self.config.system_prompt:
            self.add_message(self.prepare_system_prompt())

        stdinfile = None
        if not sys.stdin.isatty():
            if len(self.prompts) > 0:
                # There is prompts, so use stdin as data for the first prompt
                import tempfile
                stdinfile = tempfile.NamedTemporaryFile(mode='wb', delete=False)
                with stdinfile as f:
                    f.write(sys.stdin.buffer.read())

                self.prompts.insert(0, stdinfile.name)
            else:
                # No prompts, so use stdin as prompt
                self.prompts = [sys.stdin.read()]

        if len(self.prompts) == 0:
            if not models:
                self.get_models()
            self.warmup = Warmup(self)

        try:
            self.loop()
        finally:
            if self.config.chat_output:
                self.save_chat(self.config.chat_output)
            if stdinfile:
                os.unlink(stdinfile.name)

        if self.metrics.total:
            cprint(f"Total: {self.metrics.infoline(self.metrics.total)}", "light_grey")

    def load_chat(self, file):
        logger.info("Loading conversation from %s", file)
        with open(file, "r") as f:
            self.reset_messages(json.load(f))

    def reset_messages(self, messages):
        self.messages.clear()
        self.raw_messages.clear()
        for message in messages:
            self.add_message(message)
        logger.info("Reset %d messages", len(self.messages))

    def save_chat(self, file):
        logger.info("Dumping conversation to %s", file)
        with open(file, "w") as f:
            json.dump(self.messages, f, indent=2)

    def list_models(self):
        "Print the list of models"
        print(f"Models of {self.config.base_url}:")
        models = self.get_models()
        for m in models:
            sel = "-> " if m == self.model else "   "
            print(f"{sel}{m}")
        return models

    def slash_command(self, user_input):
        "Execute a slash command"
        #FIXME too much hardcoded
        args = user_input.split(None, 1)
        cmd = args.pop(0)
        arg = args[0].strip() if args else None
        if cmd in "/tools":
            list_tools()
        elif cmd in "/config":
            for k, v in vars(self.config).items():
                print(f"{k}: {repr(v)}")
        elif cmd in "/models":
            self.list_models()
        elif cmd in "/retry":
            if not self.rollback("assistant"):
                logger.error("no assistant message to retry")
        elif cmd in "/undo":
            if not self.rollback("user"):
                logger.error("no user message to undo")
        elif cmd in "/edit":
            self.edit()
        elif cmd in "/save":
            self.save_chat(arg)
        elif cmd in "/load":
            self.load_chat(arg)
        elif cmd in "/metrics":
            for k, v in metrics.total.items():
                print(f"{k}: {repr(v)}")
        elif cmd in "/set":
            args = arg.split('=', 1)
            if len(args) != 2:
                print("set: syntax error")
            else:
                self.set_config(*args)
        elif cmd in "/quit":
            raise EOFError("/quit")
        elif cmd in "/help":
            for h in self.slash_commands:
                print(h)
        else:
            print(f"Unknown {user_input}. Use /help for help.")

    def rollback(self, role):
        "Erase the last message of role, return True on success"
        candidate = None
        for i, message in enumerate(self.messages):
            if message.get("role") == role:
                candidate = i
        if not candidate:
            return False
        self.reset_messages(self.messages[:candidate])
        return True

    def edit(self):
        "Save the chat in a tmpfile, edit it, and load it back"
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=True) as tmp:
            self.save_chat(tmp.name)
            editor = os.environ.get("EDITOR", "editor")
            subprocess.run([editor, tmp.name], check=True)
            self.load_chat(tmp.name)


    def set_config(self, opt, val):
        "Dynamically change a config option"
        opt = opt.strip()
        val = val.strip()
        config = vars(self.config)
        opts = [ k for k in config  if k.startswith(opt)]
        if not opts:
            raise KeyError(f"unknown option: {opt}")
        if len(opts) > 1:
            raise KeyError(f"ambiguous option: {opt} could match {", ".join(opts)}")
        opt = opts[0]

        if opt == "verbose":
            val = int(val)
            set_verbose(val)
        elif opt == "model":
            self.model = val
        logger.info("set %s: %r", opt, val)
        # TODO convert types. but don't duplicate argparse
        setattr(self.config, opt, val)


class AnimationManager:
    """A simple context manager for a spinner animation."""
    def __init__(self, color, plain=False):
        self.color = color
        self.plain = plain
        self.stop_event = None
        self.animation_thread = None

    def _animate(self):
        """Animation loop, run in a thread."""
        for c in itertools.cycle("⠋⠙⠹⠽⠼⠴⠦⠧⠇⠏"):
            if self.stop_event.is_set():
                break
            sys.stdout.write(f"\r{colored(c, self.color)} ")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r')
        sys.stdout.flush()

    def stop(self):
        """Manually stop the animation."""
        if self.plain:
            return
        if not self.stop_event.is_set():
            self.stop_event.set()
            self.animation_thread.join()

    def __enter__(self):
        if not self.plain:
            self.stop_event = threading.Event()
            self.animation_thread = threading.Thread(target=self._animate)
            self.animation_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stop()


class Metrics:
    """Help accounting various metrics"""
    def __init__(self):
        self.total = {}
        self.history = []

    def update(self, d):
        """Add all"""
        self.history.append(d)
        for key in d:
            value = d[key]
            if key in self.total:
                self.total[key] += value
            else:
                self.total[key] = value

    def infoline(self, d):
        """Write a concise infoline"""
        info = []
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
        Note: because of Python limitation there is no real way to cancel the request. This is mildly annoying."""

        url = f"{self.llm.config.base_url}/chat/completions"
        json = {
            "model": self.llm.model,
            "messages": [{"role":"user", "content":""}],
            "max_completion_tokens":1,
            "max_tokens":1,
            "temperature":0,
            "stream": True,
        }
        logger.info("warmup %s", url)
        try:
            # TODO maybe add a timeout? I'm not sure
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
    def __init__(self, fun):
        self.name = fun.__name__
        self.fun = fun
        self.doc = fun.__doc__
        self.need_self = False
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
            if n == "self":
                self.need_self = True
                continue
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

def tool(fun):
    """ Tool decorator. This registers a function to be usable by the LLM."""
    tool = Tool(fun)
    return fun

tool(getattr(LLME,"run_command"))


class Asset:
    "A loaded file"
    def __init__(self, path):
        self.path = path
        with open(path, 'rb') as f:
            self.raw_content = f.read()
        import magic
        self.mime_type = magic.from_buffer(self.raw_content, mime=True)
        logger.info("File %s is %s", path, self.mime_type)

    def content_part(self):
        """Return the content part for the user message"""
        import base64
        if self.mime_type.startswith("image/"):
            data = base64.b64encode(self.raw_content).decode()
            url = f"data:{self.mime_type};base64,{data}"
            return {"type": "image_url", "image_url": {"url": url}}
        else:
            data = base64.b64encode(self.raw_content).decode()
            return {"type": "file", "file": {"file_data": data, "filename": self.path}}


def extract_requests_error(e):
    """Common handling of requests error"""
    logger.debug("request error: %s", e)
    if e.request is None:
        return str(e)
    if e.response is None:
        return f"{e} ({e.request.url})"

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

    message = f"{text} ({e.response.status_code} {e.response.request.url})"
    return message


def printn(previous_string):
    """Print a newline if previous_string does not end with one"""
    if not previous_string.endswith("\n"):
        print()


def apply_config(args, config, path):
    """Apply a config dict to an args namespace without overwriting existing values (precedence).
    The method is a little ugly but it works... """
    #TODO check types
    variables = vars(args)
    for k in variables:
        if variables[k] is None and k in config:
            setattr(args, k, config[k])
    for k in config:
        if k not in variables:
            logger.warning("%s: Unknown config key %s", path, k)

def apply_env(args):
    """Apply environment variables to an args namespace without overwriting existing values (precedence)."""
    variables = vars(args)
    for k in variables:
        var = f"LLME_{k.upper()}"
        env = os.environ.get(var)
        if variables[k] is None and env:
            # TODO type conversion
            setattr(args, k, env)
    for k in os.environ:
        m = re.match(r'LLME_(.*)', k)
        if m and m[1].lower() not in variables:
            logger.warning("Unknown environment variable %s", k)

def load_config_file(path):
    """Load a TOML config file."""
    logger.debug("Loading config from %s", path)
    with open(path, "rb") as f:
        return tomllib.load(f)

def resolve_config(args):
    """Compute config in order of precedence"""
    # 1. args have the highest precedence

    # 2. then explcit --config files in reverse order (last wins)
    if args.config:
        for path in reversed(args.config):
            config = load_config_file(path)
            apply_config(args, config, path)

    # 3. Then environment variables
    apply_env(args)

    # 4. The default config files: user, then system
    config_dirs = [
        os.path.expanduser("~/.config/llme"),
        os.path.dirname(os.path.abspath(__file__)),
    ]
    for directory in config_dirs:
        path = os.path.join(directory, "config.toml")
        if os.path.exists(path):
            config = load_config_file(path)
            apply_config(args, config, path)

    # 5. ultimate defaults where argparse default value is None
    if args.tool_mode is None:
        args.tool_mode = "native"
    if args.batch is None and not sys.stdin.isatty():
        args.batch = True
    if args.plain is None and not sys.stdout.isatty():
        args.plain = True

    logger.debug("Final config: %s", vars(args))


def load_module(path):
    """Just load a random python file. I'm not sure why its so complex"""
    import importlib.machinery
    basename = os.path.basename(path)
    name, ext = os.path.splitext(basename)
    return importlib.machinery.SourceFileLoader(name, path).load_module()

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
    "Assign a global vesbose level (in number of -v)"
    logging_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    logger.setLevel(logging_levels[min(level, len(logging_levels) - 1)])
    logger.info("Log level set to %s", logging.getLevelName(logger.level))

def process_args():
    """Handle command line arguments and envs."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options...] [prompts...]',
        description="OpenAI-compatible chat CLI.",
    )
    parser.add_argument("-u", "--base-url", help="API base URL [base_url]")
    parser.add_argument("-m", "--model", help="Model name [model]")
    parser.add_argument("--list-models", action="store_true", help="List available models then exit")
    parser.add_argument("--api-key", help="The API key [api_key]")
    parser.add_argument("-b", "--batch", default=None, action="store_true", help="Run non-interactively. Implicit if stdin is not a tty [batch]")
    parser.add_argument("-p", "--plain", default=None, action="store_true", help="No colors or tty fanciness. Implicit if stdout is not a tty [plain]")
    parser.add_argument(      "--bulk", default=None, action="store_true", help="Disable stream-mode. Not that useful but it helps debugging APIs [bulk]")
    parser.add_argument("-o", "--chat-output", help="Export the full raw conversation in json")
    parser.add_argument("-i", "--chat-input", help="Continue a previous (exported) conversation")
    parser.add_argument(      "--export-metrics", help="Export metrics, usage, etc. in json")
    parser.add_argument("-s", "--system", dest="system_prompt", help="System prompt [system_prompt]")
    parser.add_argument(      "--temperature", default=None, type=float, help="Temperature of predictions [temperature]")
    parser.add_argument(      "--tool-mode", default=None, choices=["markdown", "native"], help="How tools and functions are given to the LLM [tool_mode]")

    parser.add_argument("-c", "--config", action="append", help="Custom configuration files")
    parser.add_argument(      "--list-tools", action="store_true", help="List available tools then exit")
    parser.add_argument(      "--dump-config", action="store_true", help="Print the effective config and quit")
    parser.add_argument(      "--plugin", action="append", dest="plugins", help="Add additional tool (python file or directory) [plugins]")
    parser.add_argument("-v", "--verbose", default=0, action="count", help="Increase verbosity level (can be used multiple times)")
    parser.add_argument("-Y", "--yolo", default=None, action="store_true", help="UNSAFE: Do not ask for confirmation before running tools. Combine with --batch to reach the singularity.")
    parser.add_argument(      "--version", action="store_true", help="Display version information and quit")
    parser.add_argument("prompts", nargs='*', help="An initial list of prompts")

    args = parser.parse_intermixed_args()
    if args.version:
        show_version()
        sys.exit(0)

    logging.basicConfig()
    set_verbose(args.verbose)
    logger.debug("Given arguments %s", vars(args))

    resolve_config(args)

    if args.dump_config:
        json.dump(vars(args), sys.stdout, indent=2)
        sys.exit(0)

    if args.plugins:
        for plugin in args.plugins:
            load_plugin(plugin)

    if args.list_tools:
        list_tools()
        sys.exit(0)

    if args.base_url is None:
        print("Error: --base-url required and not definied the config file.", file=sys.stderr)
        sys.exit(1)

    return args


def main():
    """The main CLI entry point."""
    config = process_args()
    llme = LLME(config)
    llme.start()


if __name__ == "__main__":
    sys.exit(main())

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
import json
import logging
import os
import subprocess
import sys

from . import skills

from .config import YAMLAction, config_completer, resolve_config
from .errors import AppError
from .history import HistoryMixin
from .logging import set_verbose
from .loop import LoopMixin
from .server import ServerMixin, Warmup, extract_requests_error
from .terminal import Spinner
from .tools import Asset, Tool, ToolsMixin, all_tools, list_tools, tool
from .ui import SlashCompleter, UIMixin

import prompt_toolkit
import requests
from termcolor import cprint
try:
    from termcolor import can_colorize # Exported since v3.2.0
except ImportError:
    from termcolor.termcolor import _can_do_colour as can_colorize # Was private before v3.2.0

# The global logger of the module
logger = logging.getLogger('llme')


class LLME(HistoryMixin, ServerMixin, ToolsMixin, UIMixin, LoopMixin):
    """The LLME application object. It wires the mixins together;
    each mixin implements one concern (see its module)."""

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
        self.token_budget = None
        self.dummy_responses_queue = None # Canned responses for --dummy-responses (lazily loaded)
        self.dummy_responses_index = 0 # Next canned response to return

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


    def start(self):
        """Start, work, and terminate"""
        models = None
        if not self.model:
            models = self.get_models()
            for m in models:
                if m["state"] == "loaded":
                    self.model = m["id"]
                    logger.info("Chose first loaded model from server: %s", self.model)
                    break
            if not self.model:
                self.model = models[0]["id"]
                logger.info("Chose first model from server: %s", self.model)
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

        if len(self.prompts) == 0 and not self.config.dummy and not self.config.dummy_responses:
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
            # token_budget is guaranteed non-zero by the condition above
            used = self.predicted_n() - llme.token_budget_start
            info.append(f"budget:%dt/%dt %.0f%%" % (used, llme.token_budget, 100.0 * used / llme.token_budget))
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
    parser.add_argument(      "--box", type=str, help="The (sand)box tool used to run commands [box]")
    parser.add_argument(      "--max-tool-len", type=int, help="Maximum size of tool output in bytes (0 for unlimited) [max_tool_len]")
    parser.add_argument(      "--timeout-tool", type=int, help="Maximum duration in seconds of tool runs (0 for unlimited) [timeout_tool]")
    parser.add_argument(      "--timeout-http", type=int, help="Timeout of LLM connexion (0 for unlimited) [timeout_http]")
    parser.add_argument(      "--file-mode", choices=["part", "path","json"], help="How (non image) files are given to the LLM [file_mode]")
    parser.add_argument("-c", "--config", metavar="FILE", action="append", help="Custom configuration files").completer = config_completer
    parser.add_argument(      "--list-tools", action="store_true", default=None, help="List available tools then exit")
    parser.add_argument(      "--dump-config", action="store_true", default=None, help="Print the effective config and quit")
    parser.add_argument(      "--raw-request-dump", metavar="FILE", help="Export the full POSTed json payload [raw_request_dump]")
    parser.add_argument(      "--raw-response-dump", metavar="FILE", help="Export the full json message response [raw_response_dump]")
    parser.add_argument(      "--dummy-responses", metavar="FILE", help="Mock the server responses with FILE: a json array, a single message, or a jsonl of --raw-response-dump outputs. No server needed [dummy_responses]")
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

    if not args.base_url and not args.dummy_responses:
        logger.error("Error: --base-url required and not defined the config file.")
        sys.exit(2)

    if args.history_filename is None:
        args.history_filename = os.path.expanduser("~/.config/llme/history")

    return parser, args


def register_builtin_tools(llme):
    """Register the built-in tools bound to the given LLME instance."""
    tool(llme.run_command)
    tool(llme.update_file)
    tool(llme.image_description, has_parts=True)


def main():
    """The main CLI entry point."""
    try:
        argparser, config = process_args()
        llme = LLME(config)
        llme.argparser = argparser # FIXME too much hacky
        register_builtin_tools(llme)
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

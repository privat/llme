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

from .slash import all_slash_commands
from .config import Config, YAMLAction, config_completer, process_args, resolve_config
from .errors import AppError
from .history import HistoryMixin
from .logging import set_verbose
from .loop import LoopMixin
from .server import Metrics, ServerMixin, Warmup, extract_requests_error
from .terminal import Spinner
from .tools import Asset, Tool, ToolsMixin, all_tools, list_tools, load_plugin, register_builtin_tools, tool
from .ui import SlashCompleter, UIMixin

import prompt_toolkit
import httpx
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
        self.raw_response_dump_file = None # Kept-open jsonl file for raw responses
        self.token_budget = None
        self.dummy_responses_queue = None # Canned responses for --dummy-responses (lazily loaded)
        self.dummy_responses_index = 0 # Next canned response to return

        # Slash commands registry, collected from the @slash decorators
        self.slash_commands = all_slash_commands(self)

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
            if not models:
                # get_models() already logged the reason
                raise AppError(f"Can't get models from {self.config.base_url}")
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
            # No system prompt (even if there is a template)
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
            if self.chat_output_file is not None:
                self.chat_output_file.close()
            if self.raw_response_dump_file is not None:
                self.raw_response_dump_file.close()
            if self.warmup is not None:
                self.warmup.stop()

        if self.metrics.total:
            cprint(f"Total: {self.metrics.infoline(self.metrics.total, self)}", "light_grey")
        if self.config.session:
            cprint(f"Continue this session with --session {self.config.session}", "light_cyan")

def main():
    """The main CLI entry point."""
    try:
        config = process_args()
        llme = LLME(config)
        register_builtin_tools(llme)
        if config.list_tools:
            list_tools()
            sys.exit(0)

        if config.dump_system_prompt:
            print(llme.prepare_system_prompt()["content"])
            sys.exit(0)

        llme.start()
    except AppError as e:
        logger.error("%s", e)
        sys.exit(1)
    except httpx.HTTPError as e:
        logger.error("Server error: %s", extract_requests_error(e))
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())

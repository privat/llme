"""User interface: prompt, key bindings, slash commands, and printable views."""

import argparse
import logging
import os
import re

import prompt_toolkit
from termcolor import cprint, colored

from . import skills
from .config import search_action
from .slash import slash
from .errors import AppError, CancelEvent, QuitEvent
from .logging import set_verbose
from .tools import Asset

logger = logging.getLogger('llme')


class UIMixin:
    """LLME mixin: interactive UI (prompt, key bindings, slash commands)."""
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

    def confirm(self, prompt, question, default=""):
        """Ask a yes/no confirmation to the user"""
        if self.config.yolo and self.message_index is None:
            cprint(f"{question}: YOLO!", color="light_yellow")
            return True
        if self.config.batch:
            raise AppError("Confirmation unavailable in batch mode")
        try:
            cprint(f"{question}", color="light_yellow")
            if self.session:
                x = self.session.prompt([("#ff0000", f"{prompt}? ")], placeholder=[("#7f7f7f", "Enter to confirm, or give a prompt to cancel")], default=default, rprompt="")
            else:
                x = input(colored(f"{prompt}? ", "light_yellow"))
            self.failsafe = False # user input still alive
            if x == "":
                return True
            self.prompts.insert(0, x)
            return False
        except KeyboardInterrupt:
            raise QuitEvent("Confirmation interrupted")

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
                self.warmup.check()
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
        except EOFError:
            raise QuitEvent("EOF")


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
        if user_input[0] == '!':
            self.cmd_shell(user_input[1:])
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


    @slash("skills", "list available skills")
    def list_skills(self):
        """List skills"""
        skills.list_skills(self.skills)

    @slash("models", "list available models")
    def list_models(self):
        "Print the list of models"
        print(f"Models of {self.config.base_url}:")
        models = self.get_models()
        if not models:
            # get_models() already logged the reason
            raise AppError(f"Can't get models from {self.config.base_url}")
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


    @slash("history", "list condensed conversation history")
    def list_history(self):
        "Print the history of messages"
        for i, message in enumerate(self.history):
            if self.message_index and i >= self.message_index:
                break
            self.print_message(i, message)

    @slash("full-history", "list hierarchical conversation history (with forks)")
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

    # ---- Slash commands (dispatched by slash_command) ----

    @slash("file", "attach a file for the next prompt", metavar="FILE", missing="paths", complete="path")
    def cmd_file(self, rest):
        import shlex
        for path in shlex.split(rest):
            self.files.append(Asset(path))

    @slash("shell", "run a shell command in the current environment (alias: !CMD)", metavar="CMD", missing="command")
    def cmd_shell(self, command):
        import subprocess
        if self.config.box:
            import shlex
            cmd = shlex.split(self.config.box, posix=True)
            cmd.append(command)
        else:
            cmd = ["bash", "-c", command]
        subprocess.run(cmd)

    @slash("metrics", "list current metrics")
    def cmd_metrics(self):
        for k, v in self.metrics.total.items():
            print(f"{k}: {repr(v)}")

    @slash("config", "list configuration options")
    def cmd_config(self):
        for k, v in self.config.to_dict().items():
            print(f"{k}: {repr(v)}")

    @slash("set", "change a config option", metavar="OPT=VAL", missing="setting")
    def cmd_set(self, rest):
        if "=" not in rest:
            raise AppError("/set: Syntax error, expected name=value")
        opt, _, val = rest.partition("=")
        self.set_config(opt, val)

    @slash("quit", "exit the program")
    def cmd_quit(self):
        raise QuitEvent("/quit")

    @slash("help", "show this help")
    def help_commands(self):
        """Print the list of the available slash commands"""
        entries = []
        for cmd, _ in self.slash_commands.values():
            entry = f"/{cmd.name}" + (f" {cmd.metavar}" if cmd.metavar else "")
            entries.append((entry, cmd.doc))
        width = max(max(len(entry) for entry, _ in entries),23)
        for entry, doc in entries:
            print(f"{entry:<{width}} {doc}")

    def slash_command(self, user_input):
        """Dispatch a /slash command to the @slash method that handles it"""
        parts = user_input.split(None, 1)
        name = parts[0][1:]
        arg = parts[1].strip() if len(parts) > 1 else ""
        if not name:
            # A bare / is a shortcut for /help
            return self.help_commands()
        if name == "?":
            name = "help"
        cmd = self.slash_commands.get(name)
        if cmd is None:
            # Allow a unique prefix, e.g. /he for /help
            candidates = [c for n, c in self.slash_commands.items() if n.startswith(name)]
            if len(candidates) == 1:
                cmd = candidates[0]
            elif candidates:
                raise AppError(f"{user_input}: Ambiguous slash command. Use /help for help.")
        if cmd is None and re.fullmatch(r"\d+\w*", name):
            # Shortcut: /5c == /goto 5c
            return self.goto(name)
        if cmd is None:
            raise AppError(f"{user_input}: Unknown slash command. Use /help for help.")
        slash_cmd, fn = cmd
        if slash_cmd.metavar and not arg and slash_cmd.missing is not None:
            # missing=None: the argument is optional, the method is called with ""
            raise AppError(f"/{slash_cmd.name}: Missing {slash_cmd.missing}")
        return fn(self, arg) if slash_cmd.metavar else fn(self)

    def set_config(self, opt, val):
        "Dynamically change a config option"
        opt = opt.strip()
        val = val.strip()
        opts = [ k for k in self.config.to_dict() if k.startswith(opt)]
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
        self.config.set(opt, val)

class SlashCompleter(prompt_toolkit.completion.Completer):
    """A completer for slash commands.
    For some reasons, the provided completers do not like 'words' with / at the beginning"""
    def __init__(self, llme):
        self.commands = llme.slash_commands

        # nesting completer: a dict associates a command to a sub-completer
        self.nesting = {}
        for cmd, fn in llme.slash_commands.values():
            self.nesting[cmd.name] = prompt_toolkit.completion.PathCompleter(expanduser=True) if cmd.complete == "path" else None
        self.nesting["set"] = SetOptionCompleter(llme)

        self.completer = prompt_toolkit.completion.NestedCompleter.from_nested_dict(self.nesting)

    def get_completions(self, document, complete_event):
        if not document.text.startswith("/"):
            return
        new_document = prompt_toolkit.document.Document(text=document.text[1:], cursor_position=len(document.text)-1)
        if " " not in new_document.text_before_cursor:
            # Completing a command (no space implies first word)
            word = new_document.get_word_before_cursor()
            # Completing a command name: show the command signature and its help
            for name, (cmd, fn) in self.commands.items():
                if name.startswith(word):
                    display = "/" + name
                    if cmd.metavar: # argument?
                        name += " " # inject a space after the command name (on completion)
                        display += " " + cmd.metavar # inject the metavar name in the menu
                    yield prompt_toolkit.completion.Completion(name, start_position=-len(word), display=display, display_meta=cmd.doc)
            return
        # Completing an argument: delegate to the nested completer
        yield from self.completer.get_completions(new_document, complete_event)

class SetOptionCompleter(prompt_toolkit.completion.Completer):
    """A completer for the option of /set."""
    notsettable = ["config", "no_session", "no_skills", "plugins", "prompts", "session"]

    def __init__(self, llme):
        self.llme = llme
        self.config = llme.config

    def get_completions(self, document, complete_event):
        # The last whitespace-separated chunk before the cursor: "OPT" or "OPT=VALUE"
        # ("=" is a word boundary for prompt_toolkit, so the default word extraction is not enough)
        word = re.split(r"\s", document.text_before_cursor, 1)[-1]
        name, sep, val = word.partition("=")
        if sep:
            # A value is being typed
            return
        # A option name is being typed
        for opt, value in self.config.to_dict().items():
            if opt in self.notsettable:
                continue
            if not opt.startswith(name):
                continue
            action = search_action(self.config.parser, opt)
            if action.help:
                meta = f"{action.help} (current value: {value!r})"
            else:
                meta = f"current value: {value!r}"
            if action.metavar:
                display = opt + "=" + action.metavar
            elif isinstance(action, argparse._StoreTrueAction):
                display = opt + "=BOOL"
            elif isinstance(action, argparse._CountAction):
                display = opt + "=INT"
            elif action.type:
                display = opt + action.type.__name__.upper()
            else:
                display = opt + "=STR"
            yield prompt_toolkit.completion.Completion(text=opt, start_position=-len(word), display=display, display_meta=meta)

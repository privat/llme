"""User interface: prompt, key bindings, slash commands, and printable views."""

import logging
import os
import re

import prompt_toolkit
from termcolor import cprint, colored

from . import skills
from .config import setconf
from .errors import AppError, CancelEvent, QuitEvent
from .logging import set_verbose
from .tools import Asset, list_tools

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

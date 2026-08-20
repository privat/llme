"""Main loop: the user/assistant/tool ping-pong and orchestration."""

import logging
import time

import requests

from termcolor import colored, cprint

from . import skills
from .errors import AppError, CancelEvent, QuitEvent
from .server import extract_requests_error
from .terminal import Spinner
from .tools import all_tools

logger = logging.getLogger('llme')


class LoopMixin:
    """LLME mixin: the user/assistant/tool ping-pong loop."""
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

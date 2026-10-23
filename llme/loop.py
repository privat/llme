"""Main loop: the user/assistant/tool ping-pong and orchestration."""

import logging
import os
import subprocess
import time

import httpx

import jinja2
import jinja2.sandbox
from termcolor import colored, cprint

from . import skills
from .slash import slash
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
        self.fork_if_required("assistant")
        message = self.chat_completion(**kwargs)
        if message:
            self.add_message(message)
        return message

    def do_tool(self, tool_call):
        """Run the tool, and add result to the conversation"""
        message = self.run_tool(tool_call)
        if message:
            # Stash the tool call before adding: it is used to re-run the tool
            # from a paused tool result (and is persisted in session dumps)
            message.setdefault("llme-meta", {})["tool_call"] = tool_call
            self.add_message(message)
        else:
            # The user cancelled the tool execution. Let they answer instead of the tool
            self.do_user()

    def do_tool_pause(self, tool_call):
        """Prompt the user at a paused tool result.
        An empty answer re-runs the tool (the default action of the pause,
        like confirming an unchanged user message), a typed message is
        inserted after the tool result, and slash commands (/redo, /pass,
        /goto, !) are handled as usual."""
        while file := self.next_asset():
            self.files.append(file)
        user_input = self.next_input()
        if user_input == "":
            self.do_tool(tool_call)
        elif user_input[0] == "/":
            self.slash_command(user_input)
        elif user_input[0] == "!":
            self.cmd_shell(user_input[1:])
        else:
            self.add_message(self.prompt_message(user_input))

    def do_role(self, oneround=False, tools=None):
        """Process the next role (user, assistant, tool...)"""
        if not self.history:
            self.do_user()
            return None

        role = None
        if self.message_index is not None:
            message = self.history[self.message_index]
            role = message.role()
            logger.info("Index: %s; role: %s", self.message_index, role)
            if role in ("user", "system", "developer"):
                # A paused user message: edit it and resend
                # ('developer' is the new OpenAI role that replaces 'system')
                self.do_user()
            elif role == "tool":
                # A paused tool result: let the user intervene (insert a
                # message, re-run the tool with enter, /redo the assistant,
                # or /pass to continue). A tool result is never re-run
                # silently, as it might not be idempotent.
                tool_call = message.data["llme-meta"].get("tool_call")
                if tool_call is None:
                    logger.warning("Tool result without associated tool call, cannot re-run")
                    self.do_user()
                else:
                    self.do_tool_pause(tool_call)
            elif role == "assistant":
                # We relaunch the prompt and might get a different answer
                self.do_assistant(tools=tools)
            else:
                raise Exception(f"Unexpected role {role}")
            return None

        previous_message = self.history[-1]
        previous_role = previous_message.role()
        if previous_role == "user" or previous_role == "tool":
            role = "assistant"
        elif previous_role in ("system", "developer"):
            role = "user"
        elif previous_role == "assistant":
            tool_calls = previous_message.tool_calls()
            if not tool_calls and oneround:
                return previous_message
        if previous_role == "user" or previous_role == "tool":
            if self.token_budget and self.token_budget_start + self.token_budget <= self.metrics.predicted_n():
                self.add_message({"role": "user", "content": "final answer now. No more tools available. You have to conclude."})
                tools=[]
            self.do_assistant(tools=tools)
        elif previous_role in ("system", "developer"):
            self.do_user()
        elif previous_role == "assistant":
            tool_calls = previous_message.tool_calls()
            if not tool_calls and oneround:
                return previous_message
            if tool_calls:
                for tool_call in tool_calls:
                    self.do_tool(tool_call)
            else:
                if self.config.auto_compact:
                    metrics = previous_message.data.get("llme-meta", {}).get("metrics", {})
                    if "prompt_tokens" in metrics:
                        context_tokens = metrics["prompt_tokens"] + (metrics.get("completion_tokens") or metrics.get("predicted_n") or 0)
                        if self.config.auto_compact < context_tokens:
                            cprint(f"{self.prompt_prefix()}> Auto-compaction ({context_tokens} tokens)", color="light_cyan")
                            self.compact()
                self.do_user()
        else:
            # Unknown role at the end of the history: get the next user
            # prompt instead of looping forever
            logger.warning("Unknown role %r at the end of the history", previous_role)
            self.do_user()
        return None

    def do_sleep(self, delay):
        """Throttling server"""
        try:
            if self.config.plain:
                cprint(f"Throttled for {delay}s...", "light_cyan")
                time.sleep(delay)
                return
            with Spinner("light_cyan", self.config.plain) as am:
                for i in range(delay, 0, -1):
                    # Stop the spinner while printing, or the two write
                    # over each other on the same line
                    am.stop()
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
            except httpx.HTTPError as e:
                delay = self.get_throttling_delay(e)
                if delay:
                    logger.error("Server error: %s", extract_requests_error(e))
                    self.do_sleep(delay)
                    continue
                if self.config.batch:
                    raise
                logger.error("Server error: %s", extract_requests_error(e))
                if getattr(e, "response", None) is not None and e.response.status_code == 404:
                    models = self.get_models()
                    if models and self.model not in (m["id"] for m in models):
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
                logger.error("Unexpected and uncatched exception: %s\nllme might be in a bad state, proceed with caution.", e)
                self.rollback()
            if self.config.batch:
                break


    def get_agents_md(self):
        """Search for an AGENTS.md from the current directory up to the root, and return its content."""
        if self.config.no_agents_md:
            return None
        directory = os.getcwd()
        while True:
            path = os.path.join(directory, "AGENTS.md")
            if os.path.isfile(path):
                try:
                    with open(path, encoding="utf-8") as f:
                        return f.read().strip()
                except OSError as e:
                    logger.warning("Can't read %s: %s", path, e)
                    return None
            parent = os.path.dirname(directory)
            if parent == directory:
                return None
            directory = parent

    def prepare_system_prompt(self, **more_context):
        """Build the system message from the system prompt template."""
        if self.config.tool_mode == "markdown":
            tools = [ tool for tool in all_tools.values() if tool.markdown ]
        else:
            tools = None
        self.skills = skills.discover_skills(self.config.skills_path)
        # A broken box (missing command, ssh drop, ...) must give a clean
        # error, not a traceback at startup
        try:
            date = self.direct_run_command("date").decode().strip()
            pwd = self.direct_run_command("pwd").decode().strip()
        except (OSError, subprocess.CalledProcessError) as e:
            raise AppError(f"Box command failed: {e}")

        context = {
                "system_prompt": self.config.system_prompt,
                "tools": tools,
                "skills": self.skills.values(),
                "agents_md": self.get_agents_md(),
                "date": date,
                "pwd": pwd,
                "compaction_summary": None,
        }
        context.update(more_context)

        template = self.config.system_prompt_template or "{{system_prompt}}{%if compaction_summary%}\n\n{{compaction_summary}}{%endif%}"
        env = jinja2.sandbox.SandboxedEnvironment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=False,
            autoescape=False,
            undefined=jinja2.StrictUndefined,
        )
        try:
            rendered = env.from_string(template).render(context)
        except Exception as e:
            raise AppError(f"System prompt template error") from e

        return {"role": "system", "content": rendered.strip()}


    @slash("compact", "summarize the history and restart fresh, then process the given prompt", metavar="[PROMPT]", missing=None)
    def compact(self, prompt=""):
        """Force the summarization of the conversation"""
        compaction_prompt = self.config.compaction_prompt
        if not compaction_prompt:
            logger.error("No compaction prompt defined")
            return
        message = {"role": "user", "content": compaction_prompt}
        self.add_message(message)

        # Temporally disable tools
        response = self.do_assistant(tools=[])
        content = response.get("content") if response else None
        if not content:
            logger.error("Agent did not compact. Bad agent!")
            return
        self.reset_messages([self.prepare_system_prompt(compaction_summary=content)])
        # If the user gave a next prompt, queue it so it is processed as soon as
        # the compaction is done (without the user having to wait and retype it).
        if prompt:
            self.prompts.insert(0, prompt)

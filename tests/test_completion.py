"""Tests for the prompt_toolkit completers: SlashCompleter and SetOptionCompleter.
The completers run against the real CLI parser and the real slash command registry, covering the space of options, metavars, choices and completion kinds.
The server is never contacted: get_models is mocked.
"""
import argparse

import pytest
from prompt_toolkit.completion import CompleteEvent
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import to_plain_text

from llme.config import Config, build_parser, model_completer
from llme.main import LLME
from llme.slash import all_slash_commands
from llme.ui import notsettable, SetOptionCompleter, SlashCompleter

MODELS = [
    {"id": "llama-3-8b", "state": "loaded"},
    {"id": "gpt-4o", "state": None},
    {"id": "mixtral", "state": "unloaded"},
]
MODELS_SORTED = [m["id"] for m in sorted(MODELS, key=lambda m: m["id"])]

# The real registry of slash commands (all_slash_commands only needs the class hierarchy)
REGISTRY = all_slash_commands(LLME.__new__(LLME))
PATH_COMMANDS = [name for name, (cmd, _) in REGISTRY.items() if cmd.complete == "path"]


def complete(completer, text):
    """The completions of a completer for a given text (cursor at the end, tab pressed)."""
    event = CompleteEvent(completion_requested=True)
    return list(completer.get_completions(Document(text), event))


@pytest.fixture
def llme(monkeypatch):
    """A real LLME with an empty config and a mocked get_models (no server)."""
    parser = build_parser()
    config = Config(parser)
    parser.parse_args([], namespace=config)
    config.batch = True  # force the sessionless (no prompt_toolkit) path
    app = LLME(config)
    calls = []

    def get_models():
        calls.append(None)
        return MODELS

    monkeypatch.setattr(app, "get_models", get_models)
    app.get_models_calls = calls
    return app


class TestSlashCompleter:
    @pytest.fixture
    def sc(self, llme):
        return SlashCompleter(llme)

    def test_non_slash_text_has_no_completions(self, sc):
        assert complete(sc, "hello") == []
        assert complete(sc, "a b") == []
        assert complete(sc, "") == []

    def test_bare_slash_lists_all_commands(self, llme, sc):
        expected = [name + (" " if cmd.metavar else "") for name, (cmd, _) in llme.slash_commands.items()]
        assert [c.text for c in complete(sc, "/")] == expected

    def test_command_name_prefix(self, sc):
        assert [c.text for c in complete(sc, "/h")] == ["help", "history"]  # registry order: UIMixin before HistoryMixin
        assert [c.text for c in complete(sc, "/he")] == ["help"]
        assert [c.text for c in complete(sc, "/sk")] == ["skills"]

    def test_command_completion_without_metavar(self, sc):
        (c,) = complete(sc, "/qu")
        assert (c.text, to_plain_text(c.display), c.start_position) == ("quit", "/quit", -2)
        assert to_plain_text(c.display_meta) == "exit the program"

    def test_command_completion_with_metavar(self, sc):
        # The space after the command name is part of the completion text, so accepting it starts the argument
        (c,) = complete(sc, "/se")
        assert (c.text, to_plain_text(c.display), c.start_position) == ("set ", "/set OPT=VAL", -2)
        assert to_plain_text(c.display_meta) == "change a config option"

    @pytest.mark.parametrize("command", PATH_COMMANDS)
    def test_path_argument_completions(self, sc, tmp_path, monkeypatch, command):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "prompt.txt").write_text("")
        (tmp_path / "subdir").mkdir()
        files = complete(sc, f"/{command} prom")
        assert [(c.text, to_plain_text(c.display)) for c in files] == [("pt.txt", "prompt.txt")]
        dirs = complete(sc, f"/{command} sub")
        assert [(c.text, to_plain_text(c.display)) for c in dirs] == [("dir", "subdir/")]

    def test_argument_of_other_commands_has_no_completions(self, sc):
        assert complete(sc, "/quit x") == []
        assert complete(sc, "/help ") == []

    def test_set_delegates_to_option_completer(self, sc):
        assert [c.text for c in complete(sc, "/set model=")] == MODELS_SORTED
        assert [c.text for c in complete(sc, "/set plain=f")] == ["false"]


class TestSetOptionCompleter:
    @pytest.fixture
    def sc(self, llme):
        return SetOptionCompleter(llme)

    def test_empty_prefix_lists_settable_options(self, llme, sc):
        expected = {k for k in llme.config.to_dict() if k not in notsettable}
        assert {c.text for c in complete(sc, "")} == expected

    def test_prefix_filters_options(self, sc):
        assert {c.text for c in complete(sc, "m")} == {"model", "max_tool_len"}
        assert complete(sc, "zz") == []

    def test_notsettable_options_are_hidden(self, sc):
        assert complete(sc, "session") == []
        assert complete(sc, "conf") == []  # config
        assert complete(sc, "no-s") == []  # no_session and no_skills

    def test_option_display(self, sc):
        display = {c.text: to_plain_text(c.display) for c in complete(sc, "")}
        assert display["base_url"] == "base_url=URL"
        assert display["model"] == "model=NAME"
        assert display["plain"] == "plain=BOOL"
        assert display["verbose"] == "verbose=INT"
        assert display["auto_compact"] == "auto_compact=INT"
        assert display["temperature"] == "temperature=FLOAT"
        assert display["skills_path"] == "skills_path=DIR"
        assert display["box"] == "box=STR"

    def test_option_meta_is_help_and_current_value(self, llme, sc):
        llme.config.model = "my-model"
        (c,) = complete(sc, "model")
        assert to_plain_text(c.display_meta) == "Model name or identifier [model] (current value: 'my-model')"

    def test_model_values(self, sc):
        assert [c.text for c in complete(sc, "model=")] == MODELS_SORTED
        assert [c.text for c in complete(sc, "model=zzz")] == []

    def test_model_values_are_case_insensitive(self, sc):
        assert [c.text for c in complete(sc, "model=GPT")] == ["gpt-4o"]

    def test_model_meta(self, llme, sc):
        llme.model = "llama-3-8b"
        meta = {c.text: to_plain_text(c.display_meta or "") for c in complete(sc, "model=")}
        assert meta == {"gpt-4o": "", "llama-3-8b": "current model", "mixtral": ""}

    def test_model_state_meta(self, sc):
        meta = {c.text: to_plain_text(c.display_meta or "") for c in complete(sc, "model=")}
        assert meta["llama-3-8b"] == "loaded"
        assert meta["mixtral"] == ""  # an unloaded model has no state worth showing

    def test_choice_values(self, sc):
        assert [c.text for c in complete(sc, "tool_mode=")] == ["markdown", "native"]
        assert [c.text for c in complete(sc, "tool_mode=n")] == ["native"]
        assert [c.text for c in complete(sc, "file_mode=p")] == ["part", "path"]

    def test_choice_current_meta(self, llme, sc):
        llme.config.tool_mode = "native"
        meta = {c.text: to_plain_text(c.display_meta or "") for c in complete(sc, "tool_mode=")}
        assert meta == {"markdown": "", "native": "current"}

    def test_bool_values(self, sc):
        assert [c.text for c in complete(sc, "plain=")] == ["true", "false"]
        assert [c.text for c in complete(sc, "plain=f")] == ["false"]
        assert complete(sc, "plain=x") == []

    def test_bool_current_meta(self, llme, sc):
        llme.config.plain = True
        meta = {c.text: to_plain_text(c.display_meta or "") for c in complete(sc, "plain=")}
        assert meta == {"true": "current", "false": ""}

    def test_file_values(self, sc, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "out.json").write_text("{}")
        assert [(c.text, to_plain_text(c.display)) for c in complete(sc, "chat_output=out")] == [(".json", "out.json")]

    def test_dir_values(self, sc, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "afile").write_text("")
        (tmp_path / "adir").mkdir()
        assert [(c.text, to_plain_text(c.display)) for c in complete(sc, "skills_path=a")] == [("dir", "adir/")]

    def test_value_of_unknown_option(self, sc):
        assert complete(sc, "foo=bar") == []

    def test_value_of_ambiguous_option(self, sc):
        assert complete(sc, "m=x") == []

    def test_typed_option_has_no_value_completions(self, sc):
        assert complete(sc, "auto_compact=1") == []

    def test_option_names_use_config_form(self, sc):
        # Option names are config keys (underscore form), like /set expects
        assert complete(sc, "tool-mode=n") == []

    def test_resolve_option(self, sc):
        assert sc.resolve_option("model") == "model"
        assert sc.resolve_option("auto_c") == "auto_compact"
        assert sc.resolve_option("m") is None  # ambiguous
        assert sc.resolve_option("zz") is None

    def test_server_models_are_cached(self, llme, sc):
        complete(sc, "model=")
        complete(sc, "model=")
        assert len(llme.get_models_calls) == 1
        sc._models_time = 0  # expire the cache
        complete(sc, "model=")
        assert len(llme.get_models_calls) == 2

    def test_server_error_has_no_completions(self, llme, sc, monkeypatch):
        calls = []

        def get_models():
            calls.append(None)
            raise RuntimeError("no server")

        monkeypatch.setattr(llme, "get_models", get_models)
        assert complete(sc, "model=") == []
        assert complete(sc, "model=") == []
        assert len(calls) == 2  # failures are not cached, each request retries


# --- model_completer (argcomplete, --model) ---------------------------------------

def test_model_completer_partial_namespace():
    """argcomplete passes a partial namespace: the completer must not raise, it just has no completion."""
    parser = build_parser()
    partial = argparse.Namespace(model=None)
    assert list(model_completer("", partial, parser)) == []

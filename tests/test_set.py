"""Tests for the /set slash command: suspicious and edge-case inputs.
A bad value must fail with a clean AppError (never a raw exception), an empty value unsets the option.
Runs against the real parser and config; the server is never contacted.
"""
import pytest

from llme.config import Config, build_parser
from llme.errors import AppError
from llme.main import LLME


@pytest.fixture
def app(monkeypatch):
    """A real LLME with an empty config, in batch mode (no prompt_toolkit, no server)."""
    parser = build_parser()
    config = Config(parser)
    parser.parse_args([], namespace=config)
    config.batch = True  # force the sessionless (no prompt_toolkit) path
    llme = LLME(config)
    monkeypatch.setattr(llme, "get_models", lambda: [])
    calls = []
    monkeypatch.setattr("llme.ui.set_verbose", lambda level: calls.append(level))
    llme.set_verbose_calls = calls
    return llme


def setcmd(app, arg):
    app.slash_command(f"/set {arg}")


# --- Syntax errors -----------------------------------------------------------

def test_missing_argument(app):
    with pytest.raises(AppError, match="Missing setting"):
        app.slash_command("/set")

def test_no_equals(app):
    with pytest.raises(AppError, match="Syntax error"):
        setcmd(app, "plain")

def test_empty_name_is_ambiguous(app):
    with pytest.raises(AppError, match="Ambiguous setting"):
        setcmd(app, "=x")

# --- Unknown and ambiguous names ---------------------------------------------

def test_unknown_option(app):
    with pytest.raises(AppError, match="Unknown setting: doesnotexist"):
        setcmd(app, "doesnotexist=1")

def test_ambiguous_prefix(app):
    with pytest.raises(AppError, match="Ambiguous setting"):
        setcmd(app, "sys=1")  # system_prompt and system_prompt_template

def test_dash_form_is_not_resolved(app):
    # Option names are config (underscore) names, like set_config
    with pytest.raises(AppError, match="Unknown setting: tool-mode"):
        setcmd(app, "tool-mode=native")

# --- Valid values --------------------------------------------------------------

def test_float(app):
    setcmd(app, "temperature=0.5")
    assert app.config.temperature == 0.5

def test_int_string_converted(app):
    setcmd(app, "temp=1")
    assert app.config.temperature == 1.0

def test_bool(app):
    setcmd(app, "plain=yes")
    assert app.config.plain is True

def test_whitespace_ignored(app):
    setcmd(app, "temperature = 0.25")
    assert app.config.temperature == 0.25

def test_empty_value_unsets(app):
    setcmd(app, "temperature=0.5")
    setcmd(app, "temp=")
    assert app.config.temperature is None

def test_empty_bool_unsets(app):
    setcmd(app, "plain=1")
    setcmd(app, "plain=")
    assert app.config.plain is None

def test_empty_append_unsets_to_empty_list(app):
    setcmd(app, "skills_path=/tmp")
    setcmd(app, "skills_path=")
    assert app.config.skills_path == []

def test_model(app):
    setcmd(app, "model=gpt-4o")
    assert app.model == "gpt-4o"
    assert app.config.model == "gpt-4o"

def test_empty_model_unsets(app):
    setcmd(app, "model=gpt-4o")
    setcmd(app, "model=")
    assert app.model is None
    assert app.config.model is None

def test_verbose(app):
    setcmd(app, "verbose=2")
    assert app.config.verbose == 2
    assert app.set_verbose_calls == [2]

def test_empty_verbose_resets(app):
    setcmd(app, "verbose=2")
    setcmd(app, "verbose=")
    assert app.config.verbose == 0
    assert app.set_verbose_calls == [2, 0]

def test_choices(app):
    setcmd(app, "tool_mode=markdown")
    assert app.config.tool_mode == "markdown"

def test_extra_body_yaml(app):
    setcmd(app, "extra_body=top_p: 0.5")
    assert app.config.extra_body == {"top_p": 0.5}

# --- Invalid values: clean AppError, never a raw exception ---------------------

def test_invalid_bool(app):
    with pytest.raises(AppError, match="Invalid value for plain: 5"):
        setcmd(app, "plain=5")

def test_invalid_bool_yolo(app):
    with pytest.raises(AppError, match="Invalid value for yolo: maybe"):
        setcmd(app, "yolo=maybe")

def test_invalid_float(app):
    with pytest.raises(AppError, match="Invalid value for temperature: abc"):
        setcmd(app, "temperature=abc")

def test_invalid_int(app):
    with pytest.raises(AppError, match="Invalid value for auto_compact: xyz"):
        setcmd(app, "auto_compact=xyz")

def test_invalid_verbose(app):
    with pytest.raises(AppError, match="Invalid value for verbose: x"):
        setcmd(app, "verbose=x")

def test_invalid_choices(app):
    with pytest.raises(AppError, match="Invalid value for tool_mode: foo"):
        setcmd(app, "tool_mode=foo")

def test_invalid_file_mode_choices(app):
    with pytest.raises(AppError, match="Invalid value for file_mode: weird"):
        setcmd(app, "file_mode=weird")

def test_extra_body_not_a_dict(app):
    with pytest.raises(AppError, match="Invalid value for extra_body"):
        setcmd(app, "extra_body=foo")

def test_extra_body_bad_yaml(app):
    with pytest.raises(AppError, match="Invalid value for extra_body"):
        setcmd(app, "extra_body=[1,2")

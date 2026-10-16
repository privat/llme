"""Configuration handling: CLI options, config files, env vars, precedence and typed settings."""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import tomllib

import argcomplete

from . import skills
from .errors import AppError
from .logging import set_verbose
from .tools import load_plugin
try:
    from termcolor import can_colorize # Exported since v3.2.0
except ImportError:
    from termcolor.termcolor import _can_do_colour as can_colorize # Was private before v3.2.0

logger = logging.getLogger('llme')


def deep_update(orig, delta):
    """Deep update (only dicts, other are replaced)"""
    for k, v in delta.items():
        if isinstance(v, dict) and isinstance(orig.get(k), dict):
            deep_update(orig[k], v)
        else:
            orig[k] = v
    return orig

def apply_config(parser, args, config, path):
    """Apply a config dict to an args namespace without overwriting existing values (precedence).
    The method is a little ugly but it works... """
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
            if args.no_config:
                logger.debug("no_config: ignoring %s", path)
            else:
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

    logger.debug("Final config: %s", {k:v for k,v in vars(args).items() if v is not None})

def str2bool(s):
    "Convert a boolean value from a string (or another type) in a config file or env var"
    if isinstance(s, bool):
       return s
    if isinstance(s, (int, float)):
       # TOML config files give real numbers, not strings
       return bool(s)
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
            if action.default is None:
                return action
            else:
                # action without default are not configuration option (but basic flags)
                return  None
    return None

def setconf(parser, args, name, value):
    "Update a setting according to its type"
    action = search_action(parser, name)
    if not action:
        raise AppError(f"Unknown setting {name}")
    if value == "":
        # An empty value unsets the option (ex: /set temperature=)
        setattr(args, action.dest, [] if isinstance(action, argparse._AppendAction) else None)
        return
    if action.type == bool or isinstance(action, argparse._StoreTrueAction):
        # Special case for bool, as the action just store True
        try:
            value = str2bool(value)
        except ValueError:
            raise AppError(f"Invalid value for {name}: {value}")
        setattr(args, action.dest, value)
        return
    elif isinstance(action, argparse._CountAction):
        # The action would just increment by 1, ignoring the value
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise AppError(f"Invalid value for {name}: {value}")
        setattr(args, action.dest, value)
        return
    elif isinstance(action, argparse._AppendAction) and isinstance(value, list):
        # A config file gives a TOML array: extend the list, don't nest it
        items = getattr(args, action.dest, None) or []
        setattr(args, action.dest, list(items) + list(value))
        return
    elif action.type:
        try:
            value = action.type(value)
        except ValueError:
            raise AppError(f"Invalid value for {name}: {value}")
    if action.choices is not None and value not in action.choices:
        raise AppError(f"Invalid value for {name}: {value} (choose from {', '.join(action.choices)})")
    try:
        action(parser, args, value)
    except ValueError as e:
        raise AppError(f"Invalid value for {name}: {e}") from e

class Config(argparse.Namespace):
    """The effective configuration.
    It is a plain argparse namespace with an attribute for the original parser that holds the meta-information (help, type, etc)
    """
    def __init__(self, parser=None, **kwargs):
        super().__init__(**kwargs)
        self.parser = parser

    def set(self, name, value):
        """Dynamically change a setting, with type conversion"""
        setconf(self.parser, self, name, value)

    def to_dict(self):
        """The settings as a plain dict (dumping, logging)."""
        return { k: v for k, v in vars(self).items() if search_action(self.parser, k) }

class YAMLAction(argparse.Action):
    """Special action that takes, parse and deep-merge YAML-ish arguments"""
    def __call__(self, parser, namespace, values, option_string=None):
        import yaml
        orig = getattr(namespace, self.dest)
        if orig is None:
            orig = {}
            setattr(namespace, self.dest, orig)
        # QOL hack
        try:
            delta = yaml.safe_load(values)
        except yaml.YAMLError as e:
            raise ValueError(f"bad YAML: {e}") from e
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
    from .main import LLME # Local import: main imports config, so this must not be at module level
    # Models list depend on the other options (config and url), so parse them before!
    resolve_config(parser, parsed_args)
    llme = LLME(parsed_args)
    models = llme.get_models()
    if not models:
        return ()
    return (m["id"] for m in models if m["id"].startswith(prefix))

def build_parser():
    """Build the argparse parser with all the CLI options (extracted from process_args so tests can reuse it)."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options...] [prompts...]',
        description="OpenAI-compatible chat CLI.",
        epilog="Boolean flags can be negated with `--no-`. Example `--no-plain` to force colors in a non TTY. --- Use bracketed names in config files.",
        add_help=False,
    )
    # Trick: "store_true" options are defaulted to None, so we can distinguish between explicit --foo (True), --no-foo (False) and unset (None)
    parser.add_argument("-u", "--base-url", metavar="URL", help="API base URL")
    parser.add_argument("-m", "--model", metavar="NAME", help="Model name or identifier").completer = model_completer
    parser.add_argument(      "--list-models", action="store_true", help="List available models then exit")
    parser.add_argument(      "--api-key", metavar="SECRET", help="The API key")
    parser.add_argument("-b", "--batch", action="store_true", default=None, help="*Run non-interactively. Implicit if stdin is not a tty")
    parser.add_argument("-p", "--plain", action="store_true", default=None, help="*No colors or tty fanciness. Implicit if stdout is not a tty")
    parser.add_argument(      "--bulk", action="store_true", default=None, help="*Disable stream-mode. Not that useful but it helps debugging APIs")
    parser.add_argument(      "--session", help="Resume a previous session")
    parser.add_argument(      "--no-session", action="store_true", default=None, help="Do not save the session")
    parser.add_argument("-o", "--chat-output", metavar="FILE", help="*Export the full conversation in json")
    parser.add_argument("-i", "--chat-input", metavar="FILE", help="*Continue a previous (exported) conversation")
    parser.add_argument(      "--export-metrics", metavar="FILE", help="*Export metrics, usage, etc. in json")
    parser.add_argument("-s", "--system", dest="system_prompt", help="System prompt")
    parser.add_argument(      "--system-prompt-template", help="*System prompt Jinja2 template")
    parser.add_argument(      "--no-agents-md", action="store_true", default=None, help="Do not search for AGENTS.md and add it to the system prompt")
    parser.add_argument(      "--dump-system-prompt", action="store_true", help="*Print the rendered system prompt and quit")
    parser.add_argument(      "--auto-compact", type=int, help="Automatically compact when the context reaches that many tokens (0 for disabled)")
    parser.add_argument(      "--temperature", type=float, help="Temperature of predictions")
    parser.add_argument(      "--extra-body", metavar="YAML", action=YAMLAction, help="YAML/JSON element merged with requests (ex: `--extra-body 'top_p: 0.95'`)")
    parser.add_argument(      "--no-skills", action="store_true", default=None, help="Disable defaults skills (excepts those from --skills-path)")
    parser.add_argument(      "--skills-path", metavar="DIR", action="append", help="Add a skills directory for skill recursive search")
    parser.add_argument(      "--list-skills", action="store_true", help="List all discoverable agent skills then exit")
    parser.add_argument(      "--list-tools", action="store_true", help="List available tools then exit")
    parser.add_argument(      "--plugin", metavar="PATH", action="append", dest="plugins", help="Add additional tool (python file or directory)")
    parser.add_argument(      "--tool-mode", choices=["markdown", "native"], help="*How tools and functions are given to the LLM")
    parser.add_argument(      "--box", help="The (sand)box tool used to run commands")
    parser.add_argument(      "--max-tool-len", type=int, help="Maximum size of tool output in bytes (0 for unlimited)")
    parser.add_argument(      "--timeout-tool", type=int, help="Maximum duration in seconds of tool runs (0 for unlimited)")
    parser.add_argument(      "--timeout-http", type=int, help="Timeout of LLM connexion (0 for unlimited)")
    parser.add_argument(      "--file-mode", choices=["part", "path","json"], help="How (non image) files are given to the LLM")
    parser.add_argument("-c", "--config", metavar="FILE", action="append", help="Custom configuration files").completer = config_completer
    parser.add_argument(      "--no-config", action="store_true", help="*Disable default configuration files")
    parser.add_argument(      "--dump-config", action="store_true", help="*Print the effective config and quit")
    parser.add_argument(      "--raw-request-dump", metavar="FILE", help="*Export the full POSTed json payload")
    parser.add_argument(      "--raw-response-dump", metavar="FILE", help="*Export the full json message response, one per line (jsonl)")
    parser.add_argument(      "--dummy", action="store_true", default=None, help="*Disable LLM server for testing the UI alone")
    parser.add_argument(      "--dummy-responses", metavar="FILE", help="*Mock the server responses with FILE: a json array, a single message, or a jsonl of --raw-response-dump outputs")
    parser.add_argument("-H", "--history-filename", metavar="FILE", help="*Read/write command history from FILE")
    parser.add_argument("-v", "--verbose", action="count", help="Increase verbosity level (can be used multiple times)")
    parser.add_argument(      "--log-file", metavar="FILE", help="*Write logs to a file")
    parser.add_argument("-Y", "--yolo", action="store_true", default=None, help="UNSAFE: Do not ask for confirmation before running tools. Combine with --batch to reach the singularity")
    parser.add_argument(      "--version", action="store_true", help="Display version information and quit")
    parser.add_argument(      "--completion", action="store_true", help="Print shell completion script")
    parser.add_argument(      "--compaction-prompt", default=None, help="*Prompt used in automatic and manual compaction")
    parser.add_argument("-h", "--help", action="store_true", help="Show the basic options and exit")
    parser.add_argument(      "--help-full", action="store_true", help="Show all options and exit (advanced ones have * in help)")
    parser.add_argument("prompts", nargs='*', help="An initial list of prompts")
    for action in parser._actions:
        # Trick: iterate on store_true options to add the --no- variants
        if action.const is True:
            for name in action.option_strings:
                if name.startswith("--") and not name.startswith("--no-"):
                    parser.add_argument("--no" + name[1:], dest=action.dest, action="store_false", help=argparse.SUPPRESS)
        # Extends help with the config name (default is None means the option is settable in config)
        if action.help != argparse.SUPPRESS and action.default is None:
            action.help += f" [{action.dest}]"

    return parser

def process_args():
    """Handle command line arguments and envs."""
    parser = build_parser()
    argcomplete.autocomplete(parser)

    config = Config(parser)
    args = parser.parse_intermixed_args(namespace=config)
    if args.version:
        show_version()
        sys.exit(0)

    if args.help:
        for action in parser._actions:
            if action.help[0] == '*':
                action.help = argparse.SUPPRESS
        parser.print_help()
        sys.exit(0)

    if args.help_full:
        parser.print_help()
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
    logger.debug("Given arguments %s", {k:v for k,v in args.to_dict().items() if v is not None})

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
        json.dump(args.to_dict(), sys.stdout, indent=2)
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

    if not args.base_url and not args.dummy and not args.dummy_responses:
        # --dummy and --dummy-responses never contact a server
        logger.error("Error: --base-url required and not defined the config file.")
        sys.exit(2)

    if args.history_filename is None:
        args.history_filename = os.path.expanduser("~/.config/llme/history")

    return config

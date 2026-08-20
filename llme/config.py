"""Configuration handling: config files, env vars, precedence and typed settings."""

import argparse
import json
import logging
import os
import re
import sys
import tomllib

import argcomplete

from .errors import AppError

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
    #TODO check types
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
            # TODO type conversion
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
    if args.timeout_tool is None:
        args.timeout_tool = 600 # 10 min
    if args.timeout_http is None:
        args.timeout_http = 600
    if args.max_tool_len is None:
        args.max_tool_len = 100000


    logger.debug("Final config: %s", {k:v for k,v in vars(args).items() if v is not None})

def str2bool(s):
    "Convert a boolean value from a string in a config file or env var"
    if isinstance(s, bool):
       return s
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
            return action
    return None

def setconf(parser, args, name, value):
    "Update a setting according to its type"
    action = search_action(parser, name)
    if not action:
        raise AppError(f"Unknown setting {name}")
    if action.type == bool or isinstance(action, argparse._StoreTrueAction):
        # Special case for bool, as the action just store True
        value = str2bool(value)
        setattr(args, action.dest, value)
        return
    elif action.type:
        value = action.type(value)
    action(parser, args, value)

class YAMLAction(argparse.Action):
    """Special action that takes, parse and deep-merge YAML-ish arguments"""
    def __call__(self, parser, namespace, values, option_string=None):
        import yaml
        orig = getattr(namespace, self.dest)
        if orig is None:
            orig = {}
            setattr(namespace, self.dest, orig)
        # QOL hack
        delta = yaml.safe_load(values)
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

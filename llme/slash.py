"""Slash commands: the @slash decorator and the runtime command registry.

A slash command is a method of the LLME class hierarchy (typically one of
its mixins), decorated with @slash right next to the logic it invokes.
The registry is collected at runtime from the class hierarchy by
all_slash_commands(): there is no central list to maintain, and /help and
the completion are generated from it.
"""


class SlashCommand:
    """The metadata of a @slash-decorated method."""
    def __init__(self, name, doc, metavar="", missing=None, complete=None):
        self.name = name         # The command name, without the leading /
        self.doc = doc           # The description shown by /help
        self.metavar = metavar   # The argument placeholder; "" = no argument
        self.missing = missing   # The word shown in the "Missing ..." error
        self.complete = complete # The argument completion, if any (e.g. "path")


def slash(name, doc, metavar="", missing=None, complete=None):
    """Register a method as a /slash command.

    When metavar is set, the method is called as method(llme, arg) with the
    rest of the line as a single (non empty) string; the argument checking
    and parsing is left to the method. Otherwise it is called as
    method(llme).
    """
    def deco(fn):
        fn.__slash__ = SlashCommand(name, doc, metavar, missing, complete)
        return fn
    return deco


def all_slash_commands(llme):
    """Collect all the @slash-decorated methods of the llme class hierarchy.

    Return a dict of name -> (SlashCommand, unbound method), most derived
    class last (if a name is defined in several classes, the most derived wins).
    """
    commands = {}
    for klass in reversed(type(llme).__mro__):
        for value in vars(klass).values():
            cmd = getattr(value, "__slash__", None)
            if cmd is not None:
                commands[cmd.name] = (cmd, value)
    return commands

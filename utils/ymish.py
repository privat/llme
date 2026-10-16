#!/usr/bin/env python3

import json
import sys
from termcolor import colored, cprint

def pprint_json(data, indent=4, level=0, parent=None):
    if isinstance(data, dict):
        if isinstance(parent, dict):
            print()
            first = False
        else:
            first = True
        for key, value in data.items():
            if first:
                first = False
            else:
                print(" " * level, end="")
            cprint(str(key) + ":", "light_blue", end="")
            pprint_json(value, indent, level + indent, data)
    elif isinstance(data, list):
        if not isinstance(parent, list) and level > 0:
            level -= indent
            print()
            first = False
        else:
            if isinstance(parent, dict):
                print(" ", end="")
            first = True
        for item in data:
            if first:
                first = False
            else:
                print(" " * level, end="")
            cprint("  - ", "light_green", end="")
            pprint_json(item, indent, level + indent, data)
    elif isinstance(data, str):
        if isinstance(parent, dict):
            print(" ", end="")
        try:
            nested = json.loads(data)
            cprint("|#<JSON", "light_cyan")
            pprint_json(nested, indent, level, parent)
            return
        except json.decoder.JSONDecodeError:
            pass
        lines = data.split('\n')
        if len(lines) <= 1:
            cprint(repr(data))
            return
        cprint("|", "light_cyan")
        for i, line in enumerate(lines):
            if line != "":
                print(" " * level, end="")
            cprint(line)
    else:
        if isinstance(parent, dict):
            print(" ", end="")
        cprint(repr(data), "light_yellow")

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)
    pprint_json(data)

if __name__ == "__main__":
    main()

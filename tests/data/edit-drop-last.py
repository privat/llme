#!/usr/bin/env python3
"""Test editor: drop the last message of a yaml chat (for /edit tests)."""
import sys

import yaml

with open(sys.argv[1], "r") as f:
    messages = yaml.safe_load(f)
del messages[-1]
with open(sys.argv[1], "w") as f:
    yaml.dump(messages, f, default_flow_style=False, default_style="", width=65536)

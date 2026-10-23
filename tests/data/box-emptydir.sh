#!/bin/sh
# A fake (sand)box for the tests: run the given command in an empty temp
# directory, so that files from the llme working directory are not visible.
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cd "$tmp" || exit 1
exec sh -c "$@"

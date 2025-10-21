#!/bin/bash

# We just run things that should not fail (or not not fail)

set -xe
for config in *.toml; do
	[ "$config" = "pyproject.toml" ] && continue

	llme 'hello' 'world' -c "$config" -b >/dev/null
	llme 'hello' 'world' -c "$config" -b --bulk >/dev/null
	llme <<<'hello' 'world' -c "$config" >/dev/null
	llme <<<'hello' -c "$config" >/dev/null
	llme -v -v --config "$config" --dump-config > dumpconfig.txt
	! llme -m bad hello
	! llme -u bad hello
	! llme --bad hello
	! llme -c bad hello
done

echo "SUCCESS"

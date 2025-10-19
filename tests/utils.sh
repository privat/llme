#!/bin/bash

# Common setup and useful functions for test scripts

if [ ! -f venv ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt > /dev/null
SUITE=$(basename "$0" .sh)

# The llme tool to check
LLME="$(dirname $0)/../llme/main.py"

if [ ! -f "$LLME" ]; then
	echo "llme not found: $LLME" >&2
fi

# Register a test result
result() {
	url=`jq -r .base_url "logs/$id/config.json"`
	model=`jq -r .model "logs/$id/config.json"`
	echo "$SUITE, $task, $url, $model, $1" >> "logs/$id/result.csv"
	case $1 in
		ERROR*|FAIL*|TIMEOUT*)
			color=91;;
		PASS*|LIVED*)
			color=92;;
		*)
			color=93;;
	esac
	echo -e "\e[${color}m$1\e[0m logs/$id/"
}

# Check that the llm result matches the pattern $1 on the last line.
answer() {
	if tail -n1 "logs/$id/log.txt" | grep -x "$1"; then
		result "PASS"
		return 0
	elif grep -i "$1" "logs/$id/log.txt"; then
		result "ALMOST"
		return 1
	else
		echo -e "\e[91mFAIL\e[0m logs/$id/"
		result "FAIL"
		return 1
	fi
}

# Run a test with the llme tool
# Usage: tllme taskname [llme args...] (use "$@" for args)
tllme() {
	task=$1
	shift

	# Tests results are stored in logs/$id/ where id is a unique identifier
	id=$SUITE-$task-$(date +%s)
	echo "$id" >&2
	mkdir -p "logs/$id"
	env | grep "^LLME_" > "logs/$id/env.txt"

	export LLME_CHAT_OUTPUT="logs/$id/chat.json"
	export LLME_BATCH=true
	export LLME_YOLO=true

	if [ -n "$R" ]; then
		out=/dev/null
	else
		out=/dev/stdout
	fi

	"$LLME" "$@" --dump-config > "logs/$id/config.json"
	timeout 60 "$LLME" "$@" 2>&1 > >(tee "logs/$id/log.txt" > "$out")
	err=$?

	if [ "$err" -eq 124 ]; then
		result "TIMEOUT"
		return 124
	elif [ "$err" -ne 0 ]; then
		grep --color -i error "logs/$id/log.txt"
		result "ERROR"
		return $err
	fi

	return 0
}

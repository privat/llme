#!/bin/bash

# Common setup and useful functions for test scripts

set -e
SUITE=$(basename "$0" .sh)
TESTDIR=$(dirname "$0")

# The llme tool to check
LLME="llme"
if ! command -v "$LLME"; then
	echo "llme not found: $LLME" >&2
fi

# run before each test. override if needed
setup() {
	true
}

# run after each test. override if needed
teardown() {
	true
}

# copy files from data to the workdir
copy() {
	for f in "$@"; do
		cp -r "$TESTDIR/data/$f" "$WORKDIR/"
	done
}


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
	elif grep -i "$1" "logs/$id/log.txt"; then
		result "ALMOST"
	else
		result "FAIL"
	fi
}

# Run llme in its workdir with a fresh python environment
runllme() {
	(
	set -e
	cd "$WORKDIR"
	python -m venv venv
	. venv/bin/activate
	timeout 60 "$LLME" "$@"
)
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

	export ORIG_DIR=`pwd`
	export LLME_CHAT_OUTPUT=$ORIG_DIR/logs/$id/chat.json
	export LLME_BATCH=true
	export LLME_YOLO=true

	# create a tmp workdir
	WORKDIR=`mktemp --tmpdir -d llme-XXXXX`
	ln -s "$WORKDIR" "logs/$id/workdir"

	setup

	if [ -n "$R" ]; then
		out=/dev/null
	else
		out=/dev/stdout
	fi

	"$LLME" "$@" --dump-config > "logs/$id/config.json"
	runllme "$@" 2>&1 > >(tee "logs/$id/log.txt" > "$out")
	err=$?

	teardown

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

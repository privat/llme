#!/bin/bash

# Common setup and useful functions for test scripts

export SUITE=$(basename "$0" .sh)
export TESTDIR=$(dirname "$0")
export ORIGDIR=`pwd`
export UTILDATE=${UTILDATE:-`date +%s`} # so all runs from a same initial script share a same utildate

# The llme tool to check
LLME="llme"
if ! command -v "$LLME" >/dev/null; then
	echo "llme not found: $LLME" >&2
	exit 1
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
	config="$ORIGDIR/$LOGDIR/config.json"
	url=`jq -r .base_url "$config"`
	model=`jq -r .model "$config"`
	chat="$ORIGDIR/$LOGDIR/chat.json"
	if [ -f "$chat" ]; then
		msgs=`jq '.|length' "$chat"`
		words=`wc -w < "$chat"`
	else
		msgs=
		words=
	fi

	cat > "$ORIGDIR/$LOGDIR/result.json" <<-EOF
	{
		"result":"$1",
		"comment":"$2",
		"msgs":${msgs:-null},
		"words":${words:-null},
		"task":"$task",
		"suite":"$SUITE",
		"utildate":$UTILDATE,
		"date":`date +%s`,
		"path":"$LOGDIR",
		"git-version":"`git -C "$ORIGDIR/$TESTDIR" describe --tags --dirty`",
		"llme-version":"`"$LLME" --version`"
	}
	EOF
	case $1 in
		ERROR*|FAIL*|TIMEOUT*)
			color=91;;
		PASS*)
			color=92;;
		RUNNING*)
			color=94;;
		*)
			color=93;;
	esac
	echo -e "\e[${color}m$1\e[0m $2 $LOGDIR/ model=$model msgs=$msgs words=$words"
}

# Check that the llm result matches the pattern $1 on the last line.
answer() {
	if jq -r '.[-1].content' "$LOGDIR/chat.json" | sed '/^$/d' | tail -n1 | grep -x "$1"; then
		result "PASS"
	elif grep --color=always -i "$1" "$LOGDIR/log.txt" > >(head); then
		result "ALMOST"
	else
		result "FAIL"
	fi
}

# Check that the llm result talk about a pattern
smoke() {
	if grep --color=always -i "$1" "$LOGDIR/log.txt" > >(head); then
		result "PASS"
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
	setsid timeout -v -f -sINT 180 "$LLME" "$@"
)
}

# Run a test with the llme tool
# Usage: tllme taskname [llme args...] (use "$@" for args)
#
# define '$V' for verbose
# define '$F' to filter tests
# define '$KEEPWORKDIR' to reuse the workdir in subsequent tests
tllme() {
	task=$1
	shift

	if [ -n "$F" ] && ! echo "$task" | grep "$F"; then
		return 1
	fi

	cd "$ORIGDIR"

	# Tests results are stored in logs/$id/ where id is a unique identifier
	id=$SUITE-$task-$(date +%s)-$$
	export LOGDIR="logs/$id"
	mkdir -p "$LOGDIR"
	env | grep "^LLME_" > "$LOGDIR/env.txt"

	export LLME_CHAT_OUTPUT=$ORIGDIR/$LOGDIR/chat.json
	export LLME_BATCH=true
	export LLME_YOLO=true

	# create a tmp workdir
	if [ -z "$WORKDIR" ] || [ -z "$KEEPWORKDIR" ]; then
		WORKDIR=`mktemp --tmpdir -d llme-XXXXX`
	fi
	ln -s "$WORKDIR" "$LOGDIR/workdir"

	setup

	if [ -z "$V" ]; then
		out=/dev/null
	else
		out=/dev/stdout
	fi

	if ! "$LLME" "$@" --dump-config > "$LOGDIR/config.json"; then
		result "ERROR" "can't get config"
		return 1
	fi

	echo
	result "RUNNING"

	runllme "$@" 2> >(tee "$LOGDIR/err.txt" > "$out") > >(tee "$LOGDIR/log.txt" > "$out")
	err=$?

	teardown

	if [ "$err" -eq 124 ]; then
		result "TIMEOUT"
		return 124
	elif [ "$err" -ne 0 ]; then
		grep --color -i error "$LOGDIR/log.txt"
		result "ERROR"
		return $err
	fi

	return 0
}

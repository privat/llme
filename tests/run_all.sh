#!/bin/bash

# you are in for a threat!
. "$(dirname "$0")/utils.sh"

"$TESTDIR/smoketest.sh" "$@"
"$TESTDIR/smokeimages.sh" "$@"
"$TESTDIR/basic_answers.sh" "$@"
"$TESTDIR/patch_file.sh" "$@"
"$TESTDIR/hello.sh" "$@"

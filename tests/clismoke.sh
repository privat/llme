#!/bin/bash

. "$(dirname "$0")/utils.sh"

setup() {
	copy README.md chat.json chat.jsonl chat-fork.jsonl corrupt.jsonl AGENTS.md
}

t prompt01 llme --dummy hello world "$@" &&
	validate_chat system hello assistant world assistant

# Empty prompts are ignored. not POLA
t prompt02 llme --dummy '' "$@" &&
	validate_chat system

#flacky test :(
#t prompt03 llme --dummy README.md hello "$@" &&
#	validate_chat system '"hello".*README' assistant

t prompt04 llme --dummy hello README.md "$@" &&
	validate_chat system '"hello".*README' assistant

#flacky test :(
#et prompt05 llme --dummy .. hello "$@" &&
#	validate_err "Is a directory"

t prompt06 llme --dummy <<<hello world "$@" &&
	validate_chat system '"world".*filename' assistant

t prompt07 llme --dummy <<<hello "$@" &&
	validate_chat system hello assistant

#  -u, --base-url BASE_URL API base URL [base_url]
et url1 llme -u bad -m "" hello "$@" &&
	validate_err "Error getting models"

et url1b llme -u bad -m "bad" hello "$@" &&
	validate_err "Server error"

et url2 llme -u '' hello "$@" &&
	validate_err "base-url required"

# URL ignored in dummy mode
t url3 llme --dummy -u http://bad.example.com hello "$@" &&
	validate_chat system hello assistant

et url4 llme -u http:// -m "" hello "$@" &&
	validate_err "Error getting models"

et url4b llme -u http:// -m "bad" hello "$@" &&
	validate_err "Server error"

t url5 llme --dummy -u '' hello "$@" &&
	validate_chat system hello assistant

# URL ignored in dummy mode
t url6 llme --dummy -u http://google.com hello "$@" &&
	validate_chat system hello assistant
# B6 regression: --list-models with an unreachable server must fail cleanly (no traceback)
et url7 llme --no-session -u http://127.0.0.1:1/v1 -m foo --list-models --timeout-http 3 "$@" &&
	validate_err "Error getting models"

#  -m, --model MODEL     Model name [model]
# dummy ignore the model
t model1 llme --dummy -m bad hello "$@" &&
	validate_chat system hello assistant

t model2 llme --dummy -m '' hello "$@" &&
	validate_chat system hello assistant # Should chose a default model

#  --list-models         List available models then exit
t list-models1 llme --dummy --list-models &&
	smoke "Models of"

# /models       list available models
t s-models llme --dummy /models hello "$@" &&
	smoke "Models of" &&
	validate_chat system hello assistant

#  /shell CMD    run a shell command in the current environment (alias: !CMD)
t s-shell1 llme --dummy '/shell echo shell-output-xyz' hello "$@" &&
	smoke "shell-output-xyz" &&
	validate_chat system hello assistant
t s-shell2 llme --dummy '!echo bang-output-xyz' hello "$@" &&
	smoke "bang-output-xyz" &&
	validate_chat system hello assistant
t s-shell3 llme --dummy --box "env FOO=shell-output-xyz sh -c" '/shell echo XYZ$FOO' hello "$@" &&
	smoke "XYZshell-output-xyz" &&
	validate_chat system hello assistant

#  --api-key API_KEY     The API key [api_key]
t key1 llme --dummy --api-key SECRET_KEY hello "$@" &&
	validate_chat system hello assistant

t key2 llme --dummy --api-key '' hello "$@" &&
	validate_chat system hello assistant

#  -b, --batch           Run non-interactively. Implicit if stdin is not a tty [batch]
# batch+no prompts = stdin is big prompt
t batch1 llme --dummy -b "$@" <<<$'hello\nworld\n' &&
	validate_chat system 'hello.*world' assistant
# no batch+no prompts = stdin lines are prompts
t batch2 llme --dummy --no-batch "$@" <<<$'hello\nworld\n' &&
	validate_chat system hello assistant world assistant
# batch+prompts = stdin is data (batch3 is in clismokelive.sh: it needs a real
# LLM that will actually use a tool on the stdin data)
# no batch+prompts = stdin are more prompts
t batch4 llme --dummy --no-batch goodbye "$@" <<<$'hello\nworld\n' &&
	validate_chat system goodbye assistant hello assistant world assistant

#  -p, --plain           No colors or tty fanciness. Implicit if stdout is not a tty [plain]
t plain1 llme --dummy -p hello "$@" &&
	validate_chat system hello assistant
t plain2 llme --dummy --no-plain hello "$@" &&
	smoke $'\e\\[0m'

#  --bulk                Disable stream-mode. Not that useful but it helps debugging APIs [bulk]
t bulk1 llme --dummy --bulk hello "$@" &&
	validate_chat system hello assistant
# B20 regression: stream_options must not be sent in --bulk (stream=false) mode
t bulk2 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" --bulk --raw-request-dump tmp.json hello "$@" &&
	validate_with jq -e '.stream == false and (has("stream_options") | not)' "$WORKDIR/tmp.json"
# ... and must be sent in stream mode
t bulk3 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" --raw-request-dump tmp.json hello "$@" &&
	validate_with jq -e '.stream == true and .stream_options.include_usage == true' "$WORKDIR/tmp.json"

#  -o, --chat-output CHAT_OUTPUT Export the full raw conversation in json
t output1 llme --dummy -o tmp.json hello "$@" &&
	validate_with jq . "$WORKDIR/tmp.json"

t output2 llme --dummy -o tmp.json -o '' hello "$@" &&
	validate_with [ ! -f "$WORKDIR/tmp.json" ]

# flacky test
#et output3 llme -o .. hello "$@" &&
#	validate_err "Is a directory"

# /save FILE    save chat
t s-save1 llme --dummy hello '/save tmp.json' world '/save tmp2.json' "$@" &&
	validate_with jq . "$WORKDIR/tmp.json" &&
	validate_with jq . "$WORKDIR/tmp2.json"
t s-save2 llme --dummy '/save tmp3.json' hello "$@" &&
	validate_with jq . "$WORKDIR/tmp3.json"
et s-save3 llme --dummy '/save' hello "$@" &&
	validate_err "Missing filename"
et s-save4 llme --dummy '/save a/bad/file' hello "$@" &&
	validate_err "No such file"

# /export [FILE]   export the conversation in markdown (FILE optional, stdout if omitted)
t s-export1 llme --dummy hello '/export tmp.md' world "$@" &&
	validate_with grep -q '^## user' "$WORKDIR/tmp.md" &&
	validate_with grep -q '^## assistant' "$WORKDIR/tmp.md" &&
	validate_with grep -q "I'm assistant." "$WORKDIR/tmp.md" &&
	validate_chat system hello assistant world assistant
t s-export2 llme --dummy hello '/export' world "$@" &&
	smoke '^## user' "I'm assistant." &&
	validate_with [ ! -f "$WORKDIR/tmp.md" ] &&
	validate_chat system hello assistant world assistant
et s-export3 llme --dummy '/export a/bad/file' hello "$@" &&
	validate_err "No such file"
t s-export4 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcall-nocontent.jsonl" --yolo hello '/export tmp.md' "$@" &&
	validate_with grep -q 'Tool call' "$WORKDIR/tmp.md" &&
	validate_chat system hello assistant tool assistant

#  -i, --chat-input CHAT_INPUT Continue a previous (exported) conversation
t input1 llme --dummy -i chat.json world "$@" &&
	validate_chat system hello assistant world assistant
t input1b llme --dummy -i chat.jsonl world "$@" &&
	validate_chat system hello assistant world assistant

t input2 llme --dummy -i chat.json -i '' world "$@" &&
	validate_chat system world assistant

et input3 llme --dummy -i a/bad/file hello "$@" &&
	validate_err "No such file"
et input4 llme --dummy -i corrupt.jsonl hello "$@" &&
	validate_err "Can't load chat"
# /load FILE    load chat
# The session log is append-only: the loaded messages are added, not replacing.
t s-load1 llme --dummy hello2 '/load chat.json' world '/load chat.json' "$@" &&
	validate_log "0a system" "1a user: hello2" "2a assistant" "0b system: You are assistant." "1b user: hello" "2b assistant: I'm assistant." "3b user: world" "4b assistant" "0c system: You are assistant." "1c user: hello" "2c assistant: I'm assistant."
t s-load2 llme --dummy '/load chat.json' world "$@" &&
	validate_log "0a system" "0b system: You are assistant." "1b user: hello" "2b assistant: I'm assistant." "3b user: world" "4b assistant"
# A forked history (llme-meta parent links): the tree is restored as saved (1a and 1b are siblings) and the conversation resumes on the last branch.
t s-loadfork1 llme --dummy -i chat-fork.jsonl next "$@" &&
	validate_log "0a system" "1a user: haproxy" "1b user: exit" "2b assistant" "3b user: next" "4b assistant"
et s-load3 llme --dummy '/load' world "$@" &&
	validate_err "Missing filename"
et s-load4 llme --dummy '/load a/bad/file' hello "$@" &&
	validate_err "No such file"

#  --export-metrics EXPORT_METRICS Export metrics, usage, etc. in json
t export-metrics1 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" --export-metrics tmp.json hello "$@" &&
	validate_with jq . "$WORKDIR/tmp.json"
et export-metrics2 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" --export-metrics a/bad/file hello "$@" &&
	validate_err "No such file"
t export-metrics3 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" --export-metrics tmp.json --export-metrics '' hello "$@" &&
	validate_with [ ! -f "$WORKDIR/tmp.json" ] &&
	validate_chat system hello assistant
# /metrics      list current metrics
t s-metrics llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" /metrics hello /metrics "$@" &&
	smoke "message_n: 1" &&
	validate_chat system hello assistant

# /compact [PROMPT]  summarize the history and restart fresh, then process the given prompt
t s-compact1 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-compact.jsonl" hello /compact world "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a user:.*Summarize" "4a assistant.*SUMMARY-TEXT" "SUMMARY-TEXT" "1b user: world" "2b assistant"
t s-compact2 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-compact-empty.jsonl" hello /compact "$@" &&
	validate_err "did not compact"
# /compact with a next prompt: it is queued and processed right after the compaction
t s-compact3 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-compact.jsonl" hello "/compact world" "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a user:.*Summarize" "4a assistant.*SUMMARY-TEXT" "SUMMARY-TEXT" "1b user: world" "2b assistant"
# /compact with a next prompt, but the compaction fails: the prompt is NOT processed
t s-compact4 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-compact-empty.jsonl" hello "/compact world" "$@" &&
	validate_err "did not compact" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a user:.*Summarize" "4a assistant"
# B1 regression: --auto-compact (threshold not reached) must not hang the main loop
t auto-compact1 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.jsonl" --auto-compact 100000 hello world "$@" &&
	validate_chat system hello assistant world assistant
t auto-compact2 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-auto-compact.jsonl" --auto-compact 10 --compaction-prompt "summarize this" hello world "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a user:.*summarize this" "4a assistant.*summary" "summary" "1b user: world" "2b assistant"

#  -s, --system SYSTEM_PROMPT System prompt [system_prompt]
t system1 llme --dummy -s hello world "$@" &&
	validate_chat hello world assistant

t system2 llme --dummy -s '' hello "$@" &&
	validate_chat hello assistant

#  --temperature TEMPERATURE Temperature of predictions [temperature]
t temp1 llme --dummy --temperature 0 hello "$@" &&
	validate_chat system hello assistant

et temp2 llme --temperature '' hello "$@" &&
	validate_err 'invalid float value'

et temp3 llme --temperature bad hello "$@" &&
	validate_err 'invalid float value'

#  --tool-mode {markdown,native} How tools and functions are given to the LLM [tool_mode]
t tool-mode1 llme --dummy --tool-mode markdown hello "$@" &&
	validate_chat '```' hello assistant
t tool-mode2 llme --dummy --tool-mode native hello "$@" &&
	validate_chat system hello assistant # How to test this?
et tool-mode3 llme --tool-mode bad hello "$@" &&
	validate_err 'invalid choice'
et tool-mode4 llme --tool-mode '' hello "$@" &&
	validate_err 'invalid choice'

#  -c, --config CONFIG   Custom configuration files
t config1 llme --dummy -c "$ORIGDIR/$TESTDIR/data/config.toml" hello "$@" &&
	validate_chat 'You are assistant.' hello ''
et config2 llme -c bad hello "$@" &&
	validate_err "No such file"
et config3 llme -c '' hello "$@" &&
	validate_err "No such file"
et config4 llme -c chat.json hello "$@" &&
	validate_err "Invalid config file"
# B13 regression: boolean settings given as TOML integers (batch = 1)
t config5 llme --dummy -c "$ORIGDIR/$TESTDIR/data/config-boolint.toml" hello "$@" &&
	validate_chat system hello assistant
# B10 regression: append settings given as TOML lists (skills_path = [ ... ])
t config6 llme --dummy -c "$ORIGDIR/$TESTDIR/data/config-skillslist.toml" hello "$@" &&
	validate_chat system hello assistant

#  --list-tools          List available tools then exit
t list-tools1 llme --list-tools hello "$@" &&
	smoke "run_command"
# /tools        list available tools
t s-tools1 llme --dummy /tools hello "$@" &&
	smoke "run_command" &&
	validate_chat system hello assistant

#  --dump-config         Print the effective config and quit
t dump-config1 llme --dump-config hello "$@" &&
	smoke '"base_url"'
# /config       list configuration options
t s-config1 llme --dummy '/config' hello "$@" &&
	smoke 'base_url' &&
	validate_chat system hello assistant

#  --raw-response-dump FILE
#    Export the full json message response, one per line (jsonl) [raw_response_dump]
t raw-response-dump1 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" --raw-response-dump tmp.jsonl hello world "$@" &&
	validate_with jq -s -e 'length == 2' "$WORKDIR/tmp.jsonl" &&
	validate_with grep -q '"role": "assistant"' "$WORKDIR/tmp.jsonl"
et raw-response-dump2 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" --raw-response-dump a/bad/file hello "$@" &&
	validate_err "No such file"

#  --plugin PLUGINS      Add additional tool (python file or directory) [plugins]
t plugin1 llme --dummy --plugin "$ORIGDIR/$TESTDIR/../examples/weather_plugin.py" hello "$@" &&
	validate_chat system hello assistant
t plugin1b llme --list-tools --plugin "$ORIGDIR/$TESTDIR/../examples/weather_plugin.py" hello "$@" &&
	smoke 'weather(city: str)'
t plugin2 llme --dummy --plugin "$ORIGDIR/$TESTDIR/../examples" hello "$@" &&
	validate_chat system hello assistant
t plugin2b llme --list-tools --plugin "$ORIGDIR/$TESTDIR/../examples" hello "$@" &&
	smoke 'weather(city: str)'
# B3 regression: tools annotated with float/bool/list (json-schema types)
t plugin4 llme --list-tools --plugin "$ORIGDIR/$TESTDIR/data/plugin-types.py" hello "$@" &&
	smoke 'max_temp: float'
t plugin5 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" --raw-request-dump tmp.json --plugin "$ORIGDIR/$TESTDIR/data/plugin-types.py" hello "$@" &&
	validate_with jq -e '.tools[] | select(.function.name=="wx") | .function.parameters.properties | {city: .city.type, max_temp: .max_temp.type, verbose: .verbose.type, tags: .tags.type} == {city: "string", max_temp: "number", verbose: "boolean", tags: "array"}' "$WORKDIR/tmp.json"
et plugin3 llme --plugin bad hello "$@" &&
	validate_err "No such file"

#  -v, --verbose         Increase verbosity level (can be used multiple times)
t verbose1 llme --dummy -v hello "$@" &&
	validate_err "level set to INFO"
t verbose2 llme --dummy -vv hello "$@" &&
	validate_err "level set to DEBUG"
t verbose3 llme --dummy -vvv hello "$@" &&
	validate_err "level set to DEBUG"
t ss-verbose1 llme --dummy '/set verbose=1' hello "$@" &&
	validate_err "level set to INFO"
# B7 regression: /set verbose must not add a second console handler
t ss-verbose2 llme --dummy -v hello '/set verbose=2' "$@" &&
	validate_with [ "$(grep -c 'Log level set to DEBUG' "$LOGDIR/err.txt")" -eq 1 ]
# B17 regression: LLME_VERBOSE=3 was always interpreted as 1
t verbose4 env LLME_VERBOSE=3 llme --dump-config "$@" &&
	smoke '"verbose": 3'
et verbose5 env LLME_VERBOSE=bad llme --dump-config "$@" &&
	validate_err "Invalid value for verbose"

#  --log-file LOG_FILE   Write logs to a file [log_file]
t log-file1 llme --dummy --log-file tmp.log hello "$@" &&
	validate_with grep -q 'llme - DEBUG' "$WORKDIR/tmp.log"
et log-file2 llme --log-file a/bad/file hello "$@" &&
	validate_err "No such file"

#  -Y, --yolo            UNSAFE: Do not ask for confirmation before running tools. Combine with --batch to reach the singularity.
t yolo1 llme --dummy --yolo hello "$@" &&
	validate_chat system hello assistant

#  --version             Display version information and quit
t version1 llme --version hello "$@" &&
	smoke 'v[0-9]'

# --help
t help1 llme --help "$@" &&
	smoke "usage: llme"

# --dummy
t dummy1 llme --dummy hello "$@" &&
	validate_chat system hello "I'm assistant."
t dummy2 llme --dummy --list-models "$@" &&
	smoke dummy
t dummy3 llme --dummy hello "$@" &&
	validate_chat system hello "I'm assistant."

# --dummy-responses (mock the server responses from a file, no server needed)
t dummyres1 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" hello "$@" &&
	smoke "canned response"
t dummyres2 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcall.json" runit "$@" &&
	smoke "DUMMY_TOOL_RAN" "dummy tool ran successfully"
t dummyres3 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.jsonl" one two "$@" &&
	smoke "Jsonl response one" "Jsonl response two"
t dummyres4 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.jsonl" one two three "$@" &&
	smoke "Dummy response filler"

# undo, redo, pass with tool calls
t nav_tools0 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcalls.json" hello "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a tool:.*DUMMY_TOOL1_RAN" "4a tool:.*DUMMY_TOOL2_RAN" "5a assistant"
# /undo after a tool pauses before the next message: the tool result is NOT
# re-run (no interactive user to confirm, in batch the conversation just ends)
t nav_tools1 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcalls.json" hello /undo "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a tool:.*DUMMY_TOOL1_RAN" "4a tool:.*DUMMY_TOOL2_RAN" "5a assistant"
# ... but an explicit empty answer (enter) re-runs the tool, without re-running
# the assistant that called it: the assistant only sees the clean new result
t nav_tools6 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcall-error.jsonl" --yolo hello /undo "" "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a tool:.*Error during update_file" "4a assistant" "3b tool:.*Error during update_file" "4b assistant"
# a re-run of run_command always goes through the confirmation
t nav_tools7 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcalls.json" hello /undo "" "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a tool:.*DUMMY_TOOL1_RAN" "4a tool:.*DUMMY_TOOL2_RAN" "5a assistant" "4b tool:.*Confirmation unavailable in batch mode" "5b assistant"
# /undo after a tool, then a user message: inserted after the (kept) tool result
t nav_tools2 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcalls.json" hello /undo world "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a tool:.*DUMMY_TOOL1_RAN" "4a tool:.*DUMMY_TOOL2_RAN" "5a assistant" "5b user: world" "6b assistant"
# /undo then /pass: the /undo is cancelled, no fork
t nav_tools3 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcalls.json" hello /undo /pass "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a tool:.*DUMMY_TOOL1_RAN" "4a tool:.*DUMMY_TOOL2_RAN" "5a assistant"
# /undo then /redo: the assistant after the tool is regenerated, the tool is NOT re-run
t nav_tools4 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcalls.json" hello /undo /redo "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a tool:.*DUMMY_TOOL1_RAN" "4a tool:.*DUMMY_TOOL2_RAN" "5a assistant" "5b assistant"
# same, with a tool that has no confirmation mechanism (update_file)
t nav_tools5 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcall-error.jsonl" --yolo hello /undo world "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a tool:.*Error during update_file" "4a assistant" "4b user: world" "5b assistant"

# B18 regression: a tool call whose arguments are already a json object (not a string)
t tool-args1 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcall-dictargs.jsonl" --yolo hello "$@" &&
	smoke "DICT_ARGS_RAN" &&
	validate_chat system hello assistant tool assistant

# B5 regression: a tool error must not add the message twice (which reset the whole history)
t tool-err1 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcall-error.jsonl" --yolo --log-file tmp.log hello "$@" &&
	smoke "Error during update_file" &&
	validate_with [ "$(grep -c 'Reset [0-9]* messages' "$WORKDIR/tmp.log")" -eq 0 ]

# args
t args0 llme --dummy "$@" < /dev/null &&
	pass
# prefix
t args1 llme --dummy --verbo hello "$@" &&
	validate_err "level set to INFO"
et args2 llme --bad hello "$@" &&
	validate_err "unrecognized argument"
t args3 llme --dummy --no-version hello "$@" &&
	validate_chat system hello assistant
et s-set1 llme --dummy '/set bad=bad' hello "$@" &&
	validate_err "Unknown setting"
et s-set2 llme --dummy '/set bad' hello "$@" &&
	validate_err "Syntax error"
et s-set3 llme --dummy '/set' hello "$@" &&
	validate_err "Missing setting"
# an exact match must not be ambiguous (system_prompt vs system_prompt_template)
t s-set4 llme --dummy '/set system_prompt=foo' /clear hello "$@" &&
	validate_log '0a system' '0b system: foo' '1b user: hello' '2b assistant'
et s-set5 llme --dummy '/set system_p=foo' hello "$@" &&
	validate_err "Ambiguous setting"
# /set with suspicious values must fail cleanly (no traceback), an empty value unsets the option
t s-set6 llme --dummy '/set temperature=0.5' hello "$@" &&
	validate_chat system hello assistant
et s-set7 llme --dummy '/set plain=5' "$@" &&
	validate_err "Invalid value for plain: 5"
et s-set8 llme --dummy '/set temperature=abc' "$@" &&
	validate_err "Invalid value for temperature: abc"
et s-set9 llme --dummy '/set verbose=x' "$@" &&
	validate_err "Invalid value for verbose: x"
et s-set10 llme --dummy '/set tool_mode=foo' "$@" &&
	validate_err "Invalid value for tool_mode: foo"
et s-set11 llme --dummy '/set extra_body=[1,2' "$@" &&
	validate_err "Invalid value for extra_body"
t s-set12 llme --dummy '/set temperature=' /config "$@" &&
	validate_with grep -q "temperature: None" "$LOGDIR/out.txt"
# prefix
t slash1 llme --dummy /he hello "$@" &&
	smoke "list available models"
et slash2 llme --dummy /bad hello "$@" &&
	validate_err "Unknown slash command"
#et slash3 llme / hello "$@" &&
#	validate_err "Can't load" # / is the root directory

# /quit         exit the program
t s-quit llme --dummy /quit hello "$@" &&
	validate_chat system

# /help         show this help
t s-help llme --dummy /help hello "$@" &&
	smoke "list available models"

# /redo        cancel and regenerate the last assistant message
t s-redo1 llme --dummy hello /redo world /redo "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "2b assistant" "3b user: world" "4b assistant" "4c assistant"
t s-redo2 llme --dummy hello /redo /redo "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "2b assistant" "2c assistant"
et s-redo3 llme --dummy /redo hello "$@" &&
	validate_err "No assistant message to redo"

# /undo         cancel the last user message (and the response)
t s-undo1 llme --dummy hello /undo world /undo "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "1b user: world" "2b assistant"

et s-undo2 llme --dummy /undo hello "$@" &&
	validate_err "No user message to undo"
# B12 regression: /undo on the first user message (index 0, no system message)
t s-undo3 llme --dummy -s '' hello /undo "$@" &&
	validate_log "0a user: hello" "1a assistant"

# /pass         go forward in history (cancel /undo) [PageDown]
t s-pass1 llme --dummy hello /undo /pass world "$@" &&
	validate_chat system hello assistant world assistant
et s-pass2 llme --dummy /pass hello "$@" &&
	validate_err "Already at latest message"

# /goto M       jump after message M (e.g /goto 5c)
t s-goto00 llme --dummy hello world "/goto 0" goodbye "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a user: world" "4a assistant" "0b user: goodbye" "1b assistant"
t s-goto01 llme --dummy hello world "/goto 1" goodbye "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a user: world" "4a assistant" "1b user: goodbye" "2b assistant"
t s-goto02 llme --dummy hello world "/goto 2" goodbye "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a user: world" "4a assistant" "2b assistant" "3b user: goodbye" "4b assistant"
t s-goto03 llme --dummy hello world "/goto 3" goodbye "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a user: world" "4a assistant" "3b user: goodbye" "4b assistant"
t s-goto04 llme --dummy hello world "/goto 4" goodbye "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a user: world" "4a assistant" "4b assistant" "5b user: goodbye" "6b assistant"
t s-goto10 llme --dummy hello /undo world "/goto 2a" "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "1b user: world" "2b assistant" "2c assistant"
# /goto a tool message pauses (no re-run), the next prompt is inserted after
# the whole tool run (kept, so the conversation stays valid)
t s-goto11 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcalls.json" hello "/goto 3" world "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a tool:.*DUMMY_TOOL1_RAN" "4a tool:.*DUMMY_TOOL2_RAN" "5a assistant" "5b user: world" "6b assistant"
et s-goto12 llme --dummy hello /undo world "/goto" "$@" &&
	validate_err "Missing message label"
et s-goto13 llme --dummy hello /undo world "/goto bad" "$@" &&
	validate_err "Invalid message label"
et s-goto14 llme --dummy hello world "/goto 42" goodbye "$@" &&
	validate_err "Message 42 not found"

# /history      list condensed conversation history
t s-history1 llme --dummy hello /history "$@" &&
	smoke "1 user: hello" &&
	validate_chat system hello assistant

t s-history2 llme --dummy hello /undo world /history "$@" &&
	smoke "1 user: world" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "1b user: world" "2b assistant"

# B4 regression: a tool-calls-only assistant message without a "content" key
t s-history3 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcall-nocontent.jsonl" --yolo hello /history "$@" &&
	smoke "DUMMY_TOOL_RAN" &&
	validate_chat system hello assistant tool assistant
# paused on a tool: the (kept) tool result is listed, the assistant after it is not
t s-history4 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcalls.json" hello /undo /history "$@" &&
	smoke "4 tool:.*DUMMY_TOOL2_RAN" &&
	validate_with [ "$(grep -c '5 assistant:' "$LOGDIR/out.txt")" -eq 0 ] &&
	validate_log "0a system" "1a user: hello" "2a assistant" "3a tool:.*DUMMY_TOOL1_RAN" "4a tool:.*DUMMY_TOOL2_RAN" "5a assistant"

# /full-history list hierarchical conversation history (with forks)
t s-full-history1 llme --dummy hello /full-history "$@" &&
	smoke "1a user: hello" &&
	validate_chat system hello assistant

t s-full-history2 llme --dummy hello /undo world /full-history "$@" &&
	smoke "1a user: hello" "1b user: world" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "1b user: world" "2b assistant"

# /edit         run EDITOR on the chat (save,editor,load)
export EDITOR="sed -i 's/hello/world/'"
t s-edit1 llme --dummy hello /edit hello "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "1b user: world" "2b assistant" "3b user: hello" "4b assistant"
export EDITOR="sed -i 's/hello/world/'"
t s-edit2 llme --dummy --system=hello /edit hello2 "$@" &&
	validate_log "0a system: hello" "0b system: world" "1b user: hello2" "2b assistant"
export EDITOR="false"
et s-edit3 llme --dummy /edit hello "$@" &&
	validate_err "returned non-zero exit"
export EDITOR="/bad/name"
et s-edit4 llme --dummy hello /edit "$@" &&
	validate_err "No such file"
export EDITOR="echo 'badquote"
et s-edit5 llme --dummy hello /edit "$@" &&
	validate_err "Invalid editor command"

#  --system-prompt-template TEMPLATE  System prompt Jinja2 template [system_prompt_template]
#  --dump-system-prompt               Print the rendered system prompt and quit
t tpl1 llme --dummy -s "you are a robot" --system-prompt-template 'BASE: {{ system_prompt }}' --dump-system-prompt "$@" &&
	smoke "BASE: you are a robot"
t tpl2 llme --dummy -s "you are a robot" --system-prompt-template 'BASE: {{ system_prompt }}' hello "$@" &&
	validate_chat "BASE: you are a robot" hello assistant
t tpl3 llme --dummy -s "you are a robot" --system-prompt-template 'ONLY-TEMPLATE' hello "$@" &&
	validate_chat 'ONLY-TEMPLATE' hello assistant
t tpl4 llme --dummy -s "you are a robot" --system-prompt-template '' hello "$@" &&
	validate_chat "you are a robot" hello assistant
t tpl5 llme --dummy --tool-mode markdown hello "$@" &&
	validate_chat "run cat file.txt" "user" "assistant"
t tpl6 llme --dummy --skills-path "$ORIGDIR/$TESTDIR/data/skills" --system-prompt-template '{% for skill in skills %}SKILL: {{ skill.name }} - {{ skill.desc }} {% endfor %}' hello "$@" &&
	validate_chat "SKILL: smoke-skill" "user" "assistant"
et tpl7 llme --dummy --system-prompt-template '{{ nope }}' --dump-system-prompt "$@" &&
	validate_err "template error"
et tpl8 llme --dummy --system-prompt-template '{% if %}' --dump-system-prompt "$@" &&
	validate_err "template error"
t tpl9 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-compact.jsonl" --system-prompt-template 'SUMMARY: {{ compaction_summary }}' hello /compact "$@" &&

	validate_chat "SUMMARY: None" "hello" "assistant" "user" "SUMMARY-TEXT" "SUMMARY: SUMMARY-TEXT"

t agents1 llme --dummy --dump-system-prompt "$@" &&
	smoke "DUMMY-AGENTS-MD"
t agents2 llme --dummy --no-agents-md --dump-system-prompt "$@" &&
	validate_with [ -z "$(grep "DUMMY-AGENTS-MD" "$LOGDIR/out.txt")" ]
t agents3 sh -c 'rm AGENTS.md && llme --dummy --dump-system-prompt "$@"' sh "$@" &&
	validate_with [ -z "$(grep "DUMMY-AGENTS-MD" "$LOGDIR/out.txt")" ]
t agents4 llme --dummy hello "$@" &&
	validate_chat "DUMMY-AGENTS-MD" hello assistant
t agents5 sh -c 'mkdir sub && cd sub && llme --dummy --dump-system-prompt "$@"' sh "$@" &&
	smoke "DUMMY-AGENTS-MD"

# a corrupted session file (e.g. llme killed mid-write, or
# a line without role) must give a clean error WITHOUT losing data: the
# reload used to truncate and rewrite the session file as it re-added
# the messages, so the failure point became the new (shorter) end of file.
et corrupt-resume sh -c '
    unset LLME_CHAT_OUTPUT
    mkdir -p s1
    llme --dummy -s SP --session s1 hello hello2 || exit 1
    sed -i "3s/.*/{\"content\":\"no role\"}/" s1/chat.jsonl
    llme --dummy -s SP --session s1 world
' "$@" &&
	validate_err "Can.t load chat" &&
	validate_with [ "$(grep -c . "$WORKDIR/s1/chat.jsonl")" -eq 5 ]

# /edit must not resurrect the messages cancelled by
# /undo: the chat is reloaded from the visible prefix (up to the
# message_index), so the next prompt forks from the position, not from
# the cancelled assistant message
export EDITOR=true
t edit-undo llme --dummy -s SP hello /undo /edit hello2 "$@" &&
	validate_log "0a system" "1a user: hello" "2a assistant" "1b user: hello2" "2b assistant"

# update_file must count insertions/deletions in the
# replaced region only (1 line -> 2 lines = 2 insertions, 1 deletion),
# not against the whole new file
t updatefile sh -c '
    printf "alpha\nbeta\ngamma\n" > f.txt
    llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-updatefile.jsonl" --yolo hello
' "$@" &&
	smoke "f.txt: 2 insertions(+), 1 deletions(-)" &&
	validate_with grep -qx "BETA2" "$WORKDIR/f.txt"

# with a box, image_description must look for the file
# through the box, not locally. box-emptydir.sh runs commands in an empty
# directory: img.jpg exists locally but not "in the box", so the tool must
# answer "not found" (a string), not return the local image part (a list
# of content parts).
t imagebox sh -c '
    cp "$ORIGDIR/$TESTDIR/data/image.jpg" img.jpg
    llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-imagedesc.jsonl" --yolo --box "sh $ORIGDIR/$TESTDIR/data/box-emptydir.sh" hello
' "$@" &&
	validate_with jq -se '[.[] | select(.role == "tool")][0].content | type == "string" and contains("not found")' "$LOGDIR/chat.jsonl"

# the --model completion (argcomplete) must work
t modelcompleter sh -c '
    COMP_LINE="llme --dummy --model " COMP_POINT=21 _ARGCOMPLETE=1 _ARGCOMPLETE_SHELL=bash llme 8>&1
' "$@" &&
	smoke dummy

# a broken --box must give a clean error, not a traceback
et box-broken llme --dummy -s hi --box nonexistent-cmd hello "$@" &&
	validate_err "Box command failed"

# a single malformed SKILL.md (unclosed frontmatter) must
# not crash llme at startup; it is skipped with a warning naming the file
t badskill sh -c '
    mkdir -p badskills/bad-skill
    printf -- "---\nname: bad-skill\ndescription: unclosed frontmatter\n" > badskills/bad-skill/SKILL.md
    llme --dummy --no-agents-md --skills-path badskills hello
' "$@" &&
	validate_err "Failed to parse frontmatter in.*badskills" &&
	validate_chat system hello assistant

# an unknown role (e.g. OpenAI 'developer') must not crash
# /history (KeyError on the colors dict)
t devrole sh -c '
    printf "{\"role\": \"developer\", \"content\": \"dev msg\"}\n" > dev.jsonl
    llme --dummy -s sys "/load dev.jsonl" /history
' "$@" &&
	smoke "developer: dev msg"

# with message_index = 0 (/goto 0), 0 is falsy: /undo must
# say "nothing to undo" instead of undoing the first user message
et undo-at-0 llme --dummy hello "/goto 0" /undo "$@" &&
	validate_err "No user message to undo"
# and /history must not display messages after the index
t history-at-0 llme --dummy hello world "/goto 0" /history "$@" &&
	validate_with [ -z "$(grep 'user: hello' "$LOGDIR/out.txt")" ]

# every result.json must be valid json with a numeric start date (START_DATE
# is set in prepare() for every test type, not only tllme)
t resultjson llme --dummy hello "$@" &&
	validate_chat system hello assistant &&
	validate_with jq -e '.start | type == "number"' "$LOGDIR/result.json"

exit "$errorcode"

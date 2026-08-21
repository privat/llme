#!/bin/bash

. "$(dirname "$0")/utils.sh"

setup() {
	copy README.md chat.json
}

t prompt01 llme --dummy hello world "$@" &&
	validate_chat system hello assistant world assistant

# Empty prompts are ignored. not POLA
t prompt02 llme --dummy '' "$@" &&
	validate_chat system

t prompt03 llme README.md hello "$@" &&
	validate_chat system '"hello".*README' assistant tool assistant

t prompt04 llme hello README.md "$@" &&
	validate_chat system '"hello".*README' assistant tool assistant

et prompt05 llme /etc/shadow hello "$@" &&
	validate_err "Permission denied"

t prompt06 llme <<<hello world "$@" &&
	validate_chat system '"world".*filename' assistant tool assistant

t prompt07 llme --dummy <<<hello "$@" &&
	validate_chat system hello assistant

#  -u, --base-url BASE_URL API base URL [base_url]
et url1 llme -u bad hello "$@" &&
	validate_err "Invalid URL"

et url2 llme -u '' hello "$@" &&
	validate_err "base-url required"

et url3 llme -u http://bad.example.com hello "$@" &&
	validate_err "Failed to resolve"

et url4 llme -u http:// hello "$@" &&
	validate_err "Invalid URL"

et url5 llme -u http://localhost:1 hello "$@" &&
	validate_err "Connection refused"

et url6 llme -u http://google.com hello "$@" &&
	validate_err "404"
et ss-url1 llme '/set base_url=bad' hello "$@" &&
	validate_err "Invalid URL"

#  -m, --model MODEL     Model name [model]
et model1 llme -m bad hello "$@" &&
	validate_err "ERROR" # unfortunately, servers can react differently to this error

t model2 llme --dummy -m '' hello "$@" &&
	validate_chat system hello assistant # Should chose a default model

#  --list-models         List available models then exit
t list-models1 llme --list-models &&
	smoke "Models of"
# /models       list available models
t s-models llme /models hello "$@" &&
	smoke "Models of" &&
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
t batch2 llme --no-batch "$@" <<<$'hello\nworld\n' &&
	validate_chat system hello assistant world assistant
# batch+prompts = stdin is data
t batch3 llme -b goodbye "$@" <<<$'hello\nworld\n' &&
	validate_chat system "goodbye.*file" assistant tool assistant
# no batch+prompts = stdin are more prompts
t batch4 llme --no-batch goodbye "$@" <<<$'hello\nworld\n' &&
	validate_chat system goodbye assistant hello assistant world assistant

#  -p, --plain           No colors or tty fanciness. Implicit if stdout is not a tty [plain]
t plain1 llme --dummy -p hello "$@" &&
	validate_chat system hello assistant
t plain2 llme --dummy --no-plain hello "$@" &&
	smoke $'\e\\[0m'

#  --bulk                Disable stream-mode. Not that useful but it helps debugging APIs [bulk]
t bulk1 llme --dummy --bulk hello "$@" &&
	validate_chat system hello assistant

#  -o, --chat-output CHAT_OUTPUT Export the full raw conversation in json
t output1 llme --dummy -o tmp.json hello "$@" &&
	validate_with jq . "$WORKDIR/tmp.json"

t output2 llme --dummy -o tmp.json -o '' hello "$@" &&
	validate_with [ ! -f "$WORKDIR/tmp.json" ]

et output3 llme -o /bad/file hello "$@" &&
	validate_err "No such file"

# /save FILE    save chat
t s-save1 llme --dummy hello '/save tmp.json' world '/save tmp2.json' "$@" &&
	validate_with jq . "$WORKDIR/tmp.json" &&
	validate_with jq . "$WORKDIR/tmp2.json"
t s-save2 llme --dummy '/save tmp3.json' hello "$@" &&
	validate_with jq . "$WORKDIR/tmp3.json"
et s-save3 llme --dummy '/save' hello "$@" &&
	validate_err "Missing filename"
et s-save4 llme --dummy '/save /bad/file' hello "$@" &&
	validate_err "No such file"

#  -i, --chat-input CHAT_INPUT Continue a previous (exported) conversation
t input1 llme --dummy -i chat.json world "$@" &&
	validate_chat system hello assistant world assistant

t input2 llme --dummy -i chat.json -i '' world "$@" &&
	validate_chat system world assistant

et input3 llme --dummy -i /bad/file hello "$@" &&
	validate_err "No such file"
# /load FILE    load chat
# The session log is append-only: the loaded messages are added, not replacing.
t s-load1 llme --dummy hello2 '/load chat.json' world '/load chat.json' "$@" &&
	validate_log "0a system" "1a user: hello2" "2a assistant" "0b system: You are assistant." "1b user: hello" "2b assistant: I'm assistant." "3b user: world" "4b assistant" "0c system: You are assistant." "1c user: hello" "2c assistant: I'm assistant."
t s-load2 llme --dummy '/load chat.json' world "$@" &&
	validate_log "0a system" "0b system: You are assistant." "1b user: hello" "2b assistant: I'm assistant." "3b user: world" "4b assistant"
et s-load3 llme --dummy '/load' world "$@" &&
	validate_err "Missing filename"
et s-load4 llme --dummy '/load /bad/file' hello "$@" &&
	validate_err "No such file"

#  --export-metrics EXPORT_METRICS Export metrics, usage, etc. in json
t export-metrics1 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" --export-metrics tmp.json hello "$@" &&
	validate_with jq . "$WORKDIR/tmp.json"
et export-metrics2 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" --export-metrics /bad/file hello "$@" &&
	validate_err "No such file"
t export-metrics3 llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" --export-metrics tmp.json --export-metrics '' hello "$@" &&
	validate_with [ ! -f "$WORKDIR/tmp.json" ] &&
	validate_chat system hello assistant
# /metrics      list current metrics
t s-metrics llme --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" /metrics hello /metrics "$@" &&
	smoke "message_n: 1" &&
	validate_chat system hello assistant

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

#  --list-tools          List available tools then exit
t list-tools1 llme --list-tools hello "$@" &&
	smoke "run_command"
# /tools        list available tools
t s-tools1 llme --dummy /tools hello "$@" &&
	smoke "run_command" &&
	validate_chat system hello assistant

#  --dump-config         Print the effective config and quit
t dump-config1 llme --dump-config hello "$@" &&
	smoke '"dump_config": true'
# /config       list configuration options
t s-config1 llme --dummy '/config' hello "$@" &&
	smoke 'base_url' &&
	validate_chat system hello assistant

#  --plugin PLUGINS      Add additional tool (python file or directory) [plugins]
t plugin1 llme --dummy --plugin "$ORIGDIR/$TESTDIR/../examples/weather_plugin.py" hello "$@" &&
	validate_chat system hello assistant
t plugin1b llme --list-tools --plugin "$ORIGDIR/$TESTDIR/../examples/weather_plugin.py" hello "$@" &&
	smoke 'weather(city: str)'
t plugin2 llme --dummy --plugin "$ORIGDIR/$TESTDIR/../examples" hello "$@" &&
	validate_chat system hello assistant
t plugin2b llme --list-tools --plugin "$ORIGDIR/$TESTDIR/../examples" hello "$@" &&
	smoke 'weather(city: str)'
et plugin3 llme --plugin bad hello "$@" &&
	validate_err "No such file"

#  -v, --verbose         Increase verbosity level (can be used multiple times)
t verbose1 llme --dummy -v hello "$@" &&
	validate_err "level set to INFO"
t verbose2 llme --dummy -vv hello "$@" &&
	validate_err "level set to DEBUG"
t verbose3 llme --dummy -vvv hello "$@" &&
	validate_err "level set to DEBUG"
t ss-verbose1 llme --dummy '/set verbose=1' hello "$@"

#  --log-file LOG_FILE   Write logs to a file [log_file]
t log-file1 llme --dummy --log-file tmp.log hello "$@" &&
	validate_with grep -q 'llme - DEBUG' "$WORKDIR/tmp.log"
et log-file2 llme --log-file /bad/file hello "$@" &&
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
t dummy3 llme -u bad --dummy hello "$@" &&
	validate_chat system hello "I'm assistant."

# --dummy-responses (mock the server responses from a file, no server needed)
t dummyres1 llme -u bad -m m --no-session --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.json" hello "$@" &&
	smoke "canned response"
t dummyres2 llme -u bad -m m --no-session -Y --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses-toolcall.json" runit "$@" &&
	smoke "DUMMY_TOOL_RAN" "dummy tool ran successfully"
t dummyres3 llme -u bad -m m --no-session --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.jsonl" one two "$@" &&
	smoke "Jsonl response one" "Jsonl response two"
et dummyres4 llme -u bad -m m --no-session --dummy-responses "$ORIGDIR/$TESTDIR/data/dummy-responses.jsonl" one two three "$@" &&
	validate_err "No more dummy responses"

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
# prefix
t slash1 llme --dummy /he hello "$@" &&
	smoke "list available models"
et slash2 llme --dummy /bad hello "$@" &&
	validate_err "Unknown slash command"
et slash3 llme / hello "$@" &&
	validate_err "Is a directory" # / is the root directory

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
	validate_log "0a system" "1a user: hello" "2a assistant" "1b user: world" "2b assistant" "2c assistant" "3c user: hello" "4c assistant"
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

exit "$errorcode"

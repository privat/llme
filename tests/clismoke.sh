#!/bin/bash

# We just run things that should not fail (or not not fail)
set -xe

exec </dev/null

llme hello world "$@"
llme hello world --bulk "$@"
llme <<<hello world "$@"
llme <<<hello "$@"
llme -v -v --dump-config "$@" > dumpconfig.txt

llme README.md hello "$@"
llme hello README.md "$@"
llme /etc/shadow hello "$@"

#  -u, --base-url BASE_URL API base URL [base_url]
! llme -u bad hello "$@"
! llme -u '' hello "$@"
! llme -u http://bad hello "$@"
! llme -u http:// hello "$@"

#  -m, --model MODEL     Model name [model]
! llme -m bad hello "$@"
! llme -m '' hello "$@"

#  --list-models         List available models then exit
llme --list-models

#  --api-key API_KEY     The API key [api_key]
llme --api-key SECRET_KEY hello "$@"
llme --api-key '' hello "$@"

#  -p, --plain           No colors or tty fanciness. Implicit if stdout is not a tty [plain]
llme -p hello "$@"

#  --bulk                Disable stream-mode. Not that useful but it helps debugging APIs [bulk]
llme --bulh hello "$@"

#  -o, --chat-output CHAT_OUTPUT Export the full raw conversation in json
llme -o tmp.json hello "$@"
llme -o '' hello "$@"
! llme -o /bad/file hello "$@"

#  -i, --chat-input CHAT_INPUT Continue a previous (exported) conversation
llme -i tmp.json hello "$@"
llme -i '' hello "$@"
! llme -i /bad/file hello "$@"

#  --export-metrics EXPORT_METRICS Export metrics, usage, etc. in json
llme --export-metrics tmp.json hello "$@"
llme --export-metrics /bad/file hello "$@"
llme --export-metrics '' hello "$@"

#  -s, --system SYSTEM_PROMPT System prompt [system_prompt]
llme -s hello 'word' "$@"
llme -s '' 'word' "$@"

#  --temperature TEMPERATURE Temperature of predictions [temperature]
llme --temperature 0 hello "$@"
llme --temperature '' hello "$@"
llme --temperature bad hello "$@"

#  --tool-mode {markdown,native} How tools and functions are given to the LLM [tool_mode]
llme --tool-mode marksown hello "$@"
llme --tool-mode native hello "$@"
llme --tool-mode bad hello "$@"
llme --tool-mode '' hello "$@"

#  -c, --config CONFIG   Custom configuration files
llme -c llme/config.toml
! llme -c bad hello "$@"
llme -c '' hello "$@"

#  --list-tools          List available tools then exit
llme --list-tools hello "$@"

#  --dump-config         Print the effective config and quit
llme --dump-config hello "$@"

#  --plugin PLUGINS      Add additional tool (python file or directory) [plugins]
llme --plugin examples/weather_plugin.py hello "$@"
llme --plugin examples hello "$@"
llme --plugin bad hello "$@"

#  -v, --verbose         Increase verbosity level (can be used multiple times)
llme -v hello "$@"
llme -vv hello "$@"
llme -vvv hello "$@"

#  -Y, --yolo            UNSAFE: Do not ask for confirmation before running tools. Combine with --batch to reach the singularity.
llme --yolo hello "$@"

#  --version             Display version information and quit
llme --version hello "$@"

# prefix
llme --verbo hello "$@"
! llme --bad hello "$@"

# /models       list available models
llme /models hello "$@"

# /tools        list available tools
llme /tools hello "$@"

# /metrics      list current metrics
llme /metrics hello /metrics "$@"

# /retry        cancel and regenerate the last assistant message
llme hello /retry world /retry "$@"
llme hello /retry /retry "$@"
llme /retry hello "$@"

# /undo         cancel the last user message (and the response)
llme hello /undo world /undo "$@"
llme /undo hello "$@"

# /edit         run EDITOR on the chat (save,editor,load)
export EDITOR=wc
llme hello /edit world /edit "$@"
llme /edit hello "$@"

# /save FILE    save chat
llme hello '/save tmp.json' world '/save tmp2.json' "$@"
llme '/save tmp3.json' hello "$@"
llme '/save' hello "$@"
llme '/save /bad/file' hello "$@"

# /load FILE    load chat
llme hello '/load tmp.json' world '/load tmp2.json' "$@"
llme '/load tmp3.json' hello "$@"
llme '/load' hello "$@"
llme '/load /bad/file' hello "$@"

# /config       list configuration options
llme '/config' hello "$@"

# /set OPT=VAL  change a config option
llme '/set verbose=1' hello "$@"
llme '/set base_url=bad' hello "$@"
llme '/set bad=bad' hello "$@"
llme '/set bad' hello "$@"
llme '/set' hello "$@"

# /quit         exit the program
llme '/quit' hello "$@"

# /help         show this help
llme '/help' hello "$@"

# prefix
llme /he hello "$@"
!llme /bad hello "$@"
!llme / hello "$@"

echo "SUCCESS"

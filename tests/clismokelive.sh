#!/bin/bash
# Smoke tests that really need a live LLM server (the base_url from the config).
# Everything else is server-free and in clismoke.sh (run by the CI).

. "$(dirname "$0")/utils.sh"

# copy the data files needed by the tests to the workdir
setup() {
	copy README.md chat.json
}

#  -u, --base-url BASE_URL API base URL [base_url]
et url3 llme -u http://bad.example.com hello "$@" &&
	validate_err "Failed to resolve"

et url6 llme -u http://google.com hello "$@" &&
	validate_err "404"

#  -m, --model MODEL     Model name [model]
et model1 llme -m bad hello "$@" &&
	validate_err "ERROR" # unfortunately, servers can react differently to this error

#  --list-models         List available models then exit
t list-models1 llme --list-models &&
	smoke "Models of"
# /models       list available models
t s-models llme /models hello "$@" &&
	smoke "Models of" &&
	validate_chat system hello assistant

exit "$errorcode"

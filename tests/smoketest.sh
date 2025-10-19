#!/bin/bash

. "$(dirname "$0")/utils.sh"

setup() {
	copy README.md
}

tllme "01" "What is the capital of France?" "$@" &&
	result LIVED
tllme "02" "What is the capital of France?" "What about Canada?" "And Vatican?" "And Mordor?" "And my axe?" "$@" &&
	result LIVED
tllme "03" "What the content on the current directory?" "$@" &&
	result LIVED
tllme "04" "What is the current operating system?" "$@" &&
	result LIVED
tllme "05" "What is the factorial of 153?" "$@" &&
	result LIVED
tllme "06" <<<"What is the capital of France?" "$@" &&
	result LIVED

tllme "10" "Summarize the file README.md in one sentence" "$@" &&
	result LIVED
tllme "11" "Summarize the file in one sentence" "$@" < "$TESTDIR/data/README.md" &&
	result LIVED
tllme "12" README.md "Summarize the file in one sentence" "$@" &&
	result LIVED
tllme "13" "Summarize the file in one sentence" "$@" README.md &&
	result LIVED

tllme "31" bonjour "exécute la commande uptime" "calcule la factorielle de 10" "résume en 10 (dix) mots le fichier" README.md "$@" &&
	result LIVED

tllme "32" -o "`pwd`/tmp.json" "Tell me a joke about LLMs" "$@" &&
	result LIVED
tllme "33" -i "`pwd`/tmp.json" "What is the joke about?" "$@" &&
	result LIVED

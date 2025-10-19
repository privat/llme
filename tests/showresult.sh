#!/bin/bash
dir=${1:-logs}
pass=${2:-"PASS"}
echo models:
cat "$dir"/*/result.csv | cut -d, -f 4,5 | sort | uniq -c | sort -n | grep "$pass"
echo "test:"
cat "$dir"/*/result.csv | cut -d, -f 1,2,5 | sort | uniq -c | sort -n | grep "$pass"

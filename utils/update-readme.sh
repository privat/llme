#!/bin/bash

set -e
{
sed -n '1,/^<!--help-->$/p' README.md
echo '```console'
echo '$ llme --help'
llme --help
echo '```'
sed -n '/^<!--\/help-->$/,/^<!--slash-help-->$/p' README.md
echo '```console'
echo '$ llme /help /quit'
llme /help /quit
echo '```'
sed -n '/^<!--\/slash-help-->$/,$p' README.md
} > README.new.md
mv README.new.md README.md

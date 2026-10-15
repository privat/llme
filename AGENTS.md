llme a TUI openai API compatible harness

Project organization

* `llme/*.py` source files. keep then short and KISS
* `bin/llme` run the local version (beware as llme in PATH is not necessarily the local one)
* `tests/clismoke.sh` black-box serverless tests. Other scripts require a live server and are more about benchmarking models than testing the harness anyway.
* `*.md` do not edit them unless explicitly asked

Some directives

* small diffs are preferred
* commit when task done
* add new black-box tests when feasible
* doc&comments: avoid line breaks mid sentence

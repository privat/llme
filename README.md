# llme, a CLI assitant for OpenAI-compatible chat servers

A simple, single-file command-line chat client compatible with the OpenAI API.

*(or "I just want to quickly test my model hosted with llama.cpp but don't want to spin up openwebui")*


## Features

- **OpenAI API Compatible:** Works with any self-hosted LLM platform that supports OpenAI chat completions API.
- **Extremely simple:** Single file, no installation needed.
- **Command-line interface:** Run it from the terminal.
- **Tools included:** Ask it to act on your file system and edit files (yolo).


## Installation

Chose your preferred installation method:

```bash
pipx install llme-cli # Might be stale
```

```bash
pipx install -e . # In the repo directory
```

```bash
./llme/main.py # directly (it should also work)
```


## Usage

### Run an interactive chat session

```bash
llme --base-url "http://localhost:18181/v1" --model "NexaAI/qwen3vl-8B-Thinking-4bit-mlx"`
```

* Ctrl-C to interrupt a response (or exit).


### Setup a config (optional, but recommended):

Edit `~/.config/llme/config.toml`
Look at [config.toml](llme/config.toml) for an example.
More about options and configs bellow

I assume, from now, that there is a config file...


### Run one-shots queries

Each prompt is run in order in the same chat session.

```bash
llme "What is the capital of France?" "What the content on the current directory?" "What is the current operating system?" "What is the factorial of 153?" "What is the weather at Tokyo right now?"
```

You can also pipe the query:

```bash
echo "What is the capital of France?" | llme
```


### Tools included

The LLM has a direct access to your shell (and files) and a python interpreter.
The user is asked for confirmation before executing any command.
Beware, some LLMs might be very **persistent** and **persuasive** in running **dangerous** commands. Do **not trust** the LLM blindly!

If you chose to not execute a command, it will be skipped, and you can provide a explanation to the LLM or asks for a better command.

Some LLM might insist on not using a tool, asking the user to do it manually, or just simulate the action.
A better prompt engineering might help.
Proposal to also improve the default system prompt is welcome.


### Inspect content of files or stdin

```bash
ps aux | llme "Which process consumes the most memory?"
```

you can also use file paths as assets to a prompt:

```bash
llme "how many regular users and regular groups are there in these files?" /etc/passwd /etc/group
```

Note: the file content and the path will be given to the LLM.


### Inspect images (for multimodal models)

Same as for files, but with images — duh, images are files!

```bash
llme "What is in this image?" < image.png
```

you can still use paths:

```bash
llme "What is in this image?" image.png
```


### Run yolo

Note: no warranty, yada yada, etc.
llme can just **kill** your **OS** and **cats**.
Do not run the following command without understanding what it does.

```bash
sudo llme --yolo "Distupgrade the system. You are root! Do as you wish."`
```


### Options (and config)

```bash
$ llme --help
usage: llme [-h] [-u BASE_URL] [-m MODEL] [--api-key API_KEY] [-q] [-s SYSTEM_PROMPT] [-c CONFIG] [-v] [-Y] [prompts ...]

OpenAI-compatible chat CLI.

positional arguments:
  prompts               Sequence of prompts

options:
  -h, --help            show this help message and exit
  -u, --base-url BASE_URL
                        API base URL [base_url]
  -m, --model MODEL     Model name [model]
  --api-key API_KEY     The API key, optionnal [api_key]
  -q, --quit            Quit after processed all arguments prompts [quit]
  -s, --system SYSTEM_PROMPT
                        System prompt [system_prompt]
  -c, --config CONFIG   Custom configuration file
  -v, --verbose         Increase verbosity level (can be used multiple times)
  -Y, --yolo            UNSAFE: Do not ask for confirmation before running tools
```

All options can be set in the config file (with the name in brackets, e.g. `base_url` for `--base-url`).
An option in the command line overrides the one in the `--config` file, that overrides the one in user configuration file (`~/.config/llme/config.toml`), that overrides the one in the system config file (in the package).


Note: Run a fresh `--help` in case I forgot to update this README.


## Development

I do not like Python, nor LLMs, but I needed something simple to test things quickly and play around.
My goal is to keep this simple and minimal: it should fits into a single file and still be manageable.

PR are welcome!


## Issues

* The various openai compatible servers implement different subsets.
* Models are really sensitive to prompts and system prompts, but you can create a custom config file for each.
* Models are really sensitive to how the messages are structured, unfortunately that is currenltly hardcoded in the program.


## Thanks

* [openwebui](https://github.com/open-webui/open-webui) for an inspiration, but too complex and web oriented.
* [gptme](https://github.com/gptme/gptme) for an other inspiration, but also too complex and targets too much non local LLM.
* [openai-cli](https://github.com/doryiii/openai-cli) for a simpler approach I built on top of.
* [llama.cpp](https://github.com/ggerganov/llama.cpp), [nexa-sdk](https://github.com/NexaAI/nexa-sdk/) and others for your great work.


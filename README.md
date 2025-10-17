# llme, a CLI assistant for OpenAI-compatible chat servers

A simple, single-file command-line chat client compatible with the OpenAI API.

*(or "I just want to quickly test my model hosted with llama.cpp but don't want to spin up openwebui")*


## Features

- **OpenAI API Compatible:** Works with any self-hosted LLM platform that supports OpenAI chat completions API.
- **Extremely simple:** Single file, no installation required.
- **Command-line interface:** Run it from the terminal.
- **Tools included:** Ask it to act on your file system and edit files (yolo).


## Installation

Chose your preferred installation or execution method:

```bash
# Might be old (I should automatise the upload)
pipx install llme-cli
llme --help
```

```bash
git clone https://github.com/privat/llme.git
pipx install -e llme
llme
```

```bash
# Just run it directly from the source directory
git clone https://github.com/privat/llme.git
./llme/llme/main.py --help
```


## Usage

### Run an interactive chat session

```bash
llme --base-url "http://localhost:8080/v1"
```

or if you want to a specific model


```bash
llme --base-url "http://localhost:8080/v1" --model "NexaAI/qwen3vl-8B-Thinking-4bit-mlx"
```

* Ctrl-C to interrupt a response (or exit).


### Setup a config (optional, but recommended):

Edit `~/.config/llme/config.toml`
Look at [config.toml](llme/config.toml) for an example.
More about options and configs bellow.

I assume, from now, that there is a config file...


### Run one-shots queries

Each prompt is run in order in the same chat session.

```bash
llme "What is the capital of France?" "What the content of the current directory?" "What is the current operating system?" "What is the factorial of 153?" "What is the weather at Tokyo right now?"
```

You can also pipe the query:

```bash
echo "What is the capital of France?" | llme
```


### Tools included

The LLM has direct access to your shell (and files) and a python interpreter.
The user is asked for confirmation before executing any command.
Beware, some LLMs might be very **persistent** and **persuasive** in running **dangerous** commands. Do **not trust** the LLM blindly!

If you chose to not execute a command, it will be skipped, and you can provide an explanation to the LLM or asks for a better command.

Some LLM might insist on not using a tool, asking the user to do it manually, or just simulate the action.
A better prompt engineering might help.
Proposals to improve the default system prompt are always welcome.


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

Note: Run a fresh `--help` in case I forgot to update this README.

All options with names in brackets can be set in the config file (`base_url` for `--base-url`).
They can also be set by environment variables (`LLME_BASE_URL` for `--base-url`).

For each option, the precedence order is the following:

1. The explicit option in the command line (the higher precedence)
2. The explicit config file (given by `--config`)
3. The environment variables (`LLME_SOMETHING`)
4. The user configuration file (`~/.config/llme/config.toml`)
5. The system configuration file provided by the package (the lowest precedence)


## Development

I do not like Python, nor LLMs, but I needed something simple to test things quickly and play around.
My goal is to keep this simple and minimal: it should fit into a single file and still be manageable.

PR are welcome!


## Issues

* The various openai compatible servers implement different subsets. Compatibility is thus not yet perfect, thus causing random 4xx or 5xx responses.
* Models are really sensitive to prompts and system prompts, but you can create a custom config file for each.
* Models are really sensitive to how the messages are structured, unfortunately that is currently hardcoded in the program.


## Thanks

* [openwebui](https://github.com/open-webui/open-webui) for an inspiration, but too complex and web oriented.
* [gptme](https://github.com/gptme/gptme) for another inspiration, but also too complex and targets too much non-local LLMs.
* [openai-cli](https://github.com/doryiii/openai-cli) for a simpler approach I built on top of.
* [llama.cpp](https://github.com/ggerganov/llama.cpp), [nexa-sdk](https://github.com/NexaAI/nexa-sdk/) and others for your great work.


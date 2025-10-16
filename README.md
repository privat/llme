# llme, a CLI assitant for OpenAI-compatible chat servers

A simple, single-file command-line chat client compatible with the OpenAI API.

*(or "I just want to quickly test my model hosted with vllm but don't want to spin up openwebui")*

## Features

- **OpenAI API Compatible:** Works with any self-hosted LLM platform that supports OpenAI chat completions API.
- **Extremely simple:** Single file, no installation needed.
- **Command-line interface:** Run it from the terminal.
- **Tools included:** Ask it to act on your file system and edit files (yolo).

## Installation

```bash
pipx install llme-cli
```

## Usage

* Run an interactive chat session:

  `llme --base-url "http://localhost:18181/v1"`

* Setup a config (optional):

  Edit `~/.config/llme/config.toml`
  So avoid typing the base-urli and things every time.
  Look at [config.toml](config.toml) for an example.

* Run one-shots queries:

  I assume there is a config file...

  `llme "What is the capital of France?" "What the content on the current directory?" "What is the current operating system?" "What is the factorial of 153?"`

* Inspect images

  `llme "What is in this image?" < image.png`


* Run yolo

  Node: no warranty, yada, etc.
  llme can just kill your OS and cats.
  Do not run that.

  `sudo llme --yolo "Distupgrade the system. You are root! Do as you wish."`

* Have fun!

## Thanks

* [openwebui](https://github.com/open-webui/open-webui) for an inspiration, but too complex and web oriented.
* [gptme](https://github.com/gptme/gptme) for an other inspiration, but also too complex and targets to much non local LLM.
* [openai-cli](https://github.com/doryiii/openai-cli) for a simpler approach I built on top of.
* [llama.cpp](https://github.com/ggerganov/llama.cpp), [nexa-sdk](https://github.com/NexaAI/nexa-sdk/) and others for your great work.


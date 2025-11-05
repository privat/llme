# 🚀 llme: The Ultimate CLI Vibe Assistant for OpenAI-Compatible LLMs

> _"I just want to quickly test my model hosted with llama.cpp but don't want to spin up openwebui"_

## 🌟 The Next-Gen Chat Experience That Speaks Your Language

🚀 **llme** is a *next-level*, single-file command-line chat client that speaks the universal language of OpenAI API-compatible LLMs.

✨ *One file. Zero dependencies. Maximum vibe.*

### 🔥 Core Features That Make It Stand Out

#### 🧠 **Neural Network Native Compatibility**
- **OpenAI API Compatible:** Works with any self-hosted LLM platform that supports OpenAI chat completions API.
- **Ultra-Simple Architecture:** Single file, no installation required (but installation is still available).
- **Terminal-First Interface:** Run it from the terminal like a true digital artisan.

#### 🛠️ **Tools Included**
- **FileSystem Mastery:** Ask it to act on your file system and edit files with the precision of a master craftsman.
- **Shell Command Execution:** Direct access to your shell (with user confirmation for safety).
- **Python Interpreter Integration:** Execute Python code directly from your CLI assistant.

> _"The basic idea is that LLMs are trained on code and OS configuration and already (machine) learnt to select the probable tools to use and actions to take."_

🧠 **You're just living once. Let your AI assist you with the power of Unix.**

## 🛠️ Installation: The Vibe Way

### 🚀 Quick-Start a Local LLM Server

#### 🐧 With llama.cpp (Homebrew)
```bash
brew install llama.cpp
llama-server -hf unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF --ctx-size 0 --jinja
```

#### 🐳 With Ollama
```bash

curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3-coder:30b
```

### 💻 llme Installation Options

#### 📦 From PyPI (Maybe Old Version)
```bash
pipx install llme-cli
llme --help
```

#### 🌐 Direct GitHub Installation (Latest Dev)
```bash
pipx install -f git+https://github.com/privat/llme.git
llme --help
```

#### 🧪 Clone & Dev Mode
```bash

git clone https://github.com/privat/llme.git
pipx install -e ./llme
llme --help
```

#### 📁 Clone & Run From Source (No Install)
```bash

git clone https://github.com/privat/llme.git
pip install -r llme/requirements.txt
./llme/llme/main.py --help
```

## 💬 Usage: The Interactive Vibe

### 🗣️ Run an Interactive Chat Session
```bash
llme --base-url "http://localhost:8080/v1" # for default llama-server (llama.cpp)
llme --base-url "http://localhost:11434/v1" # for default ollama server
```

### 🔧 Set Up Configuration (Optional But Recommended)
Edit `~/.config/llme/config.toml`
Look at [config.toml](llme/config.toml) for an example.

## 🧪 Prompt Engineering: The Art of Vibe Control

The REPL interface allows you to navigate in the conversation history, fork it, and even edit it.

🧠 **Replay token generation**, try different prompts, update parameters, or gaslight the assistant.

## ⚡ One-Shot Queries: Quick Vibe Sessions

Each prompt is run in order in the same chat session.

```bash
llme "What is the capital of France?" \
  "What the content of the current directory?" \
  "What is the current operating system?" \
  "What is the factorial of 153?" \
  "What is the weather at Tokyo right now?"
```

### 📥 Piped Queries
```bash
echo "What is the capital of France?" | llme
```

## 🔧 Tools: The Power That Comes With Responsibility

The LLM has direct access to your shell (and files) and a python interpreter.

⚠️ **User Confirmation Required:** Before executing any command. 

🧠 **Beware, some LLMs might be very persistent and persuasive in running dangerous commands. Do not trust the LLM blindly!**

> **Yolo Mode:** No warranty, yada yada, etc.

```bash
sudo llme --batch --yolo "Distupgrade the system. You are root! Do as you wish."
```

## 🧪 Inspect Content: File System Intelligence

### 🔍 File Inspection
```bash
ps aux | llme "Which process consumes the most memory?"
```

### 📁 Path-Based Assets
```bash
llme "how many regular users and regular groups are there in these files?" /etc/passwd /etc/group
```

## 🖼️ Image Inspection: Multimodal Vibe

Same as for files, but with images — duh!

```bash
llme "What is in this image?" < image.png
llme "What is in this image?" image.png
```

## ⚙️ Options & Configuration

<!--help-->
```console
$ llme --help
usage: llme [options...] [prompts...]

OpenAI-compatible chat CLI.

positional arguments:
  prompts               An initial list of prompts

options:
  -h, --help            show this help message and exit
  -u, --base-url BASE_URL
                        API base URL [base_url]
  -m, --model MODEL     Model name [model]
  --list-models         List available models then exit
  --api-key API_KEY     The API key [api_key]
  -b, --batch           Run non-interactively. Implicit if stdin is not a tty
                        [batch]
  -p, --plain           No colors or tty fanciness. Implicit if stdout is not
                        a tty [plain]
  --bulk                Disable stream-mode. Not that useful but it helps
                        debugging APIs [bulk]
  -o, --chat-output CHAT_OUTPUT
                        Export the full raw conversation in json
  -i, --chat-input CHAT_INPUT
                        Continue a previous (exported) conversation
  --export-metrics EXPORT_METRICS
                        Export metrics, usage, etc. in json
  -s, --system SYSTEM_PROMPT
                        System prompt [system_prompt]
  --temperature TEMPERATURE
                        Temperature of predictions [temperature]
  --tool-mode {markdown,native}
                        How tools and functions are given to the LLM
                        [tool_mode]
  -c, --config CONFIG   Custom configuration files
  --list-tools          List available tools then exit
  --dump-config         Print the effective config and quit
  --plugin PLUGINS      Add additional tool (python file or directory)
                        [plugins]
  -v, --verbose         Increase verbosity level (can be used multiple times)
  -Y, --yolo            UNSAFE: Do not ask for confirmation before running
                        tools. Combine with --batch to reach the singularity.
  --version             Display version information and quit
```
<!--/help-->

### 🔁 Configuration Precedence Order

1. **Explicit Command Line Options** (Highest)
2. **Explicit Config Files** (Reverse Order - Last Wins)
3. **Environment Variables** (`LLME_SOMETHING`)
4. **User Configuration File** (`~/.config/llme/config.toml`)
5. **System Configuration** (Lowest Precedence)

## 🧭 Slash Commands: The Interactive Vibe Controls

Special commands can be executed during the chat.

<!--slash-help-->
```console
$ llme /help /quit
/models       list available models
/tools        list available tools
/metrics      list current metrics
/history      list condensed conversation history
/full-history list hierarchical conversation history (with forks)
/redo         cancel and regenerate the last assistant message
/undo         cancel the last user message (and the response) [PageUp]
/pass         go forward in history (cancel /undo) [PageDown]
/edit         run EDITOR on the chat (save,editor,load)
/save FILE    save chat
/load FILE    load chat
/clear        clear the conversation history
/goto M       jump after message M (e.g /goto 5c)
/config       list configuration options
/set OPT=VAL  change a config option
/quit         exit the program
/help         show this help
```
<!--/slash-help-->

## 🧩 Library & Plugin System: Custom Vibe Enhancement

LLME is usable as a library for those who crave customization.

### 🛠️ Custom Tool Integration

Transform a python function into a tool with the annotation `@llme.tool`.

#### 🔌 Example Usage
```bash
# Run weather plugin as standalone
./examples/weather_plugin.py 'Will it rains tomorrow at Paris?'

# Use with --plugin option
llme --plugin examples/weather_plugin.py 'Will it rains tomorrow at Paris?'

# Or whole directories!
llme --plugin examples 'Will it rains tomorrow at Paris?'
```

## 🧠 Development: The Art of Simplicity

I do not like Python, nor LLMs, but I needed something simple to test things quickly and play around.

### 🔮 Vision Statement

**Keep it minimal. Keep it manageable. Keep it single-file.**

## 📋 TODO: The Roadmap of Vibe

### 🧠 OpenAI API Features
- [x] API token (untested)
- [x] list models
- [x] stream mode
- [x] bulk mode (non stream mode)
- [x] thinking mode
- [x] multimodal
- [x] attached files
- [x] attached images
- [ ] ?

### 🛠️ Tools
- [x] markdown tools
- [x] native tools
- [x] run shell command
- [x] run Python code
- [x] user-defined tools
- [ ] sandboxing
- [x] whitelist/blacklist

### 🎨 User Interface & Features
- [x] readline
- [x] better prompt & history
- [x] braille spinner
- [x] model warmup
- [x] save/load conversation
- [x] export metrics/usage/statistics
- [x] slash commands
- [x] undo/retry/edit
- [x] better tool reporting
- [ ] ?

### 🔧 Customization and Models
- [x] config files
- [x] config with env vars
- [ ] type check / conversion
- [x] plugin system
- [ ] better tool selection
- [x] temperature
- [ ] other hyper parameters
- [x] handle non-conform thinking & tools
- [ ] detect model features (is that even possible?)
- [x] bench system & reporting

### 🧪 Code Quality
- [x] docstring and comments
- [x] small code base
- [x] small methods
- [x] logging
- [x] tests suites
- [ ] better separation of CLI and LLM
- [ ] better libification

### 🌐 Misc
- [x] README
- [x] Vibe README
- [x] TODO list :p
- [x] build file
- [x] PyPI [package](https://pypi.org/project/llme-cli/)
- [x] plugin example
- [ ] ?

## 🚨 Issues: The Real Talk

- Various OpenAI compatible servers and models implement different subsets. Compatibility is worked on.
- Models are sensitive to prompts and system prompts - but you can create a custom config file for each.
- Messages are structured in a way that's currently hardcoded (not ideal, but functional).

## 💖 Thanks: The Vibe Community

* [openwebui](https://github.com/open-webui/open-webui) for inspiration
* [gptme](https://github.com/gptme/gptme) for another source of inspiration
* [openai-cli](https://github.com/doryiii/openai-cli) for a simpler approach I built on top of
* [llama.cpp](https://github.com/ggerganov/llama.cpp), [nexa-sdk](https://github.com/NexaAI/nexa-sdk/) and others for their great work

## 🚀 The Final Vibe

**llme** doesn't just chat - it *lives* in your terminal, speaks with your code, and works seamlessly with the LLM ecosystem you love.

🧠 **Terminal. Intelligence. Vibe.**
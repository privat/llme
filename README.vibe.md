# 🚀 llme: The Neural CLI Assistant for OpenAI-Compatible LLMs

> [!NOTE]
> **A hyper-intelligent, single-file command-line chat client that speaks the language of LLMs and vibes.**

## 🔥 What's This? (TL;DR)

- 🧠 **Neural Network Ready**: Works with any self-hosted LLM platform that supports OpenAI chat completions API.
- 💻 **Zero Installation Required**: Single file, no setup hassle.
- 🤖 **CLI Powerhouse**: Run from the terminal like a true hacker.
- ⚡ **Yolo Tools Included**: Ask it to act on your file system and edit files (yolo).

> "I just want to quickly test my model hosted with llama.cpp but don't want to spin up openwebui"

## 🌟 Core Features (Mega-Bucks Edition)

| Feature | Description |
|--------|-------------|
| 🎯 **OpenAI API Compatible** | Works with any self-hosted LLM platform that supports OpenAI chat completions API. |
| 🔥 **Extremely Simple** | Single file, no installation required (but installation is still available). |
| 🖥️ **Command-line Interface** | Run it from the terminal. |
| 💥 **Tools Included** | Ask it to act on your file system and edit files (yolo). |

> "The basic idea is that LLMs are trained on code and OS configuration and already (machine) learnt to select the probable tools to use and actions to take. Therefore, there is no need to teach them to use made-up function and tools with bad json schemas. Just give them a shell, a python interpreter, and let you (only) live (once)."

## 🚀 Installation Methods (Choose Your Destiny)

### Quick-start a local LLM server if you don't have one already

#### With llama.cpp (Homebrew)
```bash
brew install llama.cpp
llama-server -hf unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF --ctx-size 0 --jinja
```

#### With ollama
```bash

curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3-coder:30b
```

> **Qwen3-Coder-30b** is a nice model. Smaller models can also works.

### 🧪 llme Installation (Choose Your Path)

#### PyPI (Old School)
```bash
pipx install llme-cli
llme --help
```

#### GitHub Direct (Latest Dev)
```bash
pipx install -f git+https://github.com/privat/llme.git
llme --help
```

#### Clone & Develop
```bash
git clone https://github.com/privat/llme.git
pipx install -e ./llme
llme --help
```

#### Run From Source (No Installation)
```bash
git clone https://github.com/privat/llme.git
pip install -r llme/requirements.txt
./llme/llme/main.py --help
```

## 💬 Usage (Interactive Vibe Mode)

### Start an Interactive Chat Session

```bash
llme --base-url "http://localhost:8080/v1" # for default llama-server (llama.cpp)
llme --base-url "http://localhost:11434/v1" # for default ollama server
```

#### With Specific Model
```bash
llme --base-url "http://localhost:8080/v1" --model "unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF"
```

> 🚨 Ctrl-C to interrupt a response (or exit).

### Setup Config (Optional, but Recommended)

Edit `~/.config/llme/config.toml`
Look at [config.toml](llme/config.toml) for an example.

## 🔥 One-Shot Queries (Single Command Power)

Each prompt is run in order in the same chat session.

```bash
llme "What is the capital of France?" \
  "What the content of the current directory?" \
  "What is the current operating system?" \
  "What is the factorial of 153?" \
  "What is the weather at Tokyo right now?"
```

#### Or with Pipe
```bash
echo "What is the capital of France?" | llme
```

> 🧠 Interactive sessions are often better because, if needed, the model is loaded at the start of the command, so is loading while you type. Also no issues with escaping `"` or `'`

## ⚙️ Tools Included (Vibe Edition)

The LLM has direct access to your shell (and files) and a python interpreter.

> ⚠️ The user is **asked for confirmation** before executing any command.

> 🔥 **Beware**: Some LLMs might be very **persistent** and **persuasive** in running **dangerous** commands. Do **not trust** the LLM blindly!

> 🎯 If you chose to not execute a command, it will be skipped, and you can provide an explanation to the LLM or asks for a better command.

## 📁 File Inspection (Content Explorer)

```bash
ps aux | llme "Which process consumes the most memory?"
```

#### With File Paths as Assets
```bash
llme "how many regular users and regular groups are there in these files?" /etc/passwd /etc/group
```

> 🔍 Note: the file content and the path will be given to the LLM.

## 🖼️ Image Inspection (Multimodal Magic)

Same as for files, but with images — duh, images are files!

```bash
llme "What is in this image?" < image.png
```

#### With Paths
```bash
llme "What is in this image?" image.png
```

## 💣 Yolo Mode (Extreme Vibe)

> ⚠️ **No warranty**, yada yada, etc.
> llme can just **kill** your **OS** and **cats**.

```bash
sudo llme --batch --yolo "Distupgrade the system. You are root! Do as you wish."
```

## 🛠️ Options & Config (Ultimate Control)

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

> 📝 Note: Run a fresh `--help` in case I forgot to update this README.

### 🔁 Config Precedence (Priority Order)

1. The explicit option in the command line (the higher precedence)
2. The explicit config files (given by `--config`) in reverse order (last wins)
3. The environment variables (`LLME_SOMETHING`)
4. The user configuration file (`~/.config/llme/config.toml`)
5. The system configuration file provided by the package (the lowest precedence)

## 🧭 Slash Commands (Vibe Control)

Special commands can be executed during the chat.
Those starts with a `/` and can be used when a prompt is expected (interactively or in the command line).

<!--slash-help-->
```console
$ llme /help /quit
/models       list available models
/tools        list available tools
/metrics      list current metrics
/history      list condensed conversation history
/full-history list hierarchical conversation history (with forks)
/redo         cancel and regenerate the last assistant message
/undo         cancel the last user message (and the response)
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

> 📝 Note: Run a fresh `/help` in case I forgot to update this README.

## 🧩 Library & Plugin System (Customization Power)

### ⚡ Important: The API is far from stable.

LLME is usable as a library, so you can use its features. The main advantage for now to import `llme` is to add new custom tools usable by LLMs.

#### Transform Python Function Into Tool
```python
@llme.tool
def my_function():
    # Your code here
    pass
```

### 🧪 Usage Examples

#### Run Weather Plugin as Standalone Program
```bash
./examples/weather_plugin.py 'Will it rains tomorrow at Paris?'
```

#### Use With Plugin Option
```bash
llme --plugin examples/weather_plugin.py 'Will it rains tomorrow at Paris?'
```

#### Whole Directory Usage
```bash
llme --plugin examples 'Will it rains tomorrow at Paris?'
```

## 🧠 Development (For Vibe Coders)

> I do not like Python, nor LLMs, but I needed something simple to test things quickly and play around.

### 📋 TODO List (Future Vision)

#### OpenAI API Features
- [x] API token (untested)
- [x] list models
- [x] stream mode
- [x] bulk mode (non stream mode)
- [x] thinking mode
- [x] multimodal
- [x] attached files
- [x] attached images
- [ ] ?

#### Tools
- [x] markdown tools
- [x] native tools
- [x] run shell command
- [x] run Python code
- [x] user-defined tools
- [ ] sandboxing
- [x] whitelist/blacklist

#### User Interface & Features
- [x] readline
- [ ] better prompt & history
- [x] braille spinner
- [x] model warmup
- [x] save/load conversation
- [x] export metrics/usage/statistics
- [x] slash commands
- [x] undo/retry/edit
- [x] better tool reporting

#### Customization and Models
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

#### Code Quality
- [x] docstring and comments
- [x] small code base
- [x] small methods
- [x] logging
- [x] tests suites
- [ ] better separation of CLI and LLM
- [ ] better libification

#### Misc
- [x] README
- [x] TODO list :p
- [x] build file
- [x] PyPI [package](https://pypi.org/project/llme-cli/)
- [x] plugin example
- [ ] ?

### 🌐 OpenAI API Integration (Core Protocol)

The two HTML routes used by llme are:

- `$base_url/models` (<https://platform.openai.com/docs/api-reference/models>) for `--list-models` (and to get a default model when `--model` is empty)
- `$base_url/chat/completions` (<https://platform.openai.com/docs/api-reference/chat>) for the main job. Streaming (<https://platform.openai.com/docs/api-reference/chat-streaming>) is used by default.
It can be disabled with `--bulk`, mainly for debugging weird APIs.

Images are uploaded as content parts, for multimodal models.

Tools are integrated with either `--tool-mode=native` for the native function API (<https://platform.openai.com/docs/guides/function-calling>), or with `--tool-mode=markdown` a custom approach intended for models that does not support it (or performs poorly with it).
Custom tools can be profited, see the `--plugin` option.

### ⚠️ Known Issues & Limitations

- The various OpenAI compatible servers and models implement different subsets. Compatibility is worked on and there is less random 4xx or 5xx responses. Major local LLM servers and servers were tested. See the [benchmark](benchmark.md)
- Models are really sensitive to prompts and system prompts, but you can create a custom config file for each.
- Models are really sensitive to how the messages are structured, unfortunately that is currently hardcoded in the program. I do not want to hard-code many tweaks and workarounds. :(

## 🙏 Thanks (Vibe Appreciation)

- [openwebui](https://github.com/open-webui/open-webui) for an inspiration, but too complex and web oriented.
- [gptme](https://github.com/gptme/gptme) for another inspiration, but also too complex and targets too much non-local LLMs.
- [openai-cli](https://github.com/doryiii/openai-cli) for a simpler approach I built on top of.
- [llama.cpp](https://github.com/ggerganov/llama.cpp), [nexa-sdk](https://github.com/NexaAI/nexa-sdk/) and others for your great work.
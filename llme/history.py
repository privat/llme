"""Conversation history: message tree, chat persistence, and navigation."""

import json
import logging
import os
import re
import subprocess

from .errors import AppError

logger = logging.getLogger('llme')


def base26ish(n):
    """Convert an integer to a base26ish string. Used to name generations.
    0 is 'a', 25 is 'z', 26 is 'aa', 27 is 'ab', etc.
    In genuine base26, 26 should be 'ba' since a stands for 0 and b for 1.
    """
    result = ""
    while n >= 0:
        result = chr(ord('a') + (n % 26)) + result
        n //= 26
        n -= 1
    return result

def unbase26ish(s):
    """Convert a base26ish string to an integer. Inverse of base26ish()."""
    result = 0
    for c in s:
        result = result * 26 + (ord(c) - ord('a')) + 1
    return result - 1

class Message:
    """A message in the conversation full history. This class is used to track message generations and children."""
    def __init__(self, data, parent, n, gen):
        self.data = data # The raw json data for the openai API
        self.parent = parent # The parent message in the conversation tree
        self.number = n # The message number in the conversation
        self.generation = gen # The generation number of the message
        self.id = f"{self.number}{base26ish(self.generation)}" # The unique id of the message
        self.children = [] # The children messages of this message
        meta = data.get("llme-meta")
        if meta is None:
            meta = {}
            self.data["llme-meta"] = meta
        meta["id"] = self.id
        if parent:
            meta["parent"] = parent.id

    def role(self):
        return self.data["role"]

    def content(self):
        """The text content of a message"""
        content = self.data["content"]
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        for c in content:
            if c["type"] == "text":
                return c["text"]

    def tool_calls(self):
        return self.data.get("tool_calls")

    def prefix(self):
        """Return the prefix for the message"""
        return self.id

    def __repr__(self):
        return self.prefix()

class HistoryMixin:
    """LLME mixin: conversation history (message tree, persistence, navigation)."""
    def build_message_object(self, message):
        """Add a message to the history"""

        n = len(self.history)
        append = True
        meta = message.get("llme-meta")
        if meta is not None:
            if parent_id := meta.get("parent"):
                parent = self.get_message_by_id(parent_id)
                if parent is None:
                    logger.error("Parent message not found: %s", parent_id)
                else:
                    gen = parent.generation
                    sibling = parent.children
                    if n > 0 and parent != self.history[n-1]:
                        append = False
        if n > 0:
            parent = self.history[n-1]
            gen = parent.generation
            sibling = parent.children
        else:
            parent = None
            gen = 0
            sibling = self.roots

        if sibling:
            for s in sibling:
                if s.data == message:
                    # Already known, reuse it
                    if append:
                        self.history.append(s)
                        self.current_generation = s.generation
                    return s
            # Need a new generation number
            self.generations.append(message)
            gen = len(self.generations)

        message_obj = Message(message, parent, n, gen)
        self.full_history.append(message_obj)
        sibling.append(message_obj)
        if self.config.chat_output:
            if self.chat_output_file is None:
                self.chat_output_file = open(self.config.chat_output, "w")
            self.chat_output_file.write(json.dumps(message) + "\n")
            self.chat_output_file.flush()
        if append:
            self.history.append(message_obj)
            self.current_generation = gen
        return message_obj

    def add_message(self, message):
        """
        Append a new message.
        Add it as is in message but transform it in raw_messages.
        """

        self.fork_if_required()

        logger.debug("Add %s message: %s", message['role'], message)
        result = self.build_message_object(message)
        if self.history[-1] != result:
            return result

        raw_message = json.loads(json.dumps(message))
        if "llme-meta" in raw_message:
            del raw_message["llme-meta"]
        if "channel" in raw_message:
            del raw_message["channel"] # Groq adds it but refuse it. Weird
        self.filter_file(raw_message)

        if raw_message["role"] == "tool" and self.config.tool_mode != "native":
            raw_message["role"] = "user"

        self.raw_messages.append(raw_message)
        return result

    def filter_file(self, message):
        """Filter that handle how file are transmitted.
        See --file-mode"""
        if not isinstance(message.get("content"), list):
            return
        if self.config.file_mode == "part":
            return

        text_content = []
        # unpack file content parts
        for part in message["content"]:
            if part["type"] == "text":
                text_content.append(part["text"])
            elif part["type"] == "image_url":
                # sorry, images need parts
                return
            elif part["type"] != "file":
                logger.warning("unknown content part type %s", part["type"])
                return
            elif self.config.file_mode == "json":
                # serialize the part as is
                text_content.append(json.dumps(part['file']))
            elif self.config.file_mode == "path":
                # replace the part with the path.
                path = part['file']['filename']
                if self.config.box:
                    dirname = os.path.dirname(path)
                    filename = os.path.basename(path)
                    basename, extension = os.path.splitext(filename)
                    tempname = self.new_tempfile(basename + "_", extension)
                    b64 = part['file']['file_data']
                    import base64
                    data = base64.b64decode(b64)
                    self.write_file(tempname, data)
                    path = tempname
                text_content.append(f"The path of the file is {path}. You can cat its content.")
            else:
                logger.warning("unknown file_mode %s", self.config.file_mode)
                return

        message["content"] = "\n\n".join(text_content)

    def fork_if_required(self):
        """Fork the conversation to a new generation, if required.
        This will reset the conversation history"""
        if self.message_index is None:
            return
        # Here we need to reset the current conversation to fork it
        # And replace the "message_index" wit a new one
        if self.message_index > 0:
            self.reset_to_history(self.history[self.message_index-1])
        else:
            self.reset_messages([])
        logger.debug(f"Fork performed. New history: %s", self.history)


    def prompt_prefix(self):
        """Return the prefix number to use in the prompt"""
        res = str(len(self.history))
        if self.message_index is not None:
            res = f"{self.message_index}/{res}"
        return res

    def start_session(self):
        if self.config.no_session:
            return
        session_root_directory = os.path.expanduser("~/.config/llme/sessions")
        import time
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        if self.config.session:
            if os.path.exists(self.config.session):
                session_directory = self.config.session
            else:
                session_directory = os.path.join(session_root_directory, self.config.session)
                if not os.path.exists(session_directory):
                    raise AppError(f"Session {self.config.session} not found (also tried {session_directory})")
            if not self.config.chat_input:
                chat_file = os.path.join(session_directory, "chat.jsonl")
                if os.path.exists(chat_file):
                    self.config.chat_input = chat_file
            logger.info("Resuming session in %s", session_directory)
        else:
            os.makedirs(session_root_directory, exist_ok=True)
            self.config.session = timestamp
            session_directory = os.path.join(session_root_directory, timestamp)
            os.makedirs(session_directory, exist_ok=False)
            logger.info("New session in %s", session_directory)
        if not self.config.chat_output:
            self.config.chat_output = os.path.join(session_directory, "chat.jsonl")
        if not self.config.export_metrics:
            self.config.export_metrics = os.path.join(session_directory, f"{timestamp}-metrics.json")
        if not self.config.raw_request_dump:
            self.config.raw_request_dump = os.path.join(session_directory, f"{timestamp}-request.json")
        if not self.config.raw_response_dump:
            self.config.raw_response_dump = os.path.join(session_directory, f"{timestamp}-response.json")
        conf_file = os.path.join(session_directory, f"{timestamp}-config.json")
        with open(conf_file, "w") as f:
            json.dump(vars(self.config), f, indent=2)
        logfile = os.path.join(session_directory, f"{timestamp}.log")
        filehandler = logging.FileHandler(logfile)
        filehandler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        filehandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(filehandler)

    def load_chat(self, file, format=None):
        logger.info("Loading conversation from %s", file)
        if not format:
            format = self.chat_file_format(file)
        try:
            with open(file, "r") as f:
                if format == "yaml":
                    import yaml
                    messages = yaml.safe_load(f)
                if format == "jsonl":
                    messages = []
                    for line in f:
                        line = line.strip()
                        if line:
                            messages.append(json.loads(line))
                else:
                    if format != "json":
                        logger.error("Unknown format %s. Default as json", format)
                    messages = json.load(f)
            self.reset_messages(messages)
        except OSError as e:
            raise AppError(f"Can't load chat from {file}") from e

    def get_message_by_id(self, message_id):
        """Get a message by its id"""
        for m in self.full_history:
            if m.id == message_id:
                return m
        return None

    def reset_messages(self, messages):
        self.message_index = None
        self.history.clear()
        self.raw_messages.clear()
        id_map = {}
        for message in messages:
            orig_id = message.get("id")
            if orig_id is not None:
                del message["id"]
                orig_parent = message.get("parent")
                if orig_parent:
                    del message["parent"]
                    dest_parent = id_map.get(orig_parent)
                    if not dest_parent:
                        logger.error("Parent %s not found for %s", orig_parent, orig_id)
                    else:
                        message["parent"] = dest_parent
            m = self.add_message(message)
            if orig_id is not None:
                id_map[orig_id] = m.id
        logger.info("Reset %d messages", len(self.history))

    def chat_file_format(self, file):
        """Return the format of a chat file"""
        if file.endswith(".yaml") or file.endswith(".yml"):
            return "yaml"
        elif file.endswith(".jsonl"):
            return "jsonl"
        else:
            if not file.endswith(".json"):
                logger.error("Unknown format extension for %s. Default to json", file)
            return "json"

    def save_chat(self, file, messages=None, format=None):
        if messages is None:
            messages = self.full_history
        if not format:
            format = self.chat_file_format(file)
        logger.info("Dumping %s messages to %s", len(messages), file)
        try:
            all_messages = [m.data for m in messages]
            with open(file, "w") as f:
                if format == "yaml":
                    import yaml
                    yaml.dump(all_messages, f, default_flow_style=False, default_style="", width=65536)
                elif format == "jsonl":
                    for m in all_messages:
                        json.dump(m, f)
                        f.write('\n')
                else:
                    if format != "json":
                        logger.error("Unknown format %s. Saved as json", format)
                    json.dump(all_messages, f, indent=2)
        except OSError as e:
            raise AppError(f"Can't save chat to {file}") from e

    def rollback(self, roles = ["user", "tool"]):
        "Move message_index to the previous message of role, return the message on success"
        candidate = None
        for i, message in enumerate(self.history):
            if self.message_index and i >= self.message_index:
                break
            if message.role() in roles:
                candidate = i
        if not candidate:
            return None
        self.message_index = candidate
        return self.history[candidate]

    def rollforward(self, roles = ["user", "tool"]):
        "Move message_index to the next message of role, return the message on success"
        if self.message_index is None:
            return None
        for i, message in enumerate(self.history[self.message_index+1:]):
            if message.role() in roles:
                self.message_index = i + self.message_index + 1
                return message
        self.message_index = None
        return True


    def edit(self):
        "Save the chat in a tmpfile, edit it, and load it back"
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix=".yaml", delete=True) as tmp:
            import shlex
            self.save_chat(tmp.name, self.history, format="yaml")
            editor = os.environ.get("EDITOR", "editor")
            try:
                cmd = shlex.split(editor) + [tmp.name]
            except ValueError as e:
                raise AppError("Invalid editor command %s" % editor) from e
            logger.info( "Running %s", cmd)
            try:
                subprocess.run(cmd, check=True)
            except Exception as e:
                raise AppError("/edit") from e
            self.load_chat(tmp.name)


    def reset_to_history(self, message):
        """Reset the conversation to after a message in the full history"""
        self.current_generation = message.generation
        messages = []
        while message:
            messages.insert(0, message.data)
            message = message.parent
        self.reset_messages(messages)

    def find_label_in_history(self, n):
        """Return a labeled message from the full history"""
        match = re.match(r"(\d+)\s*([a-z]*)", n)
        if not match:
            raise AppError(f"Invalid message label {n}")
        num = int(match.group(1))
        if not match.group(2):
            # no gen, look in the local history first
            if num < len(self.history):
                message = self.history[num]
                logger.debug("goto %d -> %r", num, message)
                return message
            gen = self.current_generation
        else:
            gen = unbase26ish(match.group(2))

        message = self.find_in_history(num, gen)
        logger.debug("goto %s -> %d %d -> %r", n, num, gen, message)
        return message

    def goto(self, n):
        """Jump after a message in the full history"""
        message = self.find_label_in_history(n)
        if not message:
            raise AppError(f"Message {n} not found")
        if message not in self.history:
            self.reset_to_history(message)
        self.message_index = message.number

    def find_in_history(self, num, gen, messages = None):
        """Search a message in the full history with its number and generation."""
        if messages is None:
            messages = self.roots
        for message in messages:
            if message.number == num and message.generation == gen:
                return message
            found = self.find_in_history(num, gen, message.children)
            if found:
                return found
        return None

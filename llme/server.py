"""OpenAI-compatible server communication: httpx, streaming, metrics, warmup."""

import json
import logging
import os
import re
import sys
import threading
import time

import httpx

from termcolor import cprint

from .errors import AppError
from .terminal import ChunkPrinter, Spinner
from .tools import all_tools

logger = logging.getLogger('llme')
CHUNK_FIXED_FIELDS = ["role", "model", "channel"]


def chunk_update(orig, delta, path=""):
    """Deep update for chunks in streamed messages. This only appends information and should never changes it.
    This is global chunk merging approach. I hove weird open-api providers will not be too much insane."""
    import copy
    delta = copy.deepcopy(delta)
    for k, v in delta.items():
        ov = orig.get(k)
        if isinstance(v, dict) and isinstance(ov, dict):
            chunk_update(ov, v, f"{path}.{k}")
        elif (isinstance(v, str) and isinstance(ov, str)
              # Do not concatenate str values in some root elements as some provider (groq and ollama at least) repeat values in those keys
              and not (path == "" and k in CHUNK_FIXED_FIELDS)):
            orig[k] += v
        elif isinstance(v, list) and isinstance(ov, list):
            for item in v:
                # Special case, extension of an existing element in an array
                if isinstance(item, dict):
                    idx = item.get("index")
                    if idx is not None:
                        if idx < len(ov):
                            chunk_update(ov[idx], item, f"{path}[{idx}]")
                            continue
                        while len(ov) < idx:
                            logger.warning("Broken server? Chunked array needs empty slots (%r)[%s] = %r", ov, idx, item)
                            ov.append({})
                        ov.append(item)
                        continue
                # Otherwise, just append
                ov.append(item)
        else:
            if ov is not None and v != ov:
                logger.error("Broken server? Chunk update issue %s.%s override %r by %r", path, k, ov, v);
            orig[k] = v
    return orig

class SSEReader:
    """Utility class to read the Server-Sent Events (SSE) used in stream mode"""
    def __init__(self, response):
        response.encoding = "utf-8" # explicit, do not trust the server
        self.iter_lines = response.iter_lines()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            line = next(self.iter_lines)
            if not line:
                continue
            if line[0] == '{':
                # special case of no streaming
                data = json.loads(line)
                return data
            # Handle classic SSE
            event, sep, data = line.partition(':')
            if not sep:
                logger.warning(f"Chunk: Unexpected: %s", line)
                continue
            if event == '':
                if data == '':
                    logger.debug("Chunk: keep alive")
                else:
                    logger.info("Chunk: comment: %s", data)
                continue
            if event != 'data':
                logger.warning(f"Chunk: Unexpected event type: %s", line)
                continue
            if data in ['[DONE]', ' [DONE]']:
                # We continue the connection until the server closes it. We do not trust it.
                continue
            try:
                data = json.loads(data)
                return data
            except:
                logger.warning("Chunk: Got a weird one: %s", data)

class DummyResponse:
    """A fake streaming response built from a canned message.
    It mimics the minimal interface of a streaming httpx.Response
    (iter_lines, raise_for_status, close) so that the whole
    receive_chat_completion_message() code path is exercised as with a real
    server. Used with --dummy-responses to test without a server."""
    def __init__(self, message, model):
        # A whole message is just a big delta. Wrap it in a single SSE chunk.
        chunk = {"choices": [{"delta": message, "finish_reason": "stop"}], "model": model}
        if "timings" in message:
            chunk["timings"] = message["timings"]
        self._line = "data: " + json.dumps(chunk)

    def iter_lines(self):
        return iter([self._line])

    def raise_for_status(self):
        return None

    def close(self):
        pass

def load_dummy_responses(path):
    """Load the canned responses for --dummy-responses.
    Compatible with --raw-response-dump output: a json array of messages, a single
    json message, or a jsonl file with one message per line."""
    try:
        with open(path, "r") as f:
            content = f.read()
    except OSError as e:
        raise AppError(f"Can't load dummy responses from {path}") from e
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = None
    if data is None:
        # Not a single json document: assume jsonl (one raw response per line)
        data = [json.loads(line) for line in content.splitlines() if line.strip()]
    elif isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        raise AppError(f"Invalid dummy responses file {path}: expected a json array, a single message, or jsonl")
    return data

def extract_requests_error(e):
    """Common handling of httpx error"""
    logger.debug("httpx error: %s", e)
    if e.request is None:
        return str(e)
    if getattr(e, "response", None) is None: # httpx transport errors have no response
        return f"{e} ({e.request.url})"
    logger.debug("response headers: %s", e.response.headers)

    """Server may format their error in plain text or json"""
    text = e.response.text
    if text and text[0] == '{':
        logger.debug("full error response: %s", text)
        try:
            data = json.loads(text)
        except:
            data = {}
        if "error" in data:
            data = data["error"]
            text = data
        if "message" in data:
            text = data["message"]

    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 200:
        text = text[:200] + "..."

    message = f"{text.strip()} ({e.response.status_code} {e.response.request.url})"
    return message

class Warmup:
    """ A small chat request, sent while the user is typing its first prompt.
    It loads the model (if needed) and starts filling the server context, with the model and the system prompt.
    The warmup is purely advisory: If it is still running (or has failed) when the user submits its first prompt, the real request is sent anyway: the server processes both in parallel, and the warmup one is a single token.
    """

    def __init__(self, llm):
        """The thread is started as soon as possible.
        But no failure is reported before check(), called before the first prompt input"""
        self.llm = llm
        self.thread = threading.Thread(target=self._process)
        self.thread.daemon = True
        self.message = None
        self.lock = threading.Lock()
        self.started = False
        self.stopped = False
        self.thread.start()


    def check(self):
        """Stop the program if the warmup failed.
        Or start the watch."""
        with self.lock:
            if self.message is not None:
                logger.error(self.message)
                sys.exit(1)
            self.started = True
        return


    def stop(self):
        """Stop caring about the warmup now.
        There is no clean way in Python to stop the running process or its requests. So just let ignore it and let it die."""
        with self.lock:
            self.stopped = True


    def _process(self):
        """ Thread,function.
        It justs wait for the completion of a small request.
        If everything is fine then the thread will just terminate. Otherwise it will signal am event for the main thread.
        Note: because of httpx limitation there is no real way to cancel the request. This is mildly annoying."""

        url = f"{self.llm.config.base_url}/chat/completions"
        json = {
            "model": self.llm.model,
            "messages": self.llm.raw_messages, # use the raw message with system prompt for warmup
            "max_completion_tokens":1,
            "max_tokens":1,
            "temperature":0,
            "stream": True,
        }
        logger.info("warmup %s", url)
        try:
            # note: most of the warmup time is spend in httpx.get, response is only set when a response is transmitted
            # there is no sane way to cancel it, unfortunately
            response = httpx.post(url=url, headers=self.llm.api_headers, json=json, timeout=None)
            response.raise_for_status() # Care for errors
            response.close() # Do not care for content
        except httpx.HTTPError as e:
            # store, signal or ignore
            with self.lock:
                logger.info("warmup: raise %s", e)
                if self.stopped:
                    # ignore (got first prompt, don't care about warmup anymore). Same error is likely to occur on the normal path anyway.
                    return

                self.message = extract_requests_error(e)
                if not self.started: # stored (fist prompt not asked yet)
                    return

                # signal (currently asking for first prompt)
                logger.error("%s", self.message)
                # sys.stdin.close() don't cancel readline
                # sys.exit(1) don't stop the process
                # both approaches are not that much thread-safe
                # The remaining route is to send a signal that will interrupt the main thread
                import signal
                os.kill(os.getpid(), signal.SIGQUIT)
                return
        logger.info("warmup: completed")

class ServerMixin:
    """LLME mixin: talks to the (OpenAI-compatible) server."""
    def get_models(self):
        """List the available models"""
        if self.config.dummy or self.config.dummy_responses:
            # Return a proper model dict, as the callers expect "id" and "state" fields
            return [{"id": "dummy", "state": "loaded"}]
        url = f"{self.config.base_url}/models"
        logger.info("Get models from %s", url)
        try:
            response = httpx.get(url, headers=self.api_headers, timeout=self.config.timeout_http)
            response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error("Error getting models: %s", extract_requests_error(e))
            return None
        models = response.json()
        ids = [m["id"] for m in models["data"]]
        for m in models["data"]:
            # llama.cpp give a status field
            m["state"] = m.get("status", {}).get("value")
        logger.info("Available models: %s", ids)
        return models["data"]


    def next_dummy_response(self):
        """Return the next canned response for --dummy-responses.
        The responses file is loaded lazily on first use, and one response is
        consumed per call, until the file is exhausted."""
        if self.dummy_responses_queue is None:
            self.dummy_responses_queue = load_dummy_responses(self.config.dummy_responses)
        if self.dummy_responses_index >= len(self.dummy_responses_queue):
            if self.dummy_responses_index == len(self.dummy_responses_queue):
                logger.info("No more dummy responses in %s (needed response #%d", self.config.dummy_responses, self.dummy_responses_index+1)
            message = {"role":"assistant","content":"Dummy response filler"}
        else:
            message = self.dummy_responses_queue[self.dummy_responses_index]
        self.dummy_responses_index += 1
        return message


    def dump_raw_response(self, message):
        """Append the raw response message to the raw_response_dump file.
        That file is a jsonl file: one complete json message per line.
        The file is opened once in append mode and kept open."""
        if not self.config.raw_response_dump:
            return
        if self.raw_response_dump_file is None:
            try:
                self.raw_response_dump_file = open(self.config.raw_response_dump, "a")
            except OSError as e:
                raise AppError(f"Can't open raw response dump {self.config.raw_response_dump}") from e
        self.raw_response_dump_file.write(json.dumps(message) + "\n")
        self.raw_response_dump_file.flush()

    def post_chat_completion(self, tools=None):
        """Prepare and send the POST request.
        Returns a response"""
        url = f"{self.config.base_url}/chat/completions"
        data = {
            "model": self.model,
            "messages": self.raw_messages,
            "stream": not self.config.bulk,
            "stream_options": {"include_usage": True},
        }
        if self.config.tool_mode == "native":
            data_tools = []
            for n, tool in all_tools.items():
                if tools is not None and n not in tools:
                    continue
                data_tools.append(tool.schema)
            if tools:
                for n in tools:
                    if not n in all_tools:
                        logger.warning("Unknown tool %s", n)
            if data_tools:
                data["tools"] = data_tools

        if self.config.temperature is not None:
            data["temperature"] = self.config.temperature
        if(self.config.extra_body):
            data.update(self.config.extra_body)
        if self.config.raw_request_dump:
            with open(self.config.raw_request_dump, "w") as f:
                json.dump(data, f, indent=2)
        logger.debug("Sending %d raw messages to %s", len(self.raw_messages), url)
        if self.config.dummy_responses:
            logger.info("Dummy response from %s (no server contacted)", self.config.dummy_responses)
            return DummyResponse(self.next_dummy_response(), self.model)
        # httpx responses are always lazily read, so no stream= argument is needed
        return httpx.post(
            url,
            json=data,
            headers=self.api_headers,
            timeout=self.config.timeout_http,
        )

    def receive_chat_completion_message(self, response):
        """Process the server response to extract and return the message.
        This function handle; stream mode, tools, thinking, metrics, etc."""

        if self.answering_model is None:
            self.answering_model = self.model

        start_time = time.perf_counter()
        message = {} # The whole message
        meta = {} # LLME specific metadata
        last_chunk = None
        first_token = True
        cp = ChunkPrinter()
        for data in SSEReader(response):
            processed = False
            choices = data.get("choices")
            if not choices:
                # assume an empty chunk. This avoids None tests below
                choices = [{"delta":{}}]
            elif len(choices) > 1:
                logger.warning("chunk: too much choices: %s", data)
            choice0 = choices[0]

            # A whole message is just a big delta! So reuse the whole code path
            delta = choice0.get('message')
            if not delta:
                delta = choice0['delta']

            # last_chunk is used for debugging, it's usually too much to print each chunk
            last_chunk = data
            self.completion_metrics["chunk_n"] += 1

            chunk_update(message, delta)

            # Some openai-api provider have a reasoning_content field, with various names
            # It's non-standard but helps to distinguish the reasoning content from the main content
            for label in ["reasoning_content", "reasoning"]:
                reasoning_content = delta.get(label)
                if reasoning_content:
                    break # We found one
            if reasoning_content:
                processed = True
                cp.print(reasoning_content, "light_magenta", id='reasoning_content')

            content = delta.get("content")
            if content:
                processed = True
                cp.print(content, id='content')

            tool_calls = delta.get("tool_calls")
            if tool_calls:
                processed = True
                for tool_call in tool_calls:
                    idx = tool_call.get("index")
                    f = tool_call["function"]
                    if "name" in f:
                        cp.print(f["name"], color="yellow", id=idx)
                    arguments = f["arguments"]
                    if not isinstance(arguments, str):
                        # Some providers send the arguments already parsed (a json object)
                        arguments = json.dumps(arguments)
                    cp.print_escaped(arguments, color="yellow", string_color="light_yellow", id=idx)

            finish_reason = choice0.get('finish_reason')
            if finish_reason:
                processed = True
                # About: finish_reason
                # We do nothing with it for the moment
                # Some servers give Null for continue and "" for the uneventful finish reason
                # Some other gives "" for continue and a non empty string for finish reason
                # So do not trust anybody and continue the connection until the server closes it
                logger.debug("Chunk: finish reason: %s", finish_reason)

            timings = data.get("timings")
            if timings:
                processed = True
                self.completion_metrics.update(timings)

            usage = data.get("usage")
            if usage:
                processed = True
                self.completion_metrics.update(usage)

            model = data.get("model")
            if model and self.answering_model != model:
                logger.warning("Unexpected answering model: got %s instead of %s", model, self.model)
                self.answering_model = model

            if not processed:
                logger.info("Chunk: Unexpected content: %s", data)
                continue
            elif first_token:
                first_token_time = time.perf_counter()
                self.completion_metrics["first_token_ms"] = (first_token_time - start_time) * 1000.0
                first_token = False

            #FIXME: this is fragile and ugly.
            if self.config.tool_mode == "markdown" and message.get('content'):
                cb = re.search(r"^```run([^\n]*)\n(.*?)^```$", message['content'], re.DOTALL | re.MULTILINE)
                if not cb:
                    continue
                tool_calls = message.get("tool_calls")
                if tool_calls is None:
                    tool_calls = message['tool_calls'] = []
                arguments = {"command": cb[1], "stdin": cb[2]}
                tool_call = {
                    "id": f"toolcallid-{len(self.history)}-{len(tool_calls)}",
                    "type": "function",
                    "function": {"name": "run_command", "arguments": json.dumps(arguments)}}
                tool_calls.append(tool_call)
                # Force the LLM to stop once a tool call is found
                break

        cp.end()
        logger.debug("Chunk: Last one: %s", last_chunk)
        response.close()
        self.dump_raw_response(message)
        meta["model"] = self.model
        meta["answering_model"] = self.answering_model
        message["llme-meta"] = meta
        return message


    def chat_completion(self, tools=None):
        """Post messages and get a response from the LLM."""
        self.completion_metrics = {}
        start_time = time.perf_counter()
        self.completion_metrics["chunk_n"] = 0
        self.completion_metrics["message_n"] = 1 # only one

        with Spinner("light_blue", self.config.plain):
            response = self.post_chat_completion(tools)
            response.raise_for_status()

        response_time = time.perf_counter()
        self.completion_metrics["response_ms"] = (response_time - start_time) * 1000.0

        if not self.config.plain:
            cprint(f"{self.prompt_prefix()}< ", "light_blue", end='', flush=True)

        message = self.receive_chat_completion_message(response)
        message_time = time.perf_counter()
        self.completion_metrics["total_ms"] = (message_time - start_time) * 1000.0
        meta = message["llme-meta"]
        meta["metrics"] = self.update_metrics()
        return message


    def update_metrics(self):
        """Display metrics information, and update the global metrics information"""
        data = self.completion_metrics
        logger.info("metrics: %s", data)
        if not "first_token_ms" in data:
            data["first_token_ms"] = 0.0
        data["last_token_ms"] = data["total_ms"] - data["first_token_ms"] - data["response_ms"]
        self.metrics.update(data)

        cprint(self.metrics.infoline(data, self), "light_grey")

        if self.config.export_metrics:
            try:
                with open(self.config.export_metrics, "w") as file:
                    json.dump({"total": self.metrics.total, "history": self.metrics.history}, file, indent=2)
            except OSError as e:
                raise AppError(f"Can't save metrics to {self.config.export_metrics}") from e
        return data


    def get_throttling_delay(self, e):
        """Extract throttling delay from headers"""
        if getattr(e, "response", None) is None: # httpx transport errors have no response
            return
        for h in ['retry-after', 'x-ratelimit-reset-requests', 'x-ratelimit-reset-tokens']:
            v = e.response.headers.get(h)
            if not v:
                continue
            logger.debug("throttling header %s=%s", h, v)
            if v[-1] == 's':
                v = v[:-1]
            try:
                return int(v)
            except:
                pass
        if e.response.status_code == 429:
            # Default throttling
            return 60
        return None

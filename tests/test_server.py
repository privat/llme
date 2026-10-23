"""Tests for interactions with a real OpenAI-compatible server.

--dummy-responses cannot simulate what happens at the http layer: HTTP errors,
connection failures, timeouts, throttling (429 + retry headers), model
listing, non-streaming and broken SSE streams. These tests run the real
LLME code path (loop, chat_completion, get_models, start) against a local
mock HTTP server, over a real socket, with the real httpx client.
"""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import httpx
import pytest

from llme.config import Config, build_parser
from llme.errors import AppError
from llme.main import LLME
from llme.server import extract_requests_error


# --- Mock server -----------------------------------------------------------------

class MockServer:
    """Local http server answering queued canned responses, recording all requests."""

    def __init__(self):
        self.requests = []  # recorded requests: {"method", "path", "headers", "body"}
        self.queue = []  # pending responses: (status, headers, body, delay)
        self.lock = threading.Lock()
        server = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass  # silence the per-request log

            def do_GET(self):
                self.respond("GET")

            def do_POST(self):
                self.respond("POST")

            def respond(self, method):
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length)
                with server.lock:
                    server.requests.append({
                        "method": method,
                        "path": self.path,
                        "headers": dict(self.headers),
                        "body": json.loads(raw) if raw else None,
                    })
                    response = server.queue.pop(0) if server.queue else (500, {}, b"unexpected request", 0)
                status, headers, body, delay = response
                if delay:
                    # threading.Event.wait, not time.sleep: tests may patch time.sleep without affecting the server
                    threading.Event().wait(delay)
                self.send_response(status)
                for name, value in headers.items():
                    self.send_header(name, value)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        self.httpd = _ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.httpd.handle_error = lambda *args: None  # the timeout tests abandon the in-flight request
        # a small poll_interval makes shutdown() snappy (default is 0.5s per server)
        threading.Thread(target=lambda: self.httpd.serve_forever(poll_interval=0.05), daemon=True).start()
        self.base_url = f"http://127.0.0.1:{self.httpd.server_address[1]}/v1"

    def add(self, status, body, headers=None, delay=0):
        """Queue a canned response (dict, str or bytes body)."""
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode()
        elif isinstance(body, str):
            body = body.encode()
        with self.lock:
            self.queue.append((status, headers or {}, body, delay))

    def chat_requests(self):
        return [r for r in self.requests if r["path"] == "/v1/chat/completions"]

    def shutdown(self):
        self.httpd.shutdown()
        self.httpd.server_close()


class _ThreadingHTTPServer(ThreadingHTTPServer):
    daemon_threads = True  # abandoned handlers (timeout tests) must not block the exit


def sse(chunks):
    """Build an SSE body from a list of json dicts and/or '[DONE]' markers."""
    return "".join(
        f"data: {chunk if isinstance(chunk, str) else json.dumps(chunk)}\n\n" for chunk in chunks
    ).encode()


def ok_stream(content, model="test-model", usage=None):
    """A standard chat completion stream, split in two content chunks."""
    mid = max(1, len(content) // 2)
    chunks = [
        {"choices": [{"delta": {"role": "assistant", "content": content[:mid]}}]},
        {"choices": [{"delta": {"content": content[mid:], "finish_reason": "stop"}}], "model": model},
    ]
    if usage:
        chunks[-1]["usage"] = usage
    return sse(chunks + ["[DONE]"])


# --- fixtures -----------------------------------------------------------------------

@pytest.fixture
def server():
    srv = MockServer()
    yield srv
    srv.shutdown()


@pytest.fixture
def app(server):
    """A real LLME (batch mode, no prompt_toolkit) pointed at the mock server."""
    parser = build_parser()
    config = Config(parser)
    parser.parse_args([], namespace=config)
    config.batch = True  # sessionless path, errors propagate
    config.plain = True  # no tty decoration, single-sleep throttling
    config.base_url = server.base_url
    config.timeout_http = 5
    config.api_key = "sk-test"
    llme = LLME(config)
    llme.model = "test-model"
    return llme


def run(llme, prompt="hello"):
    """Process one prompt through the full ping-pong loop (batch mode)."""
    llme.prompts = [prompt]
    llme.loop()


# --- chat completion streams -----------------------------------------------------------

def test_ok_stream(server, app):
    server.add(200, ok_stream("hello world", usage={"prompt_tokens": 4, "completion_tokens": 2}),
               {"Content-Type": "text/event-stream"})
    run(app)
    message = app.history[-1].data
    assert message["role"] == "assistant"
    assert message["content"] == "hello world"
    assert message["llme-meta"]["answering_model"] == "test-model"
    # the request really sent to the server
    (req,) = server.chat_requests()
    assert req["body"]["model"] == "test-model"
    assert req["body"]["messages"] == [{"role": "user", "content": "hello"}]
    assert req["body"]["stream"] is True
    assert req["body"]["stream_options"] == {"include_usage": True}
    assert req["headers"]["Authorization"] == "Bearer sk-test"
    # metrics are fed by the usage chunk
    assert app.metrics.total["prompt_tokens"] == 4


def test_non_streaming_json_response(server, app):
    """A single non-SSE json completion, as some servers answer."""
    body = {
        "id": "chatcmpl-1", "model": "test-model",
        "choices": [{"index": 0,
                     "message": {"role": "assistant", "content": "whole message"},
                     "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 3, "completion_tokens": 2},
    }
    server.add(200, body, {"Content-Type": "application/json"})
    run(app)
    assert app.history[-1].data["content"] == "whole message"
    assert app.metrics.total["prompt_tokens"] == 3


def test_malformed_chunks_are_skipped(server, app):
    """Garbage SSE lines and invalid json chunks must not break the stream."""
    body = (": keep-alive comment\n\nevent: ping\n\ndata: {not json}\n\n").encode()
    body += sse([{"choices": [{"delta": {"role": "assistant", "content": "ok"}, "finish_reason": "stop"}]}])
    server.add(200, body, {"Content-Type": "text/event-stream"})
    run(app)
    assert app.history[-1].data["content"] == "ok"


def test_stream_closed_early(server, app):
    """The server may close the connection without [DONE]: the message ends as is."""
    server.add(200, sse([{"choices": [{"delta": {"role": "assistant", "content": "partial"}}]}]),
               {"Content-Type": "text/event-stream"})
    run(app)
    assert app.history[-1].data["content"] == "partial"


# --- http errors -------------------------------------------------------------------------

@pytest.mark.parametrize("status, headers, body, expected", [
    (404, {"Content-Type": "application/json"},
     {"error": {"message": "model not found"}}, "model not found"),
    (401, {"Content-Type": "text/plain"}, "Invalid API key provided", "Invalid API key"),
    (500, {"Content-Type": "text/html"},
     "<html><body><h1>Internal Server Error</h1></body></html>", "Internal Server Error"),
    (403, {"Content-Type": "text/plain"}, "<forbidden>nope</forbidden>", "nope"),
])
def test_http_error(server, app, status, headers, body, expected):
    server.add(status, body, headers)
    with pytest.raises(httpx.HTTPStatusError) as exc:
        run(app)
    message = extract_requests_error(exc.value)
    assert expected in message
    assert f"({status} {server.base_url}/chat/completions)" in message
    assert "<" not in message  # html tags are stripped


def test_long_error_body_is_truncated(server, app):
    server.add(500, "x" * 300)
    with pytest.raises(httpx.HTTPStatusError) as exc:
        run(app)
    message = extract_requests_error(exc.value)
    assert "..." in message
    assert len(message) < 300


def test_connection_refused(app):
    app.config.base_url = "http://127.0.0.1:1/v1"  # a closed port
    with pytest.raises(httpx.ConnectError) as exc:
        run(app)
    message = extract_requests_error(exc.value)
    assert "http://127.0.0.1:1/v1/chat/completions" in message


def test_read_timeout(server, app):
    app.config.timeout_http = 1
    server.add(200, ok_stream("too late"), {"Content-Type": "text/event-stream"}, delay=3)
    with pytest.raises(httpx.ReadTimeout) as exc:
        run(app)
    message = extract_requests_error(exc.value)
    assert "chat/completions" in message


# --- throttling ---------------------------------------------------------------------------

class TestThrottling:
    """429 responses: llme sleeps the announced delay and retries the same request."""

    @pytest.fixture
    def sleep(self, monkeypatch):
        calls = []
        monkeypatch.setattr("time.sleep", lambda s: calls.append(s))
        return calls

    def _queue_429_ok(self, server, headers):
        server.add(429, "rate limited", {"Content-Type": "text/plain", **headers})
        server.add(200, ok_stream("finally"), {"Content-Type": "text/event-stream"})

    def test_retry_after(self, server, app, sleep):
        self._queue_429_ok(server, {"Retry-After": "1"})
        run(app)
        assert app.history[-1].data["content"] == "finally"
        assert sleep == [1]
        assert len(server.chat_requests()) == 2

    def test_ratelimit_reset_header(self, server, app, sleep):
        self._queue_429_ok(server, {"x-ratelimit-reset-requests": "3"})
        run(app)
        assert sleep == [3]

    def test_seconds_suffix(self, server, app, sleep):
        self._queue_429_ok(server, {"Retry-After": "2s"})
        run(app)
        assert sleep == [2]

    def test_default_delay(self, server, app, sleep):
        """A 429 without any retry header waits the default 60s."""
        self._queue_429_ok(server, {})
        run(app)
        assert sleep == [60]

    def test_non_numeric_header_is_ignored(self, server, app, sleep):
        self._queue_429_ok(server, {"Retry-After": "soon"})
        run(app)
        assert sleep == [60]

    def test_retries_until_success(self, server, app, sleep):
        server.add(429, "wait", {"Retry-After": "1"})
        server.add(429, "wait", {"x-ratelimit-reset-requests": "3"})
        server.add(200, ok_stream("done"), {"Content-Type": "text/event-stream"})
        run(app)
        assert app.history[-1].data["content"] == "done"
        assert sleep == [1, 3]
        bodies = [r["body"] for r in server.chat_requests()]
        assert len(bodies) == 3
        assert all(body == bodies[0] for body in bodies)  # the same request is resent


# --- model listing ---------------------------------------------------------------------------

def test_get_models_states(server, app):
    server.add(200, {"data": [{"id": "a"}, {"id": "b", "status": {"value": "loaded"}}]},
               {"Content-Type": "application/json"})
    models = app.get_models()
    assert {m["id"]: m["state"] for m in models} == {"a": None, "b": "loaded"}


def _queue_models(server, data):
    body = {"data": data}
    # both start() and list_models() fetch the model list
    server.add(200, body, {"Content-Type": "application/json"})
    server.add(200, body, {"Content-Type": "application/json"})


def test_start_picks_first_loaded_model(server, app):
    app.model = None
    app.config.model = None
    app.config.list_models = True
    _queue_models(server, [
        {"id": "slow", "status": {"value": "unloaded"}},
        {"id": "fast", "status": {"value": "loaded"}},
        {"id": "plain"},
    ])
    app.start()
    assert app.model == "fast"
    assert server.requests[0]["path"] == "/v1/models"


def test_start_picks_first_when_none_loaded(server, app):
    app.model = None
    app.config.model = None
    app.config.list_models = True
    _queue_models(server, [{"id": "b"}, {"id": "c"}])
    app.start()
    assert app.model == "b"


def test_start_without_models(server, app):
    app.model = None
    server.add(500, "server down")
    with pytest.raises(AppError, match="Can't get models"):
        app.start()


# --- get_throttling_delay (unit, no server) ----------------------------------------------------

def make_http_error(status, headers=None):
    request = httpx.Request("POST", "http://mock/v1/chat/completions")
    response = httpx.Response(status, headers=headers or {}, request=request, text="error")
    return httpx.HTTPStatusError("server error", request=request, response=response)


@pytest.mark.parametrize("headers, expected", [
    ({"retry-after": "5"}, 5),
    ({"retry-after": "5s"}, 5),  # seconds suffix
    ({"retry-after": "5", "x-ratelimit-reset-tokens": "9"}, 5),  # retry-after wins
    ({"x-ratelimit-reset-requests": "7"}, 7),
    ({"x-ratelimit-reset-tokens": "8"}, 8),
    ({"retry-after": "soon"}, 60),  # non numeric, fall back to the default
    ({}, 60),  # 429 default
    ({"x-ratelimit-reset-requests": "1791674509"}, 60),  # epoch timestamp, not a duration
    ({"retry-after": "999999999"}, 60),  # implausibly large
])
def test_get_throttling_delay_429(app, headers, expected):
    assert app.get_throttling_delay(make_http_error(429, headers)) == expected


def test_get_throttling_delay_other_status(app):
    """Other statuses are retried only when they announce a delay."""
    assert app.get_throttling_delay(make_http_error(500)) is None
    assert app.get_throttling_delay(make_http_error(401)) is None
    assert app.get_throttling_delay(make_http_error(503, {"retry-after": "2"})) == 2


def test_get_throttling_delay_transport_error(app):
    error = httpx.ConnectError("boom", request=httpx.Request("GET", "http://mock/"))
    assert app.get_throttling_delay(error) is None

#!/usr/bin/env python3

# Copyright (C) 2025 Dory
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import re
import json
import argparse
import requests
import base64
import mimetypes
from termcolor import colored, cprint
from rich.console import Console
import itertools
import threading
import time
import tomllib
from sseclient import SSEClient

def parse_image(user_input):
  parts = user_input.split("@image:")
  if len(parts) > 2 or not user_input.endswith(parts[1]):
    raise ValueError("'@image:' tag must be at the end of the prompt.")

  text_prompt = parts[0].strip()
  image_path = parts[1].strip()

  if image_path.startswith(("http://", "https://")):
    image_url = image_path

  else:
    if not os.path.exists(image_path):
      raise ValueError(f"Error: Image file not found at '{image_path}'")

    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type or not mime_type.startswith('image/'):
      raise ValueError(f"Error: Unsupported image type '{mime_type}'")

    with open(image_path, "rb") as image_file:
      encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    image_url = f"data:{mime_type};base64,{encoded_image}"

  return text_prompt, image_url


def get_model_name(base_url, model):
  response = requests.get(f"{base_url}/models")
  response.raise_for_status()
  models = response.json()

  if not model:
    return models["data"][0]["id"]

  for m in models["data"]:
    if m["id"] == model:
      return m["id"]

  ids = [m["id"] for m in models["data"]]
  raise ValueError(f"Error: Model '{model}' not found. Available: {', '.join(ids)}")


def print_response(console, response, hide_thinking):
  content = response["content"]
  if "reasoning_content" in response and response["reasoning_content"]:
    thinking_text = response["reasoning_content"]
    answer_text = content
  else:
    answer_marker = None
    if "<answer>" in content:
      answer_marker = "<answer>"
    elif "<|end|>" in content:
      answer_marker = "<|end|>"

    if not answer_marker:
      thinking_text = ""
      answer_text = content
    else:
      parts = content.split(answer_marker, 1)
      thinking_text = parts[0].strip()
      answer_text = parts[1].strip()

  if not hide_thinking and thinking_text:
    cprint(thinking_text + "\n", "magenta")
  console.print(answer_text)

def run(tool, stdin):
    import subprocess

    x = input(colored("RUN [Yn]? ", "red", attrs=["bold"]))
    if not x in ['', 'y', 'Y']:
        raise

    resultat = subprocess.run(
        [tool],
        input=stdin,
        text=True,            # pour que `input` soit interprété comme une chaîne (et non bytes)
        capture_output=True   # pour capturer stdout/stderr
    )

    print(repr(resultat))
    return {"role":"system", "content":repr(resultat)}


def animate(stop_event):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        sys.stdout.write(f'\r{colored(c, "green", attrs=["bold"])} ')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r')
    sys.stdout.flush()


def main(base_url, model, api_key, hide_thinking, no_stream, system_prompt, prompts):
  model_name = get_model_name(base_url, model)
  if sys.stdin.isatty():
    print(f"Using model: {model_name}")

  messages = []
  if system_prompt:
    messages.append({"role": "system", "content": system_prompt})
  console = Console()

  while True:
    try:
      if len(prompts) > 0:
        user_input = prompts[0]
        prompts = prompts[1:]
        if sys.stdin.isatty():
          print(colored("> ", "green", attrs=["bold"]), user_input)
      elif sys.stdin.isatty():
        print()
        user_input = input(colored("> ", "green", attrs=["bold"]))
        print()
      else:
        user_input = input()

      if "@image:" in user_input:
        try:
          text_prompt, image_url = parse_image(user_input)
        except ValueError as e:
          cprint(e, "red")
          continue
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": text_prompt},
                {"type": "image_url", "image_url": {"url": image_url}},
            ]
        })

      elif user_input != '':
        messages.append({"role": "user", "content": user_input})

      if sys.stdin.isatty():
        stop_event = threading.Event()
        animation_thread = threading.Thread(target=animate, args=(stop_event,))
        animation_thread.start()

      try:
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"model": model_name, "messages": messages, "stream": not no_stream},
            stream=not no_stream
        )
        if not no_stream:
          response.raise_for_status()
      finally:
        if sys.stdin.isatty():
          stop_event.set()
          animation_thread.join()

      if no_stream:
        assistant_message = response.json()["choices"][0]["message"]
        messages.append(assistant_message)
        print_response(console, assistant_message, hide_thinking)
      else:
        full_content = ''
        cb=None
        for event in SSEClient(response).events():
          if event.data == "[DONE]":
            break
          data = json.loads(event.data)
          choice0 = data['choices'][0]
          if choice0['finish_reason'] == 'stop':
            break
          content = choice0['delta']['content']
          if content is None:
            continue
          full_content += content
          print(content, end='', flush=True)
          cb = re.search(r"```run ([\w+-]*)\n(.*?)```", full_content, re.DOTALL)
          if cb:
            break
        response.close()
        messages.append({"role":"agent","content":full_content})
        if cb:
          r = run(cb[1], cb[2])
          messages.append(r)

    except requests.exceptions.RequestException as e:
      print(response.content)
      raise e
    except (KeyboardInterrupt, EOFError):
      break

def apply_config(args, config):
  """
  Use default config value is absent from args.
  The method is a little ugly but it works...
  """
  variables = vars(args)
  for k in variables:
    if variables[k] is None and k in config:
      setattr(args, k, config[k])

if __name__ == "__main__":

  config_path = os.path.join(os.environ.get("HOME"), ".config", "llme", "config.toml")
  parser = argparse.ArgumentParser(description="OpenAI-compatible chat CLI")
  parser.add_argument("-u", "--base-url", help="API base URL")
  parser.add_argument("-m", "--model", help="Model name")
  parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY"))
  parser.add_argument("-s", "--system", dest="system_prompt", help="System prompt")
  parser.add_argument("--hide-thinking", action="store_true")
  parser.add_argument("--no-stream", action="store_true")
  parser.add_argument("-c", "--config", help="Custom configuration file")
  parser.add_argument("prompts", nargs="*", help="Sequence of prompts")

  args = parser.parse_args()

  if args.config or os.path.exists(config_path):
    with open(args.config or config_path, "rb") as f:
      config = tomllib.load(f)
    apply_config(args, config)
  del(args.config)

  if args.base_url is None:
      print("Error: --base-url required and not definied the config file.", file=sys.stderr)
      sys.exit(1)

  main(**vars(args))

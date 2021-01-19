import sys
import os
import signal
import warnings
import webbrowser
import json
import curses
import argparse

# local

try:
  # need when 「cat fixtures/rust.json | bin/gfzs」
  from gfzs import tty, info
  from gfzs.utils import debug
  from gfzs.controller import Controller

# need when 「cat fixtures/rust.json | python -m gfzs」
except ModuleNotFoundError:
  from utils import debug
  from controller import Controller


def validate(data):
  data = []
  for item in data:
    if 'url' in item:
      data.append(True)
    else:
      data.append(False)

    if 'abstract' in item:
      data.append(True)
    else:
      data.append(False)

    if 'url' in item:
      data.append(True)
    else:
      data.append(False)

  return all(data)


def open_tty(ttyname):
    # See https://github.com/stefanholek/term/issues/1
    return open(ttyname, "wb+", buffering=0)

def parse_args():
  parser = argparse.ArgumentParser(description='Google Fuzzy Search')
  parser.add_argument('--version', action='version', version=info.__version__)
  parser.add_argument('--score', '-s', type=int, default=30, help="fuzzywuzzy's score")
  
  return parser.parse_args()

def main() -> None:
  args = parse_args()

  signal.signal(signal.SIGINT, signal.SIG_DFL)
  # https://note.nkmk.me/python-warnings-ignore-warning/
  warnings.simplefilter('ignore', FutureWarning)

  data = None
  error = None

  ttyname = tty.get_ttyname()

  with open_tty(ttyname) as tty_f:
    _ = tty.reconnect_descriptors(tty_f)

    try:
      json_str = sys.stdin.read()
      data = json.loads(json_str)
      if not validate(data):
        raise Exception("Invalid JSON Format.")
    except json.decoder.JSONDecodeError as e:
      error = e
    except Exception as e:
      error = e
    finally:
      if error != None:
        print(error)
        sys.exit(1)

    controller = Controller(data)
    try:
      _ = controller.run()
    except curses.error as e:
      error = e
    except Exception as e:
      error = e
    finally:
      controller._end_curses()
      if error != None:
        print(error)
        sys.exit(1)

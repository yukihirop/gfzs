import sys
import os
import signal
import warnings
import webbrowser
import json
import curses

# local

try:
  from gfzs import debug, tty
  from gfzs.controller import Controller
except:
  import debug
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

def main() -> None:
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  # https://note.nkmk.me/python-warnings-ignore-warning/
  warnings.simplefilter('ignore', FutureWarning)

  data = None
  error = None

  ttyname = tty.get_ttyname()

  with open_tty(ttyname) as tty_f:
    descriptors = tty.reconnect_descriptors(tty_f)

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
      choice = controller.run()
      result = controller.model.result
      if not choice is None:
          webbrowser.open(result[choice].get('url'), new=2)
    except curses.error as e:
      error = e
    except Exception as e:
      error = e
    finally:
      controller._end_curses()
      if error != None:
        print(error)
        sys.exit(1)

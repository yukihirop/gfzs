#coding:utf-8

import os
import sys
import json
import subprocess

# local

try:
  # need when 「python3 gfzs/cmd/config.py」
  if __name__ == '__main__':
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))))
    import debug
    from config.app import AppConfig

  # need when 「cat fixtures/rust.json | python -m gfzs」
  # need when 「cat fixtures/rust.json | bin/gfzs」
  else:
    from gfzs.utils import debug
    from gfzs.config.app import AppConfig

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
  # https://codechacha.com/ja/how-to-import-python-files/
  sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('../'))))
  from utils import debug
  from config.app import AppConfig


def main():
  app_config = AppConfig.get_instance()
  config_path = app_config.config_path

  if os.path.exists(config_path):
    if os.environ["EDITOR"] != '':
      subprocess.call([os.environ["EDITOR"], config_path])
    else:
      print("Set the environment variable 'EDITOR'")
  else:
    print("Config does not exist in %s" % config_path)

  sys.exit(0)


if __name__ == '__main__':
  main()
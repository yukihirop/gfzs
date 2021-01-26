# coding:utf-8

import os
import sys
import json
import subprocess

# local

try:
    # need when 「python3 gfzs/cmd/config.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        import debug
        from runtime.config import RuntimeConfig

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.utils import debug
        from gfzs.runtime.config import RuntimeConfig

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from utils import debug
    from runtime.config import RuntimeConfig


def main():
    runtime_config = RuntimeConfig.get_instance()
    config_path = runtime_config.config_path

    try:
        if os.path.exists(config_path):
            if os.environ["EDITOR"] != "":
                try:
                    subprocess.call([os.environ["EDITOR"], config_path])
                    sys.exit(0)
                except Exception:
                    raise Exception("Set the command to launch the editor in 'EDITOR'.")
            else:
                raise Exception("Set the environment variable 'EDITOR'")
        else:
            raise Exception("Config does not exist in %s" % config_path)
    except Exception as e:
        print("Error: %s" % str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()

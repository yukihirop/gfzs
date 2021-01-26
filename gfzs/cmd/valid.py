# coding:utf-8

import json
import os, sys
import signal
import warnings

# local

try:
    # need when 「python3 gfzs/cmd/valid.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        from runtime.config import RuntimeConfig

        if os.environ.get("DEBUG"):
            import debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.runtime.config import RuntimeConfig

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from runtime.config import RuntimeConfig

    if os.environ.get("DEBUG"):
        import utils.debug as debug


def main():
    runtime_config = RuntimeConfig.get_instance()
    if runtime_config.valid():
        print("Config is valid.")
    else:
        print("Config is invalid.")
        for error in runtime_config.errors:
            print("Error: %s" % error)

    sys.exit(0)


if __name__ == "__main__":
    main()

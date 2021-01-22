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
        from config.app import AppConfig

        if os.environ.get("DEBUG"):
            import debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.config.app import AppConfig

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from config.app import AppConfig

    if os.environ.get("DEBUG"):
        import utils.debug as debug


def main():
    app_config = AppConfig.get_instance()
    if app_config.valid():
        print("Config is valid.")
    else:
        print("Config is invalid.")
        for error in app_config.errors:
            print("Error: %s" % error)

    sys.exit(0)


if __name__ == "__main__":
    main()

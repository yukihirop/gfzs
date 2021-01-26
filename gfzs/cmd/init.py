# coding:utf-8

import os
import sys
import json

# local

try:
    # need when 「python3 gfzs/cmd/init.py」
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
    data = runtime_config.data

    if os.path.exists(config_path):
        print("Reinitialized existing in %s" % config_path)
    else:
        with open(config_path, mode="w") as f:
            f.write(json.dumps(data, indent=2))
            print("Initialize config in %s" % config_path)

    sys.exit(0)


if __name__ == "__main__":
    main()

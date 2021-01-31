# coding:utf-8

import json
import os, sys
import signal
import warnings
import argparse
from typing import Optional

# local

try:
    # need when 「python3 gfzs/cmd/valid.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        from runtime.config import RuntimeConfig
        from utils.logger import Logger

        if os.environ.get("DEBUG"):
            import debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.runtime.config import RuntimeConfig
        from gfzs.utils.logger import Logger

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from runtime.config import RuntimeConfig
    from utils.logger import Logger

    if os.environ.get("DEBUG"):
        import utils.debug as debug


def main(args: Optional[argparse.Namespace] = None):
    progname = "gfzs.cmd.valid"
    logger = Logger.get_instance(progname, args.log_path)
    logger.set_level(args.log_level)
    logger.debug("start %s" % progname)

    runtime_config = RuntimeConfig.get_instance()
    if runtime_config.valid():
        logger.debug("[print] Config is valid.")
        print("Config is valid.")
    else:
        logger.debug("[print] Config is invalid.")
        print("Config is invalid.")
        for error in runtime_config.errors:
            logger.error(error)
            print("Error: %s" % error)

    logger.debug("exit 0")
    logger.debug("end %s" % progname, new_line=True)
    sys.exit(0)


if __name__ == "__main__":
    args = argparse.Namespace
    args.log_path = "./tmp/gfzs.log"
    args.log_level = 0

    main(args)

# coding:utf-8

import os
import sys
import json
import argparse

# local

try:
    # need when 「python3 gfzs/cmd/init.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        import runtime.config as runtime_config
        import utils.logger as logger

        if os.environ.get("DEBUG"):
            import debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        import gfzs.runtime.config as runtime_config
        import gfzs.utils.logger as logger

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    import runtime.config as runtime_config
    import utils.logger as logger

    if os.environ.get("DEBUG"):
        import utils.debug as debug


def main(args: argparse.Namespace):
    progname = "gfzs.cmd.init"
    properties = {
        "progname": progname,
        "severity": int(args.log_level),
        "log_path": args.log_path,
    }
    logger.init_properties(**properties)
    logger.debug("start %s" % progname)

    runtime_config.init()
    config_path = runtime_config.config_path
    data = runtime_config.data

    if os.path.exists(config_path):
        logger.debug("[print] 'Reinitialized existing in %s'" % config_path)
        print("Reinitialized existing in %s" % config_path)
    else:
        logger.debug("[print] 'Initialize config in %s'" % config_path)
        with open(config_path, mode="w") as f:
            f.write(json.dumps(data, indent=2))
            print("Initialize config in %s" % config_path)

    logger.debug("exit 0")
    logger.debug("end %s" % progname, new_line=True)
    sys.exit(0)


if __name__ == "__main__":
    args = argparse.Namespace()
    args.log_path = "./tmp/gfzs.log"
    args.log_level = 0

    main(args)

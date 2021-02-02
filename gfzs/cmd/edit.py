# coding:utf-8

import os
import sys
import json
import subprocess
import argparse

# local

try:
    # need when 「python3 gfzs/cmd/config.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        import runtime.config as runtime_config
        import utils.logger as logger

        if os.environ.get("DEBUG"):
            import utils.debug as debug

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
    progname = "gfzs.cmd.edit"
    properties = {
        "progname": progname,
        "severity": int(args.log_level),
        "log_path": args.log_path,
    }
    logger.init_properties(**properties)
    logger.debug("start %s" % progname)

    runtime_config.init()
    config_path = runtime_config.config_path

    try:
        if os.path.exists(config_path):
            logger.debug("runtime config file exist")
            if os.environ["EDITOR"] != "":
                try:
                    logger.debug("open editor")
                    subprocess.call([os.environ["EDITOR"], config_path])
                    logger.debug("exit 0")
                    logger.debug("end %s" % progname, new_line=True)
                    sys.exit(0)
                except Exception:
                    raise Exception("Set the command to launch the editor in 'EDITOR'.")
            else:
                raise Exception("Set the environment variable 'EDITOR'")
        else:
            raise Exception("Config does not exist in %s" % config_path)
    except Exception as e:
        logger.error(e)
        print("Error: %s" % str(e))
        logger.debug("exit 1")
        logger.debug("end %s" % progname, new_line=True)
        sys.exit(1)


if __name__ == "__main__":
    args = argparse.Namespace()
    args.log_path = "./tmp/gfzs.log"
    args.log_level = 0

    main(args)

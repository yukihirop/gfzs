# Copy from https://github.com/mooz/percol/blob/master/percol/tty.py

# -*- coding: utf-8 -*-

import sys
import os

# local

try:
    # need when 「python3 gfzs/tty.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        import utils.logger as logger

        if os.environ.get("DEBUG"):
            import utils.debug as debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        import gfzs.utils.logger as logger

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    import utils.logger as logger

    if os.environ.get("DEBUG"):
        import utils.debug as debug


def get_ttyname():
    for f in sys.stdin, sys.stdout, sys.stderr:
        if f.isatty():
            return os.ttyname(f.fileno())
    return None


def reconnect_descriptors(tty):
    target = {}

    stdios = (("stdin", "r"), ("stdout", "w"), ("stderr", "w"))

    tty_desc = tty.fileno()

    for name, mode in stdios:
        f = getattr(sys, name)

        if f.isatty():
            # f is TTY
            target[name] = f
        else:
            # f is other process's output / input or a file

            # save descriptor connected with other process
            std_desc = f.fileno()
            other_desc = os.dup(std_desc)

            # set std descriptor. std_desc become invalid.
            os.dup2(tty_desc, std_desc)

            # set file object connected to other_desc to corresponding one of sys.{stdin, stdout, stderr}
            try:
                target[name] = os.fdopen(other_desc, mode)
                setattr(sys, name, target[name])
            except OSError:
                # maybe mode specification is invalid or /dev/null is specified (?)
                target[name] = None
                error = "Error: Failed to open '{0}'".format(other_desc)
                logger.error(error)
                print(error)

    return target

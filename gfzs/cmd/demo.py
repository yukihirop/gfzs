# coding:utf-8

import json
import os, sys
import signal
import warnings
import curses
import argparse

# local

try:
    # need when 「python3 gfzs/cmd/demo.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        from controller import Controller
        import runtime.config as runtime_config
        import runtime.opts as runtime_opts
        import utils.logger as logger

        if os.environ.get("DEBUG"):
            import utils.debug as debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.controller import Controller
        import gfzs.runtime.config as runtime_config
        import gfzs.runtime.opts as runtime_opts
        import gfzs.utils.logger as logger

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from controller import Controller
    import runtime.config as runtime_config
    import runtime.opts as runtime_opts
    import utils.logger as logger

    if os.environ.get("DEBUG"):
        import utils.debug as debug

DEMO_JSON_DATA = [
    {
        "abstract": "Python 3.9.1 - Python 3.8.7 - Mac OS X - Python 3.9.0 - Python 3.7.9",
        "sitelinks": [
            {
                "abstract": "Python 3.9.1 - Python 3.8.7 - Mac OS X - Python 3.9.0 - Python 3.7.9",
                "index": "1a",
                "title": "Downloads",
                "url": "https://www.python.org/downloads/",
            },
            {
                "abstract": "3.9.1 is the first version of Python to support macOS 11 Big Sur.",
                "index": "1b",
                "title": "Python 3.9.1",
                "url": "https://www.python.org/downloads/release/python-391/",
            },
            {
                "abstract": "Python's documentation, tutorials, and guides are constantly ...",
                "index": "1c",
                "title": "Documentation",
                "url": "https://www.python.org/doc/",
            },
            {
                "abstract": "Tutorial - Standard Library - Python Language - Python Module Index",
                "index": "1d",
                "title": "Python Docs",
                "url": "https://docs.python.org/",
            },
            {
                "abstract": "BeginnersGuide/Download - Python for Programmers - IDEs",
                "index": "1e",
                "title": "Python For Beginners",
                "url": "https://www.python.org/about/gettingstarted/",
            },
            {
                "abstract": "1. Whetting Your Appetite - 5. Data Structures - 9. Classes - ...",
                "index": "1f",
                "title": "Tutorial",
                "url": "https://docs.python.org/3/tutorial/",
            },
        ],
        "title": "Downloads",
        "url": "https://www.python.org/downloads/",
    },
    {
        "abstract": "Python is an interpreted, high-level and general-purpose programming language. Python's design philosophy emphasizes code readability with its notable use ...",
        "matches": [
            {"offset": 0, "phrase": "Python"},
            {"offset": 79, "phrase": "Python's"},
        ],
        "metadata": "Developer: Python Software Foundation | Designed by: Guido van Rossum | Filename extensions: .py,.pyi,.pyc,.pyd,.pyo ... | Typing discipline: Duck, dynamic, gradual (since ...",
        "title": "Python (programming language) - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    },
    {
        "abstract": "プログラミング言語 Pythonの紹介・ダウンロードとインストール・Python入門講座など.",
        "matches": [
            {"offset": 10, "phrase": "Python"},
            {"offset": 34, "phrase": "Python"},
        ],
        "title": "プログラミング言語 Python - python.jp",
        "url": "https://www.python.jp/",
    },
    {
        "abstract": "Python · Great first language · Large programming community · Excellent online documentation · Endless libraries and packages · World-wide popularity · Powerful ...",
        "matches": [{"offset": 0, "phrase": "Python"}],
        "title": "Python Courses & Tutorials | Codecademy",
        "url": "https://www.codecademy.com/catalog/language/python",
    },
    {
        "abstract": "Well organized and easy to understand Web building tutorials with lots of examples of how to use HTML, CSS, JavaScript, SQL, PHP, Python, Bootstrap, Java ...",
        "matches": [{"offset": 130, "phrase": "Python"}],
        "title": "Python Tutorial - W3Schools",
        "url": "https://www.w3schools.com/python/",
    },
    {
        "abstract": "The Python Package Index (PyPI) is a repository of software for the Python programming language.",
        "matches": [
            {"offset": 4, "phrase": "Python"},
            {"offset": 68, "phrase": "Python"},
        ],
        "title": "PyPI · The Python Package Index",
        "url": "https://pypi.org/",
    },
]


def main(args: argparse.Namespace):
    progname = "gfzs.cmd.demo"
    properties = {
        "progname": progname,
        "severity": int(args.log_level),
        "log_path": args.log_path,
    }
    logger.init_properties(**properties)
    logger.debug("start %s" % progname)

    def handle_sigint(signum, fframe) -> None:
        logger.debug("detect SIGINT (Ctrl-c)")
        logger.debug("exit 0")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)
    warnings.simplefilter("ignore", FutureWarning)

    runtime_config.init()
    runtime_opts.init(args)
    if not runtime_config.valid():
        logger.debug("[print] 'Config is invalid.'")
        print("Config is invalid.")
        for error in runtime_config.errors:
            logger.error(error)
            print("Error: %s" % error)
        sys.exit(1)

    data = DEMO_JSON_DATA
    error = None
    controller = Controller(data)
    try:
        _ = controller.run()
    except curses.error as e:
        error = e
    except Exception as e:
        error = e
    finally:
        controller._end_curses()
        if error != None:
            logger.error(error)
            print("Error: %s" % error)
            logger.debug("exit 1")
            sys.exit(1)

        logger.debug("end %s" % progname, new_line=True)


if __name__ == "__main__":
    args = argparse.Namespace()
    args.log_path = "./tmp/gfzs.log"
    args.log_level = 0

    main(args)

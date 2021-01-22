import sys
import os
import signal
import warnings
import webbrowser
import json
import curses
import argparse

# local

try:
    # need when 「cat fixtures/rust.json | bin/gfzs」
    from gfzs import tty, info
    from gfzs.utils import debug
    from gfzs.controller import Controller
    from gfzs.model import Model
    from gfzs.config.runtime import RuntimeConfig
    from gfzs.config.app import AppConfig
    import gfzs.cmd.init as cmd_init
    import gfzs.cmd.edit as cmd_edit
    import gfzs.cmd.demo as cmd_demo
    import gfzs.cmd.valid as cmd_valid

# need when 「cat fixtures/rust.json | python -m gfzs」
except ModuleNotFoundError:
    from utils import debug
    from controller import Controller
    from model import Model
    from config.runtime import RuntimeConfig
    from config.app import AppConfig
    import cmd.init as cmd_init
    import cmd.edit as cmd_edit
    import cmd.demo as cmd_demo
    import cmd.valid as cmd_valid


def open_tty(ttyname):
    # See https://github.com/stefanholek/term/issues/1
    return open(ttyname, "wb+", buffering=0)


def init_parser():
    parser = argparse.ArgumentParser(
        prog="gfzs",
        description="Google Fuzzy Search. Pipe the search result(json) of googler and use it",
    )

    parser.add_argument("--version", "-v", action="version", version=info.__version__)
    parser.add_argument(
        "--score",
        "-s",
        type=int,
        default=RuntimeConfig.default_score,
        help="fuzzywuzzy's score. please see https://github.com/seatgeek/fuzzywuzzy",
    )

    subparsers = parser.add_subparsers(title="SubCommands", dest="command")
    subparsers.required = False

    subparsers.add_parser("init", help="Initialize gfzs")
    subparsers.add_parser("edit", help="Edit config")
    subparsers.add_parser("demo", help="Play with Demo")
    subparsers.add_parser("valid", help="Validate ~/.gfzsrc")

    return parser


def exec_subcommand(parser, argv=sys.argv[1:]) -> None:
    args = parser.parse_args(argv)

    if args.command == "init":
        cmd_init.main()
    elif args.command == "edit":
        cmd_edit.main()
    elif args.command == "demo":
        cmd_demo.main()
    elif args.command == "valid":
        cmd_valid.main()


def main() -> None:

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # https://note.nkmk.me/python-warnings-ignore-warning/
    warnings.simplefilter("ignore", FutureWarning)

    parser = init_parser()
    exec_subcommand(parser)

    data = None
    errors = []
    printable_len = 100

    args = parser.parse_args()
    _ = RuntimeConfig.get_instance(args)
    ttyname = tty.get_ttyname()

    with open_tty(ttyname) as tty_f:
        _ = tty.reconnect_descriptors(tty_f)

        try:
            json_str = sys.stdin.read()
            data = json.loads(json_str)
            app_config = AppConfig.get_instance()
            validator = Model(data)

            if not app_config.valid():
                print("Config is invalid.")
                errors = app_config.errors
                return
            elif not validator.valid():
                errors = validator.errors
                return
        except json.decoder.JSONDecodeError as e:
            print("Error: %s" % e)
            if "[ERROR]" in json_str or len(json_str) <= printable_len:
                print("Input data: %s" % json_str)
            else:
                print("Input data (100 chars): %s ..." % json_str[:printable_len])

            sys.exit(1)
        except Exception as e:
            errors.append(e)
        finally:
            if errors != []:
                for error in errors:
                    print("Error: %s" % error)

                sys.exit(1)

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
                print(error)
                sys.exit(1)

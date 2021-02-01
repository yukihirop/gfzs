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
    from gfzs.runtime.opts import RuntimeOpts
    from gfzs.runtime.config import RuntimeConfig
    import gfzs.utils.logger as logger
    import gfzs.cmd.init as cmd_init
    import gfzs.cmd.edit as cmd_edit
    import gfzs.cmd.demo as cmd_demo
    import gfzs.cmd.valid as cmd_valid

# need when 「cat fixtures/rust.json | python -m gfzs」
except ModuleNotFoundError:
    from utils import debug
    from controller import Controller
    from model import Model
    from runtime.opts import RuntimeOpts
    from runtime.config import RuntimeConfig
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
        default=RuntimeOpts.default_score,
        help="fuzzywuzzy's score (default: {0}). please see https://github.com/seatgeek/fuzzywuzzy".format(
            RuntimeOpts.default_score
        ),
    )
    parser.add_argument(
        "--log-level",
        "-l",
        type=str,
        default=logger.INFO,
        help="Log Level (default: {0}). [0: DEBUG, 1: INFO, 2: WARN, 3: ERROR, 4: FATAL, 5: UNKNOWN, 6: NULL]".format(
            logger.INFO
        ),
    )
    parser.add_argument(
        "--log-path",
        "-p",
        type=str,
        default=RuntimeConfig.default_log_path,
        help="Log Path (default: {0})".format(RuntimeConfig.default_log_path),
    )

    subparsers = parser.add_subparsers(title="SubCommands", dest="command")
    subparsers.required = False

    subparsers.add_parser("init", help="Initialize gfzs")
    subparsers.add_parser("edit", help="Edit config")
    subparsers.add_parser("demo", help="Play with Demo")
    subparsers.add_parser(
        "valid", help="Validate {0}".format(RuntimeConfig.default_config_path)
    )

    return parser


def exec_subcommand(parser, argv=sys.argv[1:]) -> None:
    args = parser.parse_args(argv)

    if args.command == "init":
        cmd_init.main(args)
    elif args.command == "edit":
        cmd_edit.main(args)
    elif args.command == "demo":
        cmd_demo.main(args)
    elif args.command == "valid":
        cmd_valid.main(args)


def main() -> None:
    # https://note.nkmk.me/python-warnings-ignore-warning/
    warnings.simplefilter("ignore", FutureWarning)

    parser = init_parser()
    exec_subcommand(parser)
    args = parser.parse_args()

    progname = "gfzs"
    properties = {
        "progname": progname,
        "severity": int(args.log_level),
        "log_path": args.log_path,
    }
    logger.init_properties(**properties)
    logger.debug("start %s" % progname)

    def handle_sigint(signum, frame):
        logger.debug("detect SIGINT (Ctrl-c)")
        logger.debug("exit 0")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)

    data = None
    error = None
    errors = []
    printable_len = 100
    _ = RuntimeOpts.get_instance(args)
    ttyname = tty.get_ttyname()

    with open_tty(ttyname) as tty_f:
        _ = tty.reconnect_descriptors(tty_f)

        try:
            json_str = sys.stdin.read()
            data = json.loads(json_str)
            validator = Model(data)
            runtime_config = RuntimeConfig.get_instance()

            if not runtime_config.valid():
                logger.debug("[print] Config is invalid.")
                print("Config is invalid.")
                errors = runtime_config.errors
                return
            elif not validator.valid():
                errors = validator.errors
                return
        except json.decoder.JSONDecodeError as e:
            logger.error(e)
            print("Error: %s" % e)
            if "[ERROR]" in json_str or len(json_str) <= printable_len:
                logger.error("Input data: %s" % json_str)
                print("Input data: %s" % json_str)
            else:
                logger.error(
                    "Input data (100 chars): %s ..." % json_str[:printable_len]
                )
                print("Input data (100 chars): %s ..." % json_str[:printable_len])

            logger.debug("exit 1")
            sys.exit(1)
        except Exception as e:
            errors.append(e)
        finally:
            if errors != []:
                for error in errors:
                    logger.error(error)
                    print("Error: %s" % error)

                logger.debug("exit 1")
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
                logger.error(error)
                print(error)
                logger.debug("exit 1")
                sys.exit(1)

            logger.debug("end %s" % progname, new_line=True)

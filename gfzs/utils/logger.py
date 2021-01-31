import datetime
import os, sys
import inspect
from typing import Union, Optional

# local

try:
    # need when 「python3 gfzs/utils/logger.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

        if os.environ.get("DEBUG"):
            import debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        if os.environ.get("DEBUG"):
            from gfzs.utils import debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))

    if os.environ.get("DEBUG"):
        from utils import debug

"""Log Formatter Class"""


class Formatter:
    """Formatter to format log output"""

    """Default Log Format"""
    DEFAULT_LOG_FORMAT = "%s, [%s#%d] %5s -- %s: %s in %s\n"

    """Default Empty Log Format"""
    DEFAULT_EMPTY_LOG_FORMAT = "%s, [%s#%d] %5s -- %s:\n"

    """Default Datetime Format"""
    DEFAULT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

    """Default Stack Format"""
    DEFAULT_STACK_FORMAT = "%s:%d  %s"

    def __init__(self):
        self.default_datetime_format = None

    def call(
        self,
        severity: str,
        datetime,
        progname: str,
        msg: Union[str, Exception],
        stack: inspect.FrameInfo,
    ) -> str:
        adjusted_msg = self._msg2str(msg)
        if adjusted_msg is "":
            return Formatter.DEFAULT_EMPTY_LOG_FORMAT % (
                severity[:1],
                self._format_datetime(datetime),
                os.getpid(),
                progname,
                severity,
            )
        else:
            stack_msg = Formatter.DEFAULT_STACK_FORMAT % (
                stack.filename,
                stack.lineno,
                stack.function,
            )
            return Formatter.DEFAULT_LOG_FORMAT % (
                severity[:1],
                self._format_datetime(datetime),
                os.getpid(),
                progname,
                severity,
                self._msg2str(msg),
                stack_msg,
            )

    def _format_datetime(self, datetime) -> str:
        return datetime.strftime(
            self.default_datetime_format or Formatter.DEFAULT_DATETIME_FORMAT
        )

    def _msg2str(self, msg: Union[str, Exception]) -> str:
        if type(msg) is str:
            return msg
        elif type(msg) is Exception:
            return "{1} ({2})\n{3}" % (
                msg.message,
                msg.__class__.__name__,
                msg.__traceback__,
            )
        else:
            return str(msg)


"""Logger Singleton Class"""

# https://qiita.com/risuoku/items/23789030db29489f8214
self = sys.modules[__name__]

"""Log Level"""
DEBUG = 0
INFO = 1
WARN = 2
ERROR = 3
FATAL = 4
UNKNOWNN = 5
NULL = 6

"""Severity Label for logging (max 5 chars)"""
SEV_LABEL = ("DEBUG", "INFO", "WARN", "ERROR", "FATAL", "NULL", "ANY")

"""Default Log Path"""
DEFAULT_LOG_PATH = "~/gfzs.log"

self.progname = ""
self.log_path = DEFAULT_LOG_PATH
self.level = INFO
self.default_formatter = Formatter()
self.formatter = None


def init_properties(*, progname: str, severity: Union[int, str], log_path: str) -> None:
    self.progname = progname
    self.log_path = log_path
    self.set_level(severity)


def set_level(severity: Union[int, str]) -> None:
    """Set logging severity threshold.

    Args:
        severity: The Severity of the long message.
    """

    if str(severity).isnumeric():
        self.level = severity
    else:
        _severity = severity.lower()

        if _severity == "debug":
            self.level = DEBUG
        elif _severity == "info":
            self.level = INFO
        elif _severity == "warn":
            self.level = ERROR
        elif _severity == "fatal":
            self.level = FATAL
        elif _severity == "UNKNOWN":
            self.level = UNKNOWN
        elif _severity == "NULL":
            self.level = NULL
        else:
            raise Exception("Invalid log level: #{severity}")


def debug(msg: Union[str, Exception], new_line=False) -> None:
    self._add(DEBUG, self.progname, msg)
    if new_line:
        self._add(DEBUG, self.progname, "")


def info(msg: Union[str, Exception], new_line=False) -> None:
    self._add(INFO, self.progname, msg)
    if new_line:
        self._add(INFO, self.progname, "")


def warn(msg: Union[str, Exception], new_line=False) -> None:
    self._add(WARAN, self.progname, msg)
    if new_line:
        self._add(WARAN, self.progname, "")


def error(msg: Union[str, Exception], new_line=False) -> None:
    self._add(ERROR, self.progname, msg)
    if new_line:
        self._add(ERROR, self.progname, "")


def fatal(msg: Union[str, Exception], new_line=False) -> None:
    self._add(FATAL, self.progname, msg)
    if new_line:
        self._add(FATAL, self.progname, "")


def unknown(msg: Union[str, Exception], new_line=False) -> None:
    self._add(UNKNOWN, self.progname, msg)
    if new_line:
        self._add(UNKNOWN, self.progname, "")


def _add(
    severity: Union[str, int], progname: str, msg: Union[str, Exception]
) -> Optional[bool]:
    if severity is None:
        severity = UNKNOWNN

    if severity < self.level:
        return True

    stack = inspect.stack()[2]

    with open(self.log_path, "a") as f:
        f.write(
            self._format_message(
                self._format_severity(severity),
                datetime.datetime.now(),
                progname,
                msg,
                stack,
            )
        )


def _format_message(
    severity: Union[str, int],
    datetime,
    progname: str,
    msg: Union[str, Exception],
    stack: inspect.FrameInfo,
) -> str:
    return (self.formatter or self.default_formatter).call(
        severity, datetime, progname, msg, stack
    )


def _format_severity(severity: int) -> str:
    return SEV_LABEL[severity] or "ANY"


if __name__ == "__main__":
    properties = {
        "progname": "gfzs.utils.logger",
        "severity": "INFO",
        "log_path": "./tmp/gfzs.log",
    }
    self.init_properties(**properties)
    self.info("info")
    self.debug("debug")

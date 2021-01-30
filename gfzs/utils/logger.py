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


class Singleton(object):
    @classmethod
    def get_instance(cls, *args):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(*args)

        return cls._instance


class Logger(Singleton):
    """A logger whose display can be controlled at the log level"""

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
    DEFAULT_LOG_PATH = "~/.gfzs.log"

    def __init__(self, progname: str, log_path=DEFAULT_LOG_PATH):
        self.progname = progname
        self.level = Logger.INFO
        self.default_formatter = Formatter()
        self.formatter = None
        self.log_path = log_path or DEFAULT_LOG_PATH

    def set_level(self, severity: Union[int, str]) -> None:
        """Set logging severity threshold.

        Args:
          severity: The Severity of the long message.
        """

        if str(severity).isnumeric():
            self.level = severity
        else:
            _severity = severity.lower()

            if _severity == "debug":
                self.level = Logger.DEBUG
            elif _severity == "info":
                self.level = Logger.INFO
            elif _severity == "warn":
                self.level = Logger.ERROR
            elif _severity == "fatal":
                self.level = Logger.FATAL
            elif _severity == "UNKNOWN":
                self.level = Logger.UNKNOWN
            elif _severity == "NULL":
                self.level = Logger.NULL
            else:
                raise Exception("Invalid log level: #{severity}")

    def debug(self, msg: Union[str, Exception], new_line=False) -> None:
        self._add(Logger.DEBUG, self.progname, msg)
        if new_line:
            self._add(Logger.DEBUG, self.progname, "")

    def info(self, msg: Union[str, Exception], new_line=False) -> None:
        self._add(Logger.INFO, self.progname, msg)
        if new_line:
            self._add(Logger.INFO, self.progname, "")

    def warn(self, msg: Union[str, Exception], new_line=False) -> None:
        self._add(Logger.WARAN, self.progname, msg)
        if new_line:
            self._add(Logger.WARAN, self.progname, "")

    def error(self, msg: Union[str, Exception], new_line=False) -> None:
        self._add(Logger.ERROR, self.progname, msg)
        if new_line:
            self._add(Logger.ERROR, self.progname, "")

    def fatal(self, msg: Union[str, Exception], new_line=False) -> None:
        self._add(Logger.FATAL, self.progname, msg)
        if new_line:
            self._add(Logger.FATAL, self.progname, "")

    def unknown(self, msg: Union[str, Exception], new_line=False) -> None:
        self._add(Logger.UNKNOWN, self.progname, msg)
        if new_line:
            self._add(Logger.UNKNOWN, self.progname, "")

    def _add(
        self, severity: Union[str, int], progname: str, msg: Union[str, Exception]
    ) -> Optional[bool]:
        if severity is None:
            severity = Logger.UNKNOWNN
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
        self,
        severity: Union[str, int],
        datetime,
        progname: str,
        msg: Union[str, Exception],
        stack: inspect.FrameInfo,
    ) -> str:
        return (self.formatter or self.default_formatter).call(
            severity, datetime, progname, msg, stack
        )

    def _format_severity(self, severity: int) -> str:
        return Logger.SEV_LABEL[severity] or "ANY"


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


if __name__ == "__main__":
    progname = "gfzs.utils.logger"
    logger = Logger.get_instance(progname, "./tmp/gfzs.log")
    logger.info("test logger")
    logger.info()

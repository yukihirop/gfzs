import curses
import os, sys

# local

try:
    # need when 「python3 gfzs/color.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        import utils.logger as logger

        if os.environ.get("DEBUG"):
            from utils import debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        import gfzs.utils.logger as logger

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug
# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    import utils.logger as logger

    if os.environ.get("DEBUG"):
        import utils.debug as debug


"""Color Class"""

# https://qiita.com/risuoku/items/23789030db29489f8214
self = sys.modules[__name__]

COLORS = (
    curses.COLOR_BLACK,
    curses.COLOR_RED,
    curses.COLOR_GREEN,
    curses.COLOR_YELLOW,
    curses.COLOR_BLUE,
    curses.COLOR_MAGENTA,
    curses.COLOR_CYAN,
    curses.COLOR_WHITE,
)


def init():
    logger.debug("[Color] init")
    curses.start_color()
    curses.use_default_colors()
    colors_len = len(COLORS)
    self.offset_after_builtin_color = self._calculate_color_number(
        colors_len, colors_len
    )
    self._setup()
    self.highlight = self._highlight()


def _setup():
    logger.debug("[Color] setup")
    for i in COLORS:
        for j in COLORS:
            color_number = self._calculate_color_number(i, j)
            curses.init_pair(color_number, i, j)

    # https://www.it-swarm-ja.tech/ja/python/curses%E3%81%A7%E7%AB%AF%E6%9C%AB%E3%81%AE%E3%82%AB%E3%83%A9%E3%83%BC%E3%83%91%E3%83%AC%E3%83%83%E3%83%88%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95/1042208550/
    # The default color is assigned to the color number -1.
    offset = self.offset_after_builtin_color
    curses.init_pair(28 + offset, 27, -1)  # G(g) color of Google
    curses.init_pair(10 + offset, 9, -1)  # o(e) color of Google
    curses.init_pair(12 + offset, 11, -1)  # o color of Google
    curses.init_pair(36 + offset, 35, -1)  # l color of Google


def _end_curses():
    """ Terminates the curses application. """
    logger.debug("[Color] end curses")
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def use(data) -> int:
    i = data["text"]
    j = data["background"]
    style = data["style"]

    try:
        if j == -1:
            offset = self.offset_after_builtin_color
            color_number = i + 1 + offset
        else:
            color_number = self._calculate_color_number(i, j)

        if style == "normal":
            return curses.color_pair(color_number)
        elif style == "bold":
            return curses.color_pair(color_number) | curses.A_BOLD
        elif style == "link":
            return curses.color_pair(color_number) | curses.A_UNDERLINE
        else:
            raise Exception("[Color] Do not support style: %s" % style)
    except Exception as e:
        logger.debug("end curses")
        self._end_curses()

        logger.error(e)
        print("Error: %s" % str(e))

        logger.debug("exit 1")
        sys.exit(1)


def google(c, style="bold") -> int:
    offset = self.offset_after_builtin_color
    color = None

    try:
        if c in ("G", "g"):
            color = curses.color_pair(28 + offset)
        elif c == "o":
            color = curses.color_pair(10 + offset)
        elif c == "o2":
            color = curses.color_pair(12 + offset)
        elif c == "l":
            color = curses.color_pair(36 + offset)
        elif c == "e":
            color = curses.color_pair(10 + offset)

        if style == "bold":
            return color | curses.A_BOLD
        elif style == "normal":
            return color
        else:
            raise Exception("[Color] Do not support style: %s" % style)
    except Exception as e:
        self._end_curses()

        logger.error(e)
        print("Error: %s" % str(e))

        logger.debug("exit 1")
        sys.exit(1)


def _highlight() -> int:
    data = {
        "text": curses.COLOR_BLACK,
        "background": curses.COLOR_GREEN,
        "style": "normal",
    }
    return self.use(data)


def fuzzy(style="bold") -> int:
    return self.google("o2", style)


def search(style="bold") -> int:
    return self.google("o", style)


def version(style="bold") -> int:
    data = {
        "text": curses.COLOR_GREEN,
        "background": curses.COLOR_BLACK,
        "style": style,
    }
    return self.use(data)


def copy_right(style="bold") -> int:
    data = {
        "text": curses.COLOR_GREEN,
        "background": curses.COLOR_BLACK,
        "style": style,
    }
    return self.use(data)


def not_found(style="bold") -> int:
    data = {
        "text": curses.COLOR_GREEN,
        "background": curses.COLOR_BLACK,
        "style": style,
    }
    return self.use(data)


# https://www.linuxjournal.com/content/about-ncurses-colors-0
def _calculate_color_number(fg, bg):
    B = 1 << 7
    bbb = (7 & bg) << 4
    ffff = 7 & fg
    return B | bbb | ffff


if __name__ == "__main__":
    import signal

    progname = "gfzs.utils.color"
    properties = {
        "progname": progname,
        "severity": 0,
        "log_path": "./tmp/gfzs.log",
    }
    logger.init_properties(**properties)
    logger.debug("start %s" % progname)

    def handle_sigint(signum, frame):
        logger.debug("detect SIGINT (Ctrl-c)")
        logger.debug("exit 0")
        logger.debug("end %s" % progname, new_line=True)
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)

    def demo(screen):
        self.init()

        for i in range(0, 8):
            for j in range(0, 8):
                use_color = color.use({"text": i, "background": j, "style": "normal"})
                screen.addstr("(%d, %d)" % (i, j), use_color)

        screen.getch()

    curses.wrapper(demo)

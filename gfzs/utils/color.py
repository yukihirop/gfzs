import curses
import os, sys

# local

try:
    # need when 「python3 gfzs/markup.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        import debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.utils import debug
# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from utils import debug


class Singleton(object):
    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance


class Color(Singleton):
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

    def __init__(self):
        curses.start_color()
        curses.use_default_colors()
        colors_len = len(Color.COLORS)
        self.offset_after_builtin_color = self._calculate_color_number(
            colors_len, colors_len
        )
        self._setup()

    def _setup(self):
        for i in Color.COLORS:
            for j in Color.COLORS:
                color_number = self._calculate_color_number(i, j)
                curses.init_pair(color_number, i, j)

        # https://www.it-swarm-ja.tech/ja/python/curses%E3%81%A7%E7%AB%AF%E6%9C%AB%E3%81%AE%E3%82%AB%E3%83%A9%E3%83%BC%E3%83%91%E3%83%AC%E3%83%83%E3%83%88%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95/1042208550/
        # The default color is assigned to the color number -1.
        offset = self.offset_after_builtin_color
        curses.init_pair(28 + offset, 27, -1)  # G(g) color of Google
        curses.init_pair(10 + offset, 9, -1)  # o(e) color of Google
        curses.init_pair(12 + offset, 11, -1)  # o color of Google
        curses.init_pair(36 + offset, 35, -1)  # l color of Google

    def _end_curses(self):
        """ Terminates the curses application. """
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def use(self, data) -> int:
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
            self._end_curses()
            print("Error: %s" % str(e))
            sys.exit(1)

    def google(self, c, style="bold") -> int:
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
            print("Error: %s" % str(e))
            sys.exit(1)

    @property
    def highlight(self) -> int:
        data = {
            "text": curses.COLOR_BLACK,
            "background": curses.COLOR_GREEN,
            "style": "normal",
        }
        return self.use(data)

    def fuzzy(self, style="bold") -> int:
        return self.google("o2", style)

    def search(self, style="bold") -> int:
        return self.google("o", style)

    def version(self, style="bold") -> int:
        data = {
            "text": curses.COLOR_GREEN,
            "background": curses.COLOR_BLACK,
            "style": style,
        }
        return self.use(data)

    def copy_right(self, style="bold") -> int:
        data = {
            "text": curses.COLOR_GREEN,
            "background": curses.COLOR_BLACK,
            "style": style,
        }
        return self.use(data)

    def not_found(self, style="bold") -> int:
        data = {
            "text": curses.COLOR_GREEN,
            "background": curses.COLOR_BLACK,
            "style": style,
        }
        return self.use(data)

    # https://www.linuxjournal.com/content/about-ncurses-colors-0
    def _calculate_color_number(self, fg, bg):
        B = 1 << 7
        bbb = (7 & bg) << 4
        ffff = 7 & fg
        return B | bbb | ffff


if __name__ == "__main__":

    import curses
    import signal

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    def demo(screen):
        color = Color.get_instance()

        for i in range(0, 8):
            for j in range(0, 8):
                use_color = color.use({"text": i, "background": j, "style": "normal"})
                screen.addstr("(%d, %d)" % (i, j), use_color)

        screen.getch()

    curses.wrapper(demo)

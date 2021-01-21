import sys, os
import curses
import curses.ascii

# local

try:
    # need when 「python3 gfzs/views/footer.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        import utils
        from utils.color import Color

        if os.environ.get("DEBUG"):
            import utils.debug as debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.utils.color import Color

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from utils.color import Color

    if os.environ.get("DEBUG"):
        import utils.debug as debug

#
# Generate by https://lazesoftware.com/tool/hugeaagen/
#                                  ■
#                                  ■                                                                                     ■
#   ■■■■■                          ■              ■■■■■■                                ■■■■                             ■
#  ■■   ■                          ■              ■                                    ■   ■■                            ■
# ■■         ■■■■    ■■■■    ■■■■  ■    ■■■■      ■      ■   ■■  ■■■■■ ■■■■■■■   ■     ■        ■■■■   ■■■   ■ ■■  ■■■■  ■ ■■■
# ■         ■■  ■■  ■■  ■■  ■■  ■  ■   ■■  ■      ■      ■   ■■     ■     ■  ■   ■     ■■■     ■■  ■  ■   ■  ■■   ■■  ■  ■■  ■■
# ■    ■■■  ■    ■  ■    ■  ■   ■  ■   ■   ■■     ■■■■■■ ■   ■■    ■     ■   ■  ■        ■■■   ■   ■■     ■  ■■   ■      ■    ■
# ■      ■  ■    ■  ■    ■  ■■  ■  ■   ■■■■■■     ■      ■   ■■   ■■    ■■    ■ ■          ■■  ■■■■■■ ■■■■■  ■    ■      ■    ■
# ■■     ■  ■    ■  ■    ■   ■■■   ■   ■          ■      ■   ■■   ■     ■     ■■■           ■  ■      ■   ■  ■    ■      ■    ■
#  ■■   ■■  ■■  ■■  ■■  ■■  ■■     ■   ■■         ■      ■■  ■■  ■     ■      ■■       ■   ■■  ■■     ■  ■■  ■    ■■  ■  ■    ■
#   ■■■■■    ■■■■    ■■■■    ■■■■  ■    ■■■■      ■       ■■■■■ ■■■■■■■■■■■■   ■        ■■■■    ■■■■  ■■■■■  ■     ■■■■  ■    ■
#                           ■   ■■                                            ■
#                           ■■■■■                                            ■■
#
#
#
#                                                                                                ■
#                                 ■■    ■■                   ■■■■■■                              ■
#                                 ■■■   ■■          ■        ■                                   ■
#                                 ■ ■   ■■   ■■■■  ■■■■      ■       ■■■■   ■   ■■  ■ ■■■    ■■■■■
#                                 ■  ■  ■■  ■■  ■■  ■        ■      ■■  ■■  ■   ■■  ■■  ■■  ■■  ■■
#                                 ■  ■■ ■■  ■    ■  ■        ■■■■■■ ■    ■  ■   ■■  ■    ■  ■    ■
#                                 ■   ■ ■■  ■    ■  ■        ■      ■    ■  ■   ■■  ■    ■  ■    ■
#                                 ■    ■■■  ■    ■  ■        ■      ■    ■  ■   ■■  ■    ■  ■    ■
#                                 ■    ■■■  ■■  ■■  ■■       ■      ■■  ■■  ■■  ■■  ■    ■  ■■  ■■
#                                 ■     ■■   ■■■■    ■■      ■       ■■■■    ■■■■■  ■    ■   ■■■ ■
#
#
GOOGLER_NOT_FOUND = [
    [[34, 0], "l"],
    [[120, 0], "search"],
    [[3, 1], "G"],
    [[4, 1], "G"],
    [[5, 1], "G"],
    [[6, 1], "G"],
    [[7, 1], "G"],
    [[34, 1], "l"],
    [[49, 1], "fuzzy"],
    [[50, 1], "fuzzy"],
    [[51, 1], "fuzzy"],
    [[52, 1], "fuzzy"],
    [[53, 1], "fuzzy"],
    [[54, 1], "fuzzy"],
    [[87, 1], "search"],
    [[88, 1], "search"],
    [[89, 1], "search"],
    [[90, 1], "search"],
    [[120, 1], "search"],
    [[2, 2], "G"],
    [[3, 2], "G"],
    [[7, 2], "G"],
    [[34, 2], "l"],
    [[49, 2], "fuzzy"],
    [[86, 2], "search"],
    [[90, 2], "search"],
    [[91, 2], "search"],
    [[120, 2], "search"],
    [[1, 3], "G"],
    [[2, 3], "G"],
    [[12, 3], "o"],
    [[13, 3], "o"],
    [[14, 3], "o"],
    [[15, 3], "o"],
    [[20, 3], "o2"],
    [[21, 3], "o2"],
    [[22, 3], "o2"],
    [[23, 3], "o2"],
    [[28, 3], "g"],
    [[29, 3], "g"],
    [[30, 3], "g"],
    [[31, 3], "g"],
    [[34, 3], "l"],
    [[39, 3], "e"],
    [[40, 3], "e"],
    [[41, 3], "e"],
    [[42, 3], "e"],
    [[49, 3], "fuzzy"],
    [[56, 3], "fuzzy"],
    [[60, 3], "fuzzy"],
    [[61, 3], "fuzzy"],
    [[64, 3], "fuzzy"],
    [[65, 3], "fuzzy"],
    [[66, 3], "fuzzy"],
    [[67, 3], "fuzzy"],
    [[68, 3], "fuzzy"],
    [[70, 3], "fuzzy"],
    [[71, 3], "fuzzy"],
    [[72, 3], "fuzzy"],
    [[73, 3], "fuzzy"],
    [[74, 3], "fuzzy"],
    [[75, 3], "fuzzy"],
    [[76, 3], "fuzzy"],
    [[80, 3], "fuzzy"],
    [[86, 3], "search"],
    [[95, 3], "search"],
    [[96, 3], "search"],
    [[97, 3], "search"],
    [[98, 3], "search"],
    [[102, 3], "search"],
    [[103, 3], "search"],
    [[104, 3], "search"],
    [[108, 3], "search"],
    [[110, 3], "search"],
    [[111, 3], "search"],
    [[114, 3], "search"],
    [[115, 3], "search"],
    [[116, 3], "search"],
    [[117, 3], "search"],
    [[120, 3], "search"],
    [[122, 3], "search"],
    [[123, 3], "search"],
    [[124, 3], "search"],
    [[1, 4], "G"],
    [[11, 4], "o"],
    [[12, 4], "o"],
    [[15, 4], "o"],
    [[16, 4], "o"],
    [[19, 4], "o2"],
    [[20, 4], "o2"],
    [[23, 4], "o2"],
    [[24, 4], "o2"],
    [[27, 4], "g"],
    [[28, 4], "g"],
    [[31, 4], "g"],
    [[34, 4], "l"],
    [[38, 4], "e"],
    [[39, 4], "e"],
    [[42, 4], "e"],
    [[49, 4], "fuzzy"],
    [[56, 4], "fuzzy"],
    [[60, 4], "fuzzy"],
    [[61, 4], "fuzzy"],
    [[67, 4], "fuzzy"],
    [[73, 4], "fuzzy"],
    [[76, 4], "fuzzy"],
    [[80, 4], "fuzzy"],
    [[86, 4], "search"],
    [[87, 4], "search"],
    [[88, 4], "search"],
    [[94, 4], "search"],
    [[95, 4], "search"],
    [[98, 4], "search"],
    [[101, 4], "search"],
    [[105, 4], "search"],
    [[108, 4], "search"],
    [[109, 4], "search"],
    [[113, 4], "search"],
    [[114, 4], "search"],
    [[117, 4], "search"],
    [[120, 4], "search"],
    [[121, 4], "search"],
    [[124, 4], "search"],
    [[125, 4], "search"],
    [[1, 5], "G"],
    [[6, 5], "G"],
    [[7, 5], "G"],
    [[8, 5], "G"],
    [[11, 5], "o"],
    [[16, 5], "o"],
    [[19, 5], "o2"],
    [[24, 5], "o2"],
    [[27, 5], "g"],
    [[31, 5], "g"],
    [[34, 5], "l"],
    [[38, 5], "e"],
    [[42, 5], "e"],
    [[43, 5], "e"],
    [[49, 5], "fuzzy"],
    [[50, 5], "fuzzy"],
    [[51, 5], "fuzzy"],
    [[52, 5], "fuzzy"],
    [[53, 5], "fuzzy"],
    [[54, 5], "fuzzy"],
    [[56, 5], "fuzzy"],
    [[60, 5], "fuzzy"],
    [[61, 5], "fuzzy"],
    [[66, 5], "fuzzy"],
    [[72, 5], "fuzzy"],
    [[76, 5], "fuzzy"],
    [[79, 5], "fuzzy"],
    [[88, 5], "search"],
    [[89, 5], "search"],
    [[90, 5], "search"],
    [[94, 5], "search"],
    [[98, 5], "search"],
    [[99, 5], "search"],
    [[105, 5], "search"],
    [[108, 5], "search"],
    [[109, 5], "search"],
    [[113, 5], "search"],
    [[120, 5], "search"],
    [[125, 5], "search"],
    [[1, 6], "G"],
    [[8, 6], "G"],
    [[11, 6], "o"],
    [[16, 6], "o"],
    [[19, 6], "o2"],
    [[24, 6], "o2"],
    [[27, 6], "g"],
    [[28, 6], "g"],
    [[31, 6], "g"],
    [[34, 6], "l"],
    [[38, 6], "e"],
    [[39, 6], "e"],
    [[40, 6], "e"],
    [[41, 6], "e"],
    [[42, 6], "e"],
    [[43, 6], "e"],
    [[49, 6], "fuzzy"],
    [[56, 6], "fuzzy"],
    [[60, 6], "fuzzy"],
    [[61, 6], "fuzzy"],
    [[65, 6], "fuzzy"],
    [[66, 6], "fuzzy"],
    [[71, 6], "fuzzy"],
    [[72, 6], "fuzzy"],
    [[77, 6], "fuzzy"],
    [[79, 6], "fuzzy"],
    [[90, 6], "search"],
    [[91, 6], "search"],
    [[94, 6], "search"],
    [[95, 6], "search"],
    [[96, 6], "search"],
    [[97, 6], "search"],
    [[98, 6], "search"],
    [[99, 6], "search"],
    [[101, 6], "search"],
    [[102, 6], "search"],
    [[103, 6], "search"],
    [[104, 6], "search"],
    [[105, 6], "search"],
    [[108, 6], "search"],
    [[113, 6], "search"],
    [[120, 6], "search"],
    [[125, 6], "search"],
    [[1, 7], "G"],
    [[2, 7], "G"],
    [[8, 7], "G"],
    [[11, 7], "o"],
    [[16, 7], "o"],
    [[19, 7], "o2"],
    [[24, 7], "o2"],
    [[28, 7], "g"],
    [[29, 7], "g"],
    [[30, 7], "g"],
    [[34, 7], "l"],
    [[38, 7], "e"],
    [[49, 7], "fuzzy"],
    [[56, 7], "fuzzy"],
    [[60, 7], "fuzzy"],
    [[61, 7], "fuzzy"],
    [[65, 7], "fuzzy"],
    [[71, 7], "fuzzy"],
    [[77, 7], "fuzzy"],
    [[78, 7], "fuzzy"],
    [[79, 7], "fuzzy"],
    [[91, 7], "search"],
    [[94, 7], "search"],
    [[101, 7], "search"],
    [[105, 7], "search"],
    [[108, 7], "search"],
    [[113, 7], "search"],
    [[120, 7], "search"],
    [[125, 7], "search"],
    [[2, 8], "G"],
    [[3, 8], "G"],
    [[7, 8], "G"],
    [[8, 8], "G"],
    [[11, 8], "o"],
    [[12, 8], "o"],
    [[15, 8], "o"],
    [[16, 8], "o"],
    [[19, 8], "o2"],
    [[20, 8], "o2"],
    [[23, 8], "o2"],
    [[24, 8], "o2"],
    [[27, 8], "g"],
    [[28, 8], "g"],
    [[34, 8], "l"],
    [[38, 8], "e"],
    [[39, 8], "e"],
    [[49, 8], "fuzzy"],
    [[56, 8], "fuzzy"],
    [[57, 8], "fuzzy"],
    [[60, 8], "fuzzy"],
    [[61, 8], "fuzzy"],
    [[64, 8], "fuzzy"],
    [[70, 8], "fuzzy"],
    [[77, 8], "fuzzy"],
    [[78, 8], "fuzzy"],
    [[86, 8], "search"],
    [[90, 8], "search"],
    [[91, 8], "search"],
    [[94, 8], "search"],
    [[95, 8], "search"],
    [[101, 8], "search"],
    [[104, 8], "search"],
    [[105, 8], "search"],
    [[108, 8], "search"],
    [[113, 8], "search"],
    [[114, 8], "search"],
    [[117, 8], "search"],
    [[120, 8], "search"],
    [[125, 8], "search"],
    [[3, 9], "G"],
    [[4, 9], "G"],
    [[5, 9], "G"],
    [[6, 9], "G"],
    [[7, 9], "G"],
    [[12, 9], "o"],
    [[13, 9], "o"],
    [[14, 9], "o"],
    [[15, 9], "o"],
    [[20, 9], "o2"],
    [[21, 9], "o2"],
    [[22, 9], "o2"],
    [[23, 9], "o2"],
    [[28, 9], "g"],
    [[29, 9], "g"],
    [[30, 9], "g"],
    [[31, 9], "g"],
    [[34, 9], "l"],
    [[39, 9], "e"],
    [[40, 9], "e"],
    [[41, 9], "e"],
    [[42, 9], "e"],
    [[49, 9], "fuzzy"],
    [[57, 9], "fuzzy"],
    [[58, 9], "fuzzy"],
    [[59, 9], "fuzzy"],
    [[60, 9], "fuzzy"],
    [[61, 9], "fuzzy"],
    [[63, 9], "fuzzy"],
    [[64, 9], "fuzzy"],
    [[65, 9], "fuzzy"],
    [[66, 9], "fuzzy"],
    [[67, 9], "fuzzy"],
    [[68, 9], "fuzzy"],
    [[69, 9], "fuzzy"],
    [[70, 9], "fuzzy"],
    [[71, 9], "fuzzy"],
    [[72, 9], "fuzzy"],
    [[73, 9], "fuzzy"],
    [[74, 9], "fuzzy"],
    [[78, 9], "fuzzy"],
    [[87, 9], "search"],
    [[88, 9], "search"],
    [[89, 9], "search"],
    [[90, 9], "search"],
    [[95, 9], "search"],
    [[96, 9], "search"],
    [[97, 9], "search"],
    [[98, 9], "search"],
    [[101, 9], "search"],
    [[102, 9], "search"],
    [[103, 9], "search"],
    [[104, 9], "search"],
    [[105, 9], "search"],
    [[108, 9], "search"],
    [[114, 9], "search"],
    [[115, 9], "search"],
    [[116, 9], "search"],
    [[117, 9], "search"],
    [[120, 9], "search"],
    [[125, 9], "search"],
    [[27, 10], "g"],
    [[31, 10], "g"],
    [[32, 10], "g"],
    [[77, 10], "fuzzy"],
    [[27, 11], "g"],
    [[28, 11], "g"],
    [[29, 11], "g"],
    [[30, 11], "g"],
    [[31, 11], "g"],
    [[76, 11], "fuzzy"],
    [[77, 11], "fuzzy"],
    [[96, 15], "not_found"],
    [[33, 16], "not_found"],
    [[34, 16], "not_found"],
    [[39, 16], "not_found"],
    [[40, 16], "not_found"],
    [[60, 16], "not_found"],
    [[61, 16], "not_found"],
    [[62, 16], "not_found"],
    [[63, 16], "not_found"],
    [[64, 16], "not_found"],
    [[65, 16], "not_found"],
    [[96, 16], "not_found"],
    [[33, 17], "not_found"],
    [[34, 17], "not_found"],
    [[35, 17], "not_found"],
    [[39, 17], "not_found"],
    [[40, 17], "not_found"],
    [[51, 17], "not_found"],
    [[60, 17], "not_found"],
    [[96, 17], "not_found"],
    [[33, 18], "not_found"],
    [[35, 18], "not_found"],
    [[39, 18], "not_found"],
    [[40, 18], "not_found"],
    [[44, 18], "not_found"],
    [[45, 18], "not_found"],
    [[46, 18], "not_found"],
    [[47, 18], "not_found"],
    [[50, 18], "not_found"],
    [[51, 18], "not_found"],
    [[52, 18], "not_found"],
    [[53, 18], "not_found"],
    [[60, 18], "not_found"],
    [[68, 18], "not_found"],
    [[69, 18], "not_found"],
    [[70, 18], "not_found"],
    [[71, 18], "not_found"],
    [[75, 18], "not_found"],
    [[79, 18], "not_found"],
    [[80, 18], "not_found"],
    [[83, 18], "not_found"],
    [[85, 18], "not_found"],
    [[86, 18], "not_found"],
    [[87, 18], "not_found"],
    [[92, 18], "not_found"],
    [[93, 18], "not_found"],
    [[94, 18], "not_found"],
    [[95, 18], "not_found"],
    [[96, 18], "not_found"],
    [[33, 19], "not_found"],
    [[36, 19], "not_found"],
    [[39, 19], "not_found"],
    [[40, 19], "not_found"],
    [[43, 19], "not_found"],
    [[44, 19], "not_found"],
    [[47, 19], "not_found"],
    [[48, 19], "not_found"],
    [[51, 19], "not_found"],
    [[60, 19], "not_found"],
    [[67, 19], "not_found"],
    [[68, 19], "not_found"],
    [[71, 19], "not_found"],
    [[72, 19], "not_found"],
    [[75, 19], "not_found"],
    [[79, 19], "not_found"],
    [[80, 19], "not_found"],
    [[83, 19], "not_found"],
    [[84, 19], "not_found"],
    [[87, 19], "not_found"],
    [[88, 19], "not_found"],
    [[91, 19], "not_found"],
    [[92, 19], "not_found"],
    [[95, 19], "not_found"],
    [[96, 19], "not_found"],
    [[33, 20], "not_found"],
    [[36, 20], "not_found"],
    [[37, 20], "not_found"],
    [[39, 20], "not_found"],
    [[40, 20], "not_found"],
    [[43, 20], "not_found"],
    [[48, 20], "not_found"],
    [[51, 20], "not_found"],
    [[60, 20], "not_found"],
    [[61, 20], "not_found"],
    [[62, 20], "not_found"],
    [[63, 20], "not_found"],
    [[64, 20], "not_found"],
    [[65, 20], "not_found"],
    [[67, 20], "not_found"],
    [[72, 20], "not_found"],
    [[75, 20], "not_found"],
    [[79, 20], "not_found"],
    [[80, 20], "not_found"],
    [[83, 20], "not_found"],
    [[88, 20], "not_found"],
    [[91, 20], "not_found"],
    [[96, 20], "not_found"],
    [[33, 21], "not_found"],
    [[37, 21], "not_found"],
    [[39, 21], "not_found"],
    [[40, 21], "not_found"],
    [[43, 21], "not_found"],
    [[48, 21], "not_found"],
    [[51, 21], "not_found"],
    [[60, 21], "not_found"],
    [[67, 21], "not_found"],
    [[72, 21], "not_found"],
    [[75, 21], "not_found"],
    [[79, 21], "not_found"],
    [[80, 21], "not_found"],
    [[83, 21], "not_found"],
    [[88, 21], "not_found"],
    [[91, 21], "not_found"],
    [[96, 21], "not_found"],
    [[33, 22], "not_found"],
    [[38, 22], "not_found"],
    [[39, 22], "not_found"],
    [[40, 22], "not_found"],
    [[43, 22], "not_found"],
    [[48, 22], "not_found"],
    [[51, 22], "not_found"],
    [[60, 22], "not_found"],
    [[67, 22], "not_found"],
    [[72, 22], "not_found"],
    [[75, 22], "not_found"],
    [[79, 22], "not_found"],
    [[80, 22], "not_found"],
    [[83, 22], "not_found"],
    [[88, 22], "not_found"],
    [[91, 22], "not_found"],
    [[96, 22], "not_found"],
    [[33, 23], "not_found"],
    [[38, 23], "not_found"],
    [[39, 23], "not_found"],
    [[40, 23], "not_found"],
    [[43, 23], "not_found"],
    [[44, 23], "not_found"],
    [[47, 23], "not_found"],
    [[48, 23], "not_found"],
    [[51, 23], "not_found"],
    [[52, 23], "not_found"],
    [[60, 23], "not_found"],
    [[67, 23], "not_found"],
    [[68, 23], "not_found"],
    [[71, 23], "not_found"],
    [[72, 23], "not_found"],
    [[75, 23], "not_found"],
    [[76, 23], "not_found"],
    [[79, 23], "not_found"],
    [[80, 23], "not_found"],
    [[83, 23], "not_found"],
    [[88, 23], "not_found"],
    [[91, 23], "not_found"],
    [[92, 23], "not_found"],
    [[95, 23], "not_found"],
    [[96, 23], "not_found"],
    [[33, 24], "not_found"],
    [[39, 24], "not_found"],
    [[40, 24], "not_found"],
    [[44, 24], "not_found"],
    [[45, 24], "not_found"],
    [[46, 24], "not_found"],
    [[47, 24], "not_found"],
    [[52, 24], "not_found"],
    [[53, 24], "not_found"],
    [[60, 24], "not_found"],
    [[68, 24], "not_found"],
    [[69, 24], "not_found"],
    [[70, 24], "not_found"],
    [[71, 24], "not_found"],
    [[76, 24], "not_found"],
    [[77, 24], "not_found"],
    [[78, 24], "not_found"],
    [[79, 24], "not_found"],
    [[80, 24], "not_found"],
    [[83, 24], "not_found"],
    [[88, 24], "not_found"],
    [[92, 24], "not_found"],
    [[93, 24], "not_found"],
    [[94, 24], "not_found"],
    [[96, 24], "not_found"],
]

GOOGLE = "Google"
FUZZY = "Fuzzy"
SEARCH = "Search"
NOT_FOUND = "Not Found"


class NotFound:
    def __init__(self, stdscr):
        self.block = "■"
        self.stdscr = stdscr
        self.window = None
        self.logo_height = 24
        self.logo_width = 126
        self.color = Color.get_instance()

    def create(self):
        self._init_layout()
        self._make_not_found()
        self.window.refresh()

    def destroy(self):
        if not self.window is None:
            self.window.erase()
            self.window.refresh()

    def _init_layout(self):
        self.parent_height, self.parent_width = self.stdscr.getmaxyx()
        self.window = curses.newwin(self.parent_height - 4, self.parent_width, 0, 0)

    def _make_not_found(self):
        if self.parent_width < self.logo_width:
            self._make_not_found_small()
        else:
            self._make_not_found_big()

    def _make_not_found_small(self):
        start_index = 0
        title = "{0} {1} {2}".format(GOOGLE, FUZZY, SEARCH)
        title_begin_y = self.parent_height // 2 - 1
        title_begin_x = self.parent_width // 2 - len(title) // 2
        msg_begin_y = title_begin_y + 1
        msg_begin_x = title_begin_x + (len(title) - len(NOT_FOUND)) // 2

        # Write Google
        google = list(GOOGLE)
        first_o = True
        for i in range(len(google)):
            c = google[i]
            if c == "o":
                if first_o:
                    first_o = False
                    self.window.addstr(
                        title_begin_y + 0, title_begin_x + i, c, self.color.google("o")
                    )
                else:
                    self.window.addstr(
                        title_begin_y + 0, title_begin_x + i, c, self.color.google("o2")
                    )
            else:
                self.window.addstr(
                    title_begin_y + 0, title_begin_x + i, c, self.color.google(c)
                )

        # Write Fuzzy
        start_index += len(GOOGLE) + 1
        self.window.addstr(
            title_begin_y + 0, title_begin_x + start_index, FUZZY, self.color.fuzzy()
        )

        # Write Search
        start_index += len(FUZZY) + 1
        self.window.addstr(
            title_begin_y + 0, title_begin_x + start_index, SEARCH, self.color.search()
        )

        # Write Not Found
        self.window.addstr(
            msg_begin_y, msg_begin_x, NOT_FOUND, self.color.not_found() | curses.A_BOLD
        )

    # stdscr.getch doesn't work when I addstr to subwin
    def _make_not_found_big(self):
        logo_begin_x = self.parent_width // 2 - self.logo_width // 2
        logo_begin_y = self.parent_height // 2 - self.logo_height // 2

        for data in GOOGLER_NOT_FOUND:
            cordinate = data[0]
            c = data[1]
            x = cordinate[0]
            y = cordinate[1]
            if c in ("G", "o", "o2", "g", "l", "e"):
                self.window.addstr(
                    logo_begin_y + y,
                    logo_begin_x + x,
                    self.block,
                    self.color.google(c, style="normal"),
                )
            elif c == "fuzzy":
                self.window.addstr(
                    logo_begin_y + y,
                    logo_begin_x + x,
                    self.block,
                    self.color.fuzzy(style="normal"),
                )
            elif c == "search":
                self.window.addstr(
                    logo_begin_y + y,
                    logo_begin_x + x,
                    self.block,
                    self.color.search(style="normal"),
                )
            elif c == "not_found":
                self.window.addstr(
                    logo_begin_y + y,
                    logo_begin_x + x,
                    self.block,
                    self.color.not_found(style="normal"),
                )


if __name__ == "__main__":

    class TestNotFound(NotFound):
        def run(self):
            self._loop()

        def _loop(self):
            self.create()

            while True:
                pass


if __name__ == "__main__":
    import curses
    import signal
    import sys, os

    # local

    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    import utils, model
    from model import Model

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # initscr() returns a window object representing the entire screen.
    stdscr = curses.initscr()

    # turn off automatic echoing of keys to the screen
    curses.noecho()
    # Buffering off
    # https://docs.python.org/ja/3/library/curses.html#curses.cbreak
    curses.cbreak()
    # Aable the mouse cursor.
    curses.curs_set(0)

    target = TestNotFound(stdscr)
    error = None
    try:
        target.run()
    except curses.error as e:
        error = str(e)
    finally:
        target._end_curses()
        if error != None:
            print(error)

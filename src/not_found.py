import curses
import curses.ascii

# local

import debug
#
# Generate by https://lazesoftware.com/tool/hugeaagen/
#                                  ■                              
#   ■■■■■                          ■                              
#  ■■   ■                          ■                              
# ■■         ■■■■    ■■■■    ■■■■  ■    ■■■■  ■ ■■                
# ■         ■■  ■■  ■■  ■■  ■■  ■  ■   ■■  ■  ■■                  
# ■    ■■■  ■    ■  ■    ■  ■   ■  ■   ■   ■■ ■■                  
# ■      ■  ■    ■  ■    ■  ■■  ■  ■   ■■■■■■ ■                   
# ■■     ■  ■    ■  ■    ■   ■■■   ■   ■      ■                   
#  ■■   ■■  ■■  ■■  ■■  ■■  ■■     ■   ■■     ■                   
#   ■■■■■    ■■■■    ■■■■    ■■■■  ■    ■■■■  ■                   
#                           ■   ■■                                
#                           ■■■■■                                 
#                                                                 
#                                                                 
#                                                                 
#                                                                ■
# ■■    ■■                   ■■■■■■                              ■
# ■■■   ■■          ■        ■                                   ■
# ■ ■   ■■   ■■■■  ■■■■      ■       ■■■■   ■   ■■  ■ ■■■    ■■■■■
# ■  ■  ■■  ■■  ■■  ■        ■      ■■  ■■  ■   ■■  ■■  ■■  ■■  ■■
# ■  ■■ ■■  ■    ■  ■        ■■■■■■ ■    ■  ■   ■■  ■    ■  ■    ■
# ■   ■ ■■  ■    ■  ■        ■      ■    ■  ■   ■■  ■    ■  ■    ■
# ■    ■■■  ■    ■  ■        ■      ■    ■  ■   ■■  ■    ■  ■    ■
# ■    ■■■  ■■  ■■  ■■       ■      ■■  ■■  ■■  ■■  ■    ■  ■■  ■■
# ■     ■■   ■■■■    ■■      ■       ■■■■    ■■■■■  ■    ■   ■■■ ■
# 
GOOGLER_NOT_FOUND = [
    [[34, 0], "l"],
    [[3, 1], "g"],
    [[4, 1], "g"],
    [[5, 1], "g"],
    [[6, 1], "g"],
    [[7, 1], "g"],
    [[34, 1], "l"],
    [[2, 2], "g"],
    [[3, 2], "g"],
    [[7, 2], "g"],
    [[34, 2], "l"],
    [[1, 3], "g"],
    [[2, 3], "g"],
    [[12, 3], "o"],
    [[13, 3], "o"],
    [[14, 3], "o"],
    [[15, 3], "o"],
    [[20, 3], "o2"],
    [[21, 3], "o2"],
    [[22, 3], "o2"],
    [[23, 3], "o2"],
    [[28, 3], "g2"],
    [[29, 3], "g2"],
    [[30, 3], "g2"],
    [[31, 3], "g2"],
    [[34, 3], "l"],
    [[39, 3], "e"],
    [[40, 3], "e"],
    [[41, 3], "e"],
    [[42, 3], "e"],
    [[45, 3], "r"],
    [[47, 3], "r"],
    [[48, 3], "r"],
    [[1, 4], "g"],
    [[11, 4], "o"],
    [[12, 4], "o"],
    [[15, 4], "o"],
    [[16, 4], "o"],
    [[19, 4], "o2"],
    [[20, 4], "o2"],
    [[23, 4], "o2"],
    [[24, 4], "o2"],
    [[27, 4], "g2"],
    [[28, 4], "g2"],
    [[31, 4], "g2"],
    [[34, 4], "l"],
    [[38, 4], "e"],
    [[39, 4], "e"],
    [[42, 4], "e"],
    [[45, 4], "r"],
    [[46, 4], "r"],
    [[1, 5], "g"],
    [[6, 5], "g"],
    [[7, 5], "g"],
    [[8, 5], "g"],
    [[11, 5], "o"],
    [[16, 5], "o"],
    [[19, 5], "o2"],
    [[24, 5], "o2"],
    [[27, 5], "g2"],
    [[31, 5], "g2"],
    [[34, 5], "l"],
    [[38, 5], "e"],
    [[42, 5], "e"],
    [[43, 5], "e"],
    [[45, 5], "r"],
    [[46, 5], "r"],
    [[1, 6], "g"],
    [[8, 6], "g"],
    [[11, 6], "o"],
    [[16, 6], "o"],
    [[19, 6], "o2"],
    [[24, 6], "o2"],
    [[27, 6], "g2"],
    [[28, 6], "g2"],
    [[31, 6], "g2"],
    [[34, 6], "l"],
    [[38, 6], "e"],
    [[39, 6], "e"],
    [[40, 6], "e"],
    [[41, 6], "e"],
    [[42, 6], "e"],
    [[43, 6], "e"],
    [[45, 6], "r"],
    [[1, 7], "g"],
    [[2, 7], "g"],
    [[8, 7], "g"],
    [[11, 7], "o"],
    [[16, 7], "o"],
    [[19, 7], "o2"],
    [[24, 7], "o2"],
    [[28, 7], "g2"],
    [[29, 7], "g2"],
    [[30, 7], "g2"],
    [[34, 7], "l"],
    [[38, 7], "e"],
    [[45, 7], "r"],
    [[2, 8], "g"],
    [[3, 8], "g"],
    [[7, 8], "g"],
    [[8, 8], "g"],
    [[11, 8], "o"],
    [[12, 8], "o"],
    [[15, 8], "o"],
    [[16, 8], "o"],
    [[19, 8], "o2"],
    [[20, 8], "o2"],
    [[23, 8], "o2"],
    [[24, 8], "o2"],
    [[27, 8], "g2"],
    [[28, 8], "g2"],
    [[34, 8], "l"],
    [[38, 8], "e"],
    [[39, 8], "e"],
    [[45, 8], "r"],
    [[3, 9], "g"],
    [[4, 9], "g"],
    [[5, 9], "g"],
    [[6, 9], "g"],
    [[7, 9], "g"],
    [[12, 9], "o"],
    [[13, 9], "o"],
    [[14, 9], "o"],
    [[15, 9], "o"],
    [[20, 9], "o2"],
    [[21, 9], "o2"],
    [[22, 9], "o2"],
    [[23, 9], "o2"],
    [[28, 9], "g2"],
    [[29, 9], "g2"],
    [[30, 9], "g2"],
    [[31, 9], "g2"],
    [[34, 9], "l"],
    [[39, 9], "e"],
    [[40, 9], "e"],
    [[41, 9], "e"],
    [[42, 9], "e"],
    [[45, 9], "r"],
    [[27, 10], "g2"],
    [[31, 10], "g2"],
    [[32, 10], "g2"],
    [[27, 11], "g2"],
    [[28, 11], "g2"],
    [[29, 11], "g2"],
    [[30, 11], "g2"],
    [[31, 11], "g2"],
    [[1, 16], "not_found"],
    [[2, 16], "not_found"],
    [[7, 16], "not_found"],
    [[8, 16], "not_found"],
    [[28, 16], "not_found"],
    [[29, 16], "not_found"],
    [[30, 16], "not_found"],
    [[31, 16], "not_found"],
    [[32, 16], "not_found"],
    [[33, 16], "not_found"],
    [[64, 16], "not_found"],
    [[1, 17], "not_found"],
    [[2, 17], "not_found"],
    [[3, 17], "not_found"],
    [[7, 17], "not_found"],
    [[8, 17], "not_found"],
    [[19, 17], "not_found"],
    [[28, 17], "not_found"],
    [[64, 17], "not_found"],
    [[1, 18], "not_found"],
    [[3, 18], "not_found"],
    [[7, 18], "not_found"],
    [[8, 18], "not_found"],
    [[12, 18], "not_found"],
    [[13, 18], "not_found"],
    [[14, 18], "not_found"],
    [[15, 18], "not_found"],
    [[18, 18], "not_found"],
    [[19, 18], "not_found"],
    [[20, 18], "not_found"],
    [[21, 18], "not_found"],
    [[28, 18], "not_found"],
    [[36, 18], "not_found"],
    [[37, 18], "not_found"],
    [[38, 18], "not_found"],
    [[39, 18], "not_found"],
    [[43, 18], "not_found"],
    [[47, 18], "not_found"],
    [[48, 18], "not_found"],
    [[51, 18], "not_found"],
    [[53, 18], "not_found"],
    [[54, 18], "not_found"],
    [[55, 18], "not_found"],
    [[60, 18], "not_found"],
    [[61, 18], "not_found"],
    [[62, 18], "not_found"],
    [[63, 18], "not_found"],
    [[64, 18], "not_found"],
    [[1, 19], "not_found"],
    [[4, 19], "not_found"],
    [[7, 19], "not_found"],
    [[8, 19], "not_found"],
    [[11, 19], "not_found"],
    [[12, 19], "not_found"],
    [[15, 19], "not_found"],
    [[16, 19], "not_found"],
    [[19, 19], "not_found"],
    [[28, 19], "not_found"],
    [[35, 19], "not_found"],
    [[36, 19], "not_found"],
    [[39, 19], "not_found"],
    [[40, 19], "not_found"],
    [[43, 19], "not_found"],
    [[47, 19], "not_found"],
    [[48, 19], "not_found"],
    [[51, 19], "not_found"],
    [[52, 19], "not_found"],
    [[55, 19], "not_found"],
    [[56, 19], "not_found"],
    [[59, 19], "not_found"],
    [[60, 19], "not_found"],
    [[63, 19], "not_found"],
    [[64, 19], "not_found"],
    [[1, 20], "not_found"],
    [[4, 20], "not_found"],
    [[5, 20], "not_found"],
    [[7, 20], "not_found"],
    [[8, 20], "not_found"],
    [[11, 20], "not_found"],
    [[16, 20], "not_found"],
    [[19, 20], "not_found"],
    [[28, 20], "not_found"],
    [[29, 20], "not_found"],
    [[30, 20], "not_found"],
    [[31, 20], "not_found"],
    [[32, 20], "not_found"],
    [[33, 20], "not_found"],
    [[35, 20], "not_found"],
    [[40, 20], "not_found"],
    [[43, 20], "not_found"],
    [[47, 20], "not_found"],
    [[48, 20], "not_found"],
    [[51, 20], "not_found"],
    [[56, 20], "not_found"],
    [[59, 20], "not_found"],
    [[64, 20], "not_found"],
    [[1, 21], "not_found"],
    [[5, 21], "not_found"],
    [[7, 21], "not_found"],
    [[8, 21], "not_found"],
    [[11, 21], "not_found"],
    [[16, 21], "not_found"],
    [[19, 21], "not_found"],
    [[28, 21], "not_found"],
    [[35, 21], "not_found"],
    [[40, 21], "not_found"],
    [[43, 21], "not_found"],
    [[47, 21], "not_found"],
    [[48, 21], "not_found"],
    [[51, 21], "not_found"],
    [[56, 21], "not_found"],
    [[59, 21], "not_found"],
    [[64, 21], "not_found"],
    [[1, 22], "not_found"],
    [[6, 22], "not_found"],
    [[7, 22], "not_found"],
    [[8, 22], "not_found"],
    [[11, 22], "not_found"],
    [[16, 22], "not_found"],
    [[19, 22], "not_found"],
    [[28, 22], "not_found"],
    [[35, 22], "not_found"],
    [[40, 22], "not_found"],
    [[43, 22], "not_found"],
    [[47, 22], "not_found"],
    [[48, 22], "not_found"],
    [[51, 22], "not_found"],
    [[56, 22], "not_found"],
    [[59, 22], "not_found"],
    [[64, 22], "not_found"],
    [[1, 23], "not_found"],
    [[6, 23], "not_found"],
    [[7, 23], "not_found"],
    [[8, 23], "not_found"],
    [[11, 23], "not_found"],
    [[12, 23], "not_found"],
    [[15, 23], "not_found"],
    [[16, 23], "not_found"],
    [[19, 23], "not_found"],
    [[20, 23], "not_found"],
    [[28, 23], "not_found"],
    [[35, 23], "not_found"],
    [[36, 23], "not_found"],
    [[39, 23], "not_found"],
    [[40, 23], "not_found"],
    [[43, 23], "not_found"],
    [[44, 23], "not_found"],
    [[47, 23], "not_found"],
    [[48, 23], "not_found"],
    [[51, 23], "not_found"],
    [[56, 23], "not_found"],
    [[59, 23], "not_found"],
    [[60, 23], "not_found"],
    [[63, 23], "not_found"],
    [[64, 23], "not_found"],
    [[1, 24], "not_found"],
    [[7, 24], "not_found"],
    [[8, 24], "not_found"],
    [[12, 24], "not_found"],
    [[13, 24], "not_found"],
    [[14, 24], "not_found"],
    [[15, 24], "not_found"],
    [[20, 24], "not_found"],
    [[21, 24], "not_found"],
    [[28, 24], "not_found"],
    [[36, 24], "not_found"],
    [[37, 24], "not_found"],
    [[38, 24], "not_found"],
    [[39, 24], "not_found"],
    [[44, 24], "not_found"],
    [[45, 24], "not_found"],
    [[46, 24], "not_found"],
    [[47, 24], "not_found"],
    [[48, 24], "not_found"],
    [[51, 24], "not_found"],
    [[56, 24], "not_found"],
    [[60, 24], "not_found"],
    [[61, 24], "not_found"],
    [[62, 24], "not_found"],
    [[64, 24], "not_found"]
]

class NotFound:
  def __init__(self, stdscr, colors):
    self.block = "■"
    self.stdscr = stdscr
    self.parent_height, self.parent_width = stdscr.getmaxyx()
    # これを使って書き直す
    self.window = curses.newwin(self.parent_height - 4, self.parent_width, 0, 0)
    self.logo_height = 24
    self.logo_width = 64
    self.logo_begin_x = self.parent_width // 2 - self.logo_width // 2
    self.logo_begin_y = self.parent_height // 2 - self.logo_height // 2
    self.colors = colors

  def create(self):
    self._init_curses()
    self._make_not_found()
    self.window.refresh()

  def destroy(self):
    self.window.erase()
    self.window.refresh()
    self.stdscr.refresh()

  def _init_curses(self):
    """ Inits the curses application """
    # turn off automatic echoing of keys to the screen
    curses.noecho()
    # Buffering off
    # https://docs.python.org/ja/3/library/curses.html#curses.cbreak
    curses.cbreak()
    # Aable the mouse cursor.
    curses.curs_set(0)

  def _end_curses(self, end=True):
    """ Terminates the curses application. """
    curses.nocbreak()
    self.window.keypad(0)
    if end:
      curses.echo()
      curses.endwin()

  # stdscr.getch doesn't work when I addstr to subwin
  def _make_not_found(self):
    for data in GOOGLER_NOT_FOUND:
      cordinate = data[0]
      color = data[1]
      x = cordinate[0]
      y = cordinate[1]
      if color in ('g', 'g2'):
        self.window.addstr(
            self.logo_begin_y + y, self.logo_begin_x + x, self.block, self.colors.googler_g)
      elif color == 'o':
        self.window.addstr(
            self.logo_begin_y + y, self.logo_begin_x + x, self.block, self.colors.googler_o)
      elif color == 'o2':
        self.window.addstr(
            self.logo_begin_y + y, self.logo_begin_x + x, self.block, self.colors.googler_o2)
      elif color == 'l':
        self.window.addstr(
            self.logo_begin_y + y, self.logo_begin_x + x, self.block, self.colors.googler_l)
      elif color == 'e':
        self.window.addstr(
            self.logo_begin_y + y, self.logo_begin_x + x, self.block, self.colors.googler_e)
      elif color == 'r':
        self.window.addstr(
            self.logo_begin_y + y, self.logo_begin_x + x, self.block, self.colors.googler_r)
      elif color == 'not_found':
        self.window.addstr(
            self.logo_begin_y + y, self.logo_begin_x + x, self.block, self.colors.not_found)

  def _loop(self):
    self.create()

    while True:
      pass

if __name__ == '__main__':
  import curses
  import signal

  # local

  from colors import Colors
  from model import Model

  signal.signal(signal.SIGINT, signal.SIG_DFL)

  # initscr() returns a window object representing the entire screen.
  stdscr = curses.initscr()
  colors = Colors(curses)
  stdscr.bkgd(colors.normal)

  NotFound(stdscr, colors)._loop()

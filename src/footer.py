import curses

# local

import debug
from multibyte import Multibyte

KEY_ENTER = 10

class Footer:
  def __init__(self, stdscr, colors, model):
    self.message = 'googler (? for help)'
    self.stdscr = stdscr
    self.colors = colors
    self.model = model
    self.multibyte = Multibyte(self.stdscr)

  def create(self):
    self._init_curses()
    self._make_footer()

  def _wait_input_prompt(self):
    self.create()
    inp = self._loop()
    self._end_curses()
    return inp

  def _init_curses(self):
    """ Inits the curses application """
    # turn off automatic echoing of keys to the screen
    curses.echo()
    # Buffering off
    # https://docs.python.org/ja/3/library/curses.html#curses.cbreak
    curses.cbreak()
    # Aable the mouse cursor.
    curses.curs_set(1)

  def _finish_curses(self):
    self._end_curses(self, False)

  def _end_curses(self, end = True):
    """ Terminates the curses application. """
    curses.nocbreak()
    self.stdscr.keypad(0)
    curses.echo()
    if end:
      curses.endwin()

  # stdscr.getch doesn't work when I addstr to subwin
  def _make_footer(self):
    maxy, maxx = self.stdscr.getmaxyx()
    self.stdscr.addstr(maxy - 1, 0, self.message, self.colors.prompt)

  def _loop(self):
    maxy, maxx = self.stdscr.getmaxyx()
    self.stdscr.move(maxy - 1, len(self.message) + 1)
    self.stdscr.refresh()

    inp = ''
    while True:
        try:
            user_input = self.multibyte.getch()
        except curses.error:
            continue
        except KeyboardInterrupt:
            break

        # Ah hitting enter, return the index of the selected list element.
        if user_input == curses.KEY_ENTER or user_input == KEY_ENTER:
          return inp
        else:
          inp += chr(user_input)
          self.model.update_query(inp)

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
  model = Model([])

  inp = Footer(stdscr, colors, model)._wait_input_prompt()
  print('query:', model.query)
  print('result:', inp)

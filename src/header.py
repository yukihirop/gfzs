import curses

GOOGLE = 'Google'
FUZZY = 'Fuzzy'
SEARCH = 'Search'

class Header:
  def __init__(self, stdscr, colors):
    self.version = '(v0.0.1)'
    self.copyright = 'Copyright ©︎ 2021 yukihirop'
    self.stdscr = stdscr
    self.colors = colors

  def create(self):
    self._init_curses()
    self._init_layout()
    self._make_header()
    self.window.refresh()

  def reset(self):
    self._init_curses()
    self.window.erase()
    self._init_layout()
    self._make_header()
    self.window.refresh()

  def _init_layout(self):
    self.parent_height, self.parent_width = self.stdscr.getmaxyx()
    self.window = curses.newwin(2, self.parent_width, 0, 0)

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

  # https://stackoverflow.com/a/53016371/9434894
  def _make_header(self):
    start_index = 0
    # Write Google
    google = list(GOOGLE)
    first_o = True
    for i in range(len(google)):
      c = google[i]
      if c in ('G', 'g'):
        self.window.addstr(0, i, c, self.colors.google_g | curses.A_BOLD)
      elif c == 'o':
        if first_o:
          first_o = False
          self.window.addstr(0, i, c, self.colors.google_o | curses.A_BOLD)
        else:
          self.window.addstr(0, i, c, self.colors.google_o2 | curses.A_BOLD)
      elif c == 'l':
        self.window.addstr(0, i, c, self.colors.google_l | curses.A_BOLD)
      elif c == 'e':
        self.window.addstr(0, i, c, self.colors.google_e | curses.A_BOLD)
    
    # Write Fuzzy
    start_index += len(GOOGLE) + 1
    self.window.addstr(0, start_index, FUZZY, self.colors.fuzzy | curses.A_BOLD)

    # Write Search
    start_index += len(FUZZY) + 1
    self.window.addstr(0, start_index, SEARCH,
                       self.colors.search | curses.A_BOLD)
    
    # Write verion
    start_index += len(SEARCH) + 1
    self.window.addstr(0, start_index, self.version,
                       self.colors.version | curses.A_BOLD)
    
    # Write Copyright
    self.window.addstr(0, self.parent_width - len(self.copyright),
                       self.copyright, self.colors.header | curses.A_BOLD)
    self.window.hline(1, 0, curses.ACS_HLINE | self.colors.hline, self.parent_width)

  def _loop(self):
    self.create()

    while True:
      try:
          user_input = self.window.getch()
      except curses.error:
          continue
      except KeyboardInterrupt:
          break

      if user_input == curses.KEY_RESIZE:
        self.reset()


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

  Header(stdscr, colors)._loop()

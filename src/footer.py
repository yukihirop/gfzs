import debug

ENTER = "\n"

class Footer:
  def __init__(self, stdscr, colors):
    self.message = 'googler (? for help)'
    self.stdscr = stdscr
    self.colors = colors

  def wait_input_prompt(self):
    footer = self._make_footer()
    inp = self._wait_input_prompt(footer)
    self._end_curses()
    return inp

  def _init_curses(self):
    """ Inits the curses application """
    # Something

  def _end_curses(self):
    """ Terminates the curses application. """
    curses.nocbreak()
    self.stdscr.keypad(0)
    curses.echo()
    curses.endwin()

  def _make_footer(self):
    maxy, maxx = self.stdscr.getmaxyx()
    footer = self.stdscr.subwin(
        1,
        maxx - 1,
        maxy - 1,
        0
    )
    footer.addstr(self.message, self.colors.prompt)
    return footer

  def _wait_input_prompt(self, footer):
    maxy, _ = self.stdscr.getmaxyx()

    self.stdscr.move(maxy - 1, len(self.message) + 1)
    footer.refresh()

    inp = ''
    while True:
        try:
            user_input = self.stdscr.get_wch()
        except curses.error:
            continue
        except KeyboardInterrupt:
            break

        # Ah hitting enter, return the index of the selected list element.
        if user_input == ENTER:
          return inp
        else:
          inp += user_input
          debug.log(inp)

if __name__ == '__main__':
  import curses
  import signal

  # local

  from colors import Colors

  signal.signal(signal.SIGINT, signal.SIG_DFL)

  # initscr() returns a window object representing the entire screen.
  stdscr = curses.initscr()
  # turn off automatic echoing of keys to the screen
  curses.echo()
  # Enable non-blocking mode. keys are read directly, without hitting enter.
  curses.nocbreak()
  # Able the mouse cursor.
  curses.curs_set(1)
  stdscr.keypad(0)

  colors = Colors(curses)
  stdscr.bkgd(colors.normal)
  stdscr.refresh()

  inp = Footer(stdscr, colors).wait_input_prompt()
  print('result: ', inp)

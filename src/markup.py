import re

# local

import debug
from multibyte import Multibyte

class Markup:
  def __init__(self, colors):
    self.colors = colors
    self.multibyte = Multibyte()

  def parse(self, text, search_text):
    result = {}

    if search_text is None or search_text is '':
      return result

    remake_text = self.multibyte.marked_full_width(text)
    search_texts = [item for item in search_text.split(" ") if item]

    for st in search_texts:
      # Markup Partial
      result_at_partial = self._parse_as_partial(remake_text, st)
      for item in result_at_partial:
        result[item] = result_at_partial[item]

      # Markup Char
      result_at_char = self._parse_as_char(remake_text, st)
      for item in result_at_char:
          if not item in result:
            result[item] = result_at_char[item]
      
    return result

  def _parse_as_partial(self, remake_text, search_text):
    result = {}
    remake_search_text = self.multibyte.marked_full_width(search_text)

    for m in re.finditer(remake_search_text, remake_text):
        if m is None:
          continue

        if not search_text in result:
          result[search_text] = []

        span = m.span()
        result[search_text].append({
            "half_width": {
                "start_index": span[0],
                "end_index": span[1]
            },
            "color": self.colors.markup_partial,
            "match": search_text,
            "_type": "partial",
        })
    
    return result

  def _parse_as_char(self, remake_text, search_text):
    result = {}
    char_pattern = re.compile(r'[{0}]'.format(search_text))

    for m in char_pattern.finditer(remake_text):
        if m is None:
          continue

        if not search_text in result:
          result[search_text] = []

        span = m.span()
        result[search_text].append({
            "half_width": {
                "start_index": span[0],
                "end_index": span[1]
            },
            "color": self.colors.markup_char,
            "match": m.group(),
            "_type": "char",
        })

    return result


if __name__ == '__main__':
  import curses

  # local

  from colors import Colors

  try:
    # initscr() returns a window object representing the entire screen.
    stdscr = curses.initscr()
    colors = Colors(curses)

    markup = Markup(colors)
    text = "Rustは非常に高速でメモリ効率が高くランタイムやガベージコレクタがないため、パフォーマンス重視のサービスを実装できますし、組込み機器上で実行したり他の言語との調和も簡単にできます。 信頼性. Rustの豊かな型システムと所有権 ..."
    
    search_text = "Rust 非常 効率"
    result = markup.parse(text, search_text)
    print('Partial: ', result)

    search_text = "パピプペポ"
    result = markup.parse(text, search_text)
    print('Char: ', result)

    # search_text = None
    # result = markup.parse(text, search_text)
    # print('None: ', result)

    # search_text = ''
    # result = markup.parse(text, search_text)
    # print('Blank: ', result)

    # search_text = '\0'
    # result = markup.parse(text, search_text)
    # print('Null: ', result)

  finally:
    curses.endwin()

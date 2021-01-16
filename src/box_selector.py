# ref: https://github.com/NikolaiT/Scripts/blob/master/scripts/python/curses/text_selector.py

import curses
import unicodedata
import textwrap

# local

import debug
from colors import Colors
from not_found import NotFound

class BoxSelectorHelper:
  def __init__(self):
    self.current_selected = 0
    self.last = 1
    self.topy = 1
    self.top_textbox = None
    self.pad_begin_y = 0

  def update_attributues(self, current_selected, last, topy, top_textbox):
    self.current_selected = current_selected
    self.last = last
    self.topy = topy
    self.top_textbox = top_textbox

class BoxSelector:
  """Display options build from a list of strings in a (unix) terminal.
     The user can browser though the textboxes and select one with enter.
  """

  def __init__(self, stdscr, colors, model):
    """Create a BoxSelector object.
       'data' is list of string. Each string is used to build
       a textbox.
    """
    self.stdscr = stdscr
    self._init_layout()
    self.colors = colors
    self.model = model
    self.stop_loop = False
    self.textboxes = []
    self.helper = BoxSelectorHelper()
    self.not_found = NotFound(stdscr, colors)
    # Element parameters. Channge them here.
    self.TEXTBOX_HEIGHT = 8
    self.PAD_WIDTH = 400
    self.PAD_HEIGHT = 1000

  @property
  def current_selected(self) -> int:
    return self.helper.current_selected

  def init_properties_after_create(self):
    current_selected = 0
    textboxes_len = len(self.textboxes)

    if textboxes_len > 0:
      top_textbox = self.textboxes[0]
      topy, _ = self._refresh_view(top_textbox)
      if textboxes_len > 1:
        last = 1
      else:
        last = 0

      self.helper.update_attributues(current_selected, last, topy, top_textbox)

  def create(self, pad_begin_y = 0):
    self.helper.pad_begin_y = pad_begin_y
    self._init_curses()
    self._create_pad()
    self.textboxes = self._make_textboxes()
    if len(self.textboxes) > 0:
      self._refresh_view(self.textboxes[0])

  def destroy(self):
    self._delete_pad()
  
  def update_query(self, query):
    self.model.update_query(query)

  def reset(self):
    self._init_curses()
    self._reset_pad()
    self.textboxes = self._make_textboxes()
    if len(self.textboxes) > 0:
      self.not_found.destroy()
      self._refresh_view(self.textboxes[0])
    else:
      self.window.clear()
      self.window.refresh()
      self.not_found.create()

  def _pick(self, pad_begin_y = 0):
    """ Just run this when you want to spawn the selection process. """
    self.create(pad_begin_y)
    picked = self._loop()
    self._end_curses()

    return picked

  def _init_layout(self):
    self.height, self.width = self.stdscr.getmaxyx()
    # 「2」 is the height of the header or footer
    # 「4」 = header + footer height
    self.window = curses.newwin(self.height - 4, self.width, 2, 0)
    # https://stackoverflow.com/a/17369532/9434894
    self.window.keypad(1)

  def _init_curses(self):
    """ Inits the curses application """
    # turn off automatic echoing of keys to the screen
    curses.noecho()
    # Enable non-blocking mode. keys are read directly, without hitting enter.
    curses.cbreak()
    # Disable the mouse cursor.
    curses.curs_set(0)

  def _finish_curses(self):
    self._end_curses(False)

  def _end_curses(self, end = True):
    """ Terminates the curses application. """
    curses.nocbreak()
    self.window.keypad(0)
    if end:
      curses.echo()
      curses.endwin()

  def _delete_pad(self):
    self.pad.clear()
    self.window.refresh()

  def _reset_pad(self):
    self._delete_pad()
    self._init_layout()
    self._create_pad()

  def _create_pad(self):
    """ Creates a big self.pad to place the textboxes in. """
    self.pad = curses.newpad(self.PAD_HEIGHT, self.PAD_WIDTH)
    self.pad.box()
    self.window.refresh()

  def _make_textboxes(self):
    """ Build the textboxes in the pad center and put them in the
        horizontal middle of the pad. """
    textboxes = []
    i = 1
    data = self.model.find()

    if len(data) == 0:
      return textboxes

    for s in data:
        textbox = self.pad.derwin(
            self.TEXTBOX_HEIGHT,
            self.width - 4,
            i + self.helper.pad_begin_y,
            2
        )

        textboxes.append(textbox)
        i += self.TEXTBOX_HEIGHT

    # When all are displayed as multi-byte character strings
    abstract_line_len = self.width//2
    for k in range(len(textboxes)):
        textboxes[k].box()

        title = data[k].get('title')
        url = data[k].get('url')
        abstract = data[k].get('abstract')

        textboxes[k].addstr(2, 2, '%s%-3s' %
                          ('', str(k + 1) + '.'), self.colors.index)
        textboxes[k].addstr(2, 6, title, self.colors.title | curses.A_BOLD)
        textboxes[k].addstr(3, 6, url, self.colors.url | curses.A_BLINK)
        lines = textwrap.wrap(abstract, abstract_line_len)
        for l in range(len(lines)):
          textboxes[k].addstr(4 + l, 6, lines[l], self.colors.abstract)

    return textboxes

  def _refresh_view(self, window):
    """ Refresh textboxes """
    cy, cx = window.getbegyx()

    per_page = self.height // self.TEXTBOX_HEIGHT
    display_limit_pos_y = self.TEXTBOX_HEIGHT * (per_page - 1)
    display_limit_pos_x = self.width - 1
    
    # Since the display of the last pad is cut off, display_limit_pos_y + self.helper.pad_begin_y
    display_limit_pos_y += self.helper.pad_begin_y

    self.pad.refresh(cy, cx, 1 + self.helper.pad_begin_y, 2, display_limit_pos_y, display_limit_pos_x)
    return (cy, cx)

  def update_view_in_loop(self) -> bool:
    textboxes = self.textboxes
    textboxes_len = len(textboxes)

    if textboxes_len == 0:
      return False

    current_selected = self.current_selected
    last = self.helper.last
    topy = self.helper.topy
    top_textbox = self.helper.top_textbox

    # Highligth the selected one, the last selected textbox should
    # become normal again.
    if last == current_selected == 0:
      textboxes[current_selected].border(self.colors.highlight)
    else:
      textboxes[current_selected].border(self.colors.highlight)
      textboxes[last].border()

    # Paging

    # While the textbox can be displayed on the page with the current top_textbox,
    # don't after the view. When this becomes impossible,
    # center the view to last displayable textbox on the previous view.
    cy, cx = textboxes[current_selected].getbegyx()
    per_page = self.height//self.TEXTBOX_HEIGHT

    # The current window is to far down. Switch the top textbox.
    # When you reach the bottom, redisplay the current box at the top
    if ((topy + self.height - self.TEXTBOX_HEIGHT) <= cy):
      top_textbox = textboxes[current_selected]

    # The current window is to far up. There is a better way though...
    # Update the top until you reach the top of the screen.
    if topy >= cy + self.TEXTBOX_HEIGHT:
      if (current_selected < per_page - 1):
        top_textbox = textboxes[0]
      else:
        top_textbox = textboxes[current_selected - per_page + 1]

    if last == 0:
      if (current_selected > per_page):
        top_textbox = textboxes[current_selected- per_page + 2]

    if last != current_selected:
      last = current_selected

    refresh_topy, _ = self._refresh_view(top_textbox)

    self.textboxes = textboxes
    self.helper.update_attributues(
        current_selected, last, refresh_topy, top_textbox)

    return True

  def handle_key_in_loop(self, user_input):
    textboxes = self.textboxes
    textboxes_len = len(textboxes)

    if textboxes_len == 0:
      return

    current_selected = self.current_selected
    per_page = self.height//self.TEXTBOX_HEIGHT

    # Vim like KEY_UP/KEY_DOWN with j(DOWN) and k(UP)
    if textboxes_len > 1 and user_input == curses.KEY_DOWN:
      if (current_selected >= textboxes_len-1):
        current_selected = 0  # wrap around.
      else:
        current_selected += 1
    elif textboxes_len > 1 and user_input == curses.KEY_UP:
        if current_selected == 0:
          current_selected = textboxes_len - 1  # wrap around.
        else:
          current_selected -= 1
    elif textboxes_len > per_page and user_input == curses.KEY_RIGHT:
        next_pagetop_index = (per_page - 1) * \
           (current_selected // (per_page - 1) + 1)
        if (next_pagetop_index <= textboxes_len-1):
          current_selected = next_pagetop_index
        else:
          current_selected = 0  # wrap around.
    elif textboxes_len > per_page and user_input == curses.KEY_RIGHT:
        current_pagetop_index = (per_page - 1) * \
          (current_selected//(per_page - 1))
        if (current_pagetop_index == 0):
          current_selected = textboxes_len - per_page + 1  # wrap around.
        else:
          current_selected = current_pagetop_index - (per_page - 1)
    elif user_input == curses.KEY_RESIZE:
        self.reset()
    elif user_input == ord('q'):  # Quit without selecting.
        self.stop_loop = True

    self.helper.current_selected = current_selected

  def _loop(self):
    current_selected = 0
    textboxes_len = len(self.textboxes)

    if textboxes_len > 1:
      last = 1
    else:
      last = 0

    # See at the root textbox.
    if textboxes_len > 0:
      top_textbox = self.textboxes[0]
      topy, _ = self._refresh_view(top_textbox)
      self.helper.update_attributues(current_selected, last, topy, top_textbox)

    while True:
      if self.stop_loop:
        break

      self.update_view_in_loop()

      try:
          user_input = self.window.getch()
      except curses.error:
          continue
      except KeyboardInterrupt:
          break

      if user_input == curses.KEY_ENTER or user_input == 10:
        return int(self.current_selected)

      self.handle_key_in_loop(user_input)


if __name__ == '__main__':
  import curses
  import signal

  # local

  from colors import Colors
  from model import Model

  signal.signal(signal.SIGINT, signal.SIG_DFL)
  
  data = [
    {
      "abstract": "Rustは非常に高速でメモリ効率が高くランタイムやガベージコレクタがないため、パフォーマンス重視のサービスを実装できますし、組込み機器上で実行したり他の言語との調和も簡単にできます。 信頼性. Rustの豊かな型システムと所有権 ...",
      "matches": [
        {
          "offset": 0,
          "phrase": "Rust"
        },
        {
          "offset": 97,
          "phrase": "Rust"
        }
      ],
      "title": "Rustプログラミング言語",
      "url": "https://www.rust-lang.org/ja"
    },
    {
      "abstract": "Rust（ラスト）はMozillaが支援するオープンソースのシステムプログラミング言語である。 Rust言語は速度、並行性、安全性を言語仕様として保証するC言語、C++に代わるシステムプログラミング（英語版）に適したプログラミング言語を ...",
      "matches": [
        {
          "offset": 0,
          "phrase": "Rust"
        },
        {
          "offset": 48,
          "phrase": "Rust"
        }
      ],
      "metadata": "型付け： 静的型付け、強い型付け、型推論、構造... | 登場時期： 2010年7月7日 | ライセンス： Apache-2.0、MIT License | 影響を受けた言語： Alef、C++、C Sharp、Cyclon...",
      "title": "Rust (プログラミング言語) - Wikipedia",
      "url": "https://ja.wikipedia.org/wiki/Rust_(%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E8%A8%80%E8%AA%9E)"
    },
    {
      "abstract": "趣味でRustを使ってコンパイラを作ってるらいパン粉です。 プログラミング言語Rustの良さを雑にあっぴるしていきます。 では、早速cargo run！(このコマンドでRustのプログラムが実行される) C,C++のコードが出てくる ...",
      "matches": [
        {
          "offset": 3,
          "phrase": "Rust"
        },
        {
          "offset": 39,
          "phrase": "Rust"
        },
        {
          "offset": 84,
          "phrase": "Rust"
        }
      ],
      "metadata": "2020/02/04",
      "title": "プログラミング言語Rustのススメ - Qiita",
      "url": "https://qiita.com/elipmoc101/items/3c8b6d8332a9019e578c"
    },
    {
      "abstract": "開発者のRusthへの愛情が、実世界での採用に反映されつつある。2020年6月2日、TIOBEは、初めてRustがTIOBE indexのトップ20に入ったことを発表した。",
      "matches": [
        {
          "offset": 52,
          "phrase": "Rust"
        }
      ],
      "metadata": "2020/07/07",
      "title": "Rustが最も人気のあるプログラミング言語トップ20に - InfoQ",
      "url": "https://www.infoq.com/jp/news/2020/07/rust-top-20-language/"
    },
    {
      "abstract": "開発者向けQ＆Aサイト「Stack Overflow」は、先ごろ発表した年次開発者調査の結果を受け、プログラミング言語「Rust」が人気を集めているさまざまな理由について、ユーザーの生のコメントを紹介した。速度を犠牲にせず ...",
      "matches": [
        {
          "offset": 60,
          "phrase": "Rust"
        }
      ],
      "metadata": "2020/06/11",
      "title": "「Rust」はなぜ人気があるのか、Stack Overflowがユーザーの ...",
      "url": "https://www.atmarkit.co.jp/ait/articles/2006/11/news051.html"
    },
    {
      "abstract": "Rustは「最も愛されている」プログラミング言語として不動の地位を誇っているものの、その普及は遅々として進んでいないようだ。",
      "matches": [
        {
          "offset": 0,
          "phrase": "Rust"
        }
      ],
      "metadata": "2020/05/18",
      "title": "プログラミング言語「Rust」の普及に立ちはだかる壁 - ZDNet ...",
      "url": "https://japan.zdnet.com/article/35153014/"
    },
    {
      "abstract": "AWSはプログラミング言語「Rust」について、同社の長期的な戦略の重要に不可欠なコンポーネントだとしている。",
      "matches": [
        {
          "offset": 14,
          "phrase": "Rust"
        }
      ],
      "metadata": "2020/11/30",
      "title": "AWS、プログラミング言語「Rust」を重視する理由示す ...",
      "url": "https://japan.zdnet.com/article/35163089/"
    },
    {
      "abstract": "AmazonでJim Blandy, Jason Orendorff, 中田 秀基のプログラミングRust。アマゾンならポイント還元本が多数。Jim Blandy, Jason Orendorff, 中田 秀基作品ほか、お急ぎ便対象商品は当日お届けも可能。またプログラミングRustもアマゾン配送 ...",
      "matches": [
        {
          "offset": 49,
          "phrase": "Rust"
        },
        {
          "offset": 137,
          "phrase": "Rust"
        }
      ],
      "title": "プログラミングRust | Jim Blandy, Jason Orendorff, 中田 秀基 ...",
      "url": "https://www.amazon.co.jp/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0Rust-Jim-Blandy/dp/4873118557"
    },
    {
      "abstract": "オブジェクト指向と関数型の言語特徴を持ち、JavaやC#のようにVM（Virtual Machine）上の動作ではないため、既存のC言語のライブラリを直接扱える利点を持っています。またRustは、CやC++で発生しうる不正メモリアクセスに関する問題 ...",
      "matches": [
        {
          "offset": 92,
          "phrase": "Rust"
        }
      ],
      "title": "プログラミング言語Rust入門 | 増田 智明 |本 | 通販 | Amazon",
      "url": "https://www.amazon.co.jp/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E8%A8%80%E8%AA%9ERust%E5%85%A5%E9%96%80-%E5%A2%97%E7%94%B0-%E6%99%BA%E6%98%8E/dp/4822296857"
    },
    {
      "abstract": "このテキストのこの版では、Rust 2018 Editionのイディオムを使うため、Rust 1.41.0かそれ以降を使っており、すべてのプロジェクトの Cargo.toml に edition=\"2018\" とあることを前提にしています。 Rustをインストールしたりアップデート ...",
      "matches": [
        {
          "offset": 13,
          "phrase": "Rust"
        },
        {
          "offset": 42,
          "phrase": "Rust"
        },
        {
          "offset": 121,
          "phrase": "Rust"
        }
      ],
      "title": "The Rust Programming Language 日本語版 - The Rust ...",
      "url": "https://doc.rust-jp.rs/book-ja/"
    }
  ]

  # initscr() returns a window object representing the entire screen.
  stdscr = curses.initscr()
  colors = Colors(curses)
  stdscr.bkgd(colors.normal)
  stdscr.refresh()
  
  model = Model(data)
  model.update_query('Amazon')

  choice = BoxSelector(stdscr, colors, model)._pick(1)
  if choice != None:
    print(model.result[choice].get('title'))

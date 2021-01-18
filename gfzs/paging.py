import curses
import math

GOOGLE = 'Google'
FUZZY = 'Fuzzy'
SEARCH = 'Search'

class Paging:
  def __init__(self, stdscr, colors, view):
    self.stdscr = stdscr
    self.colors = colors
    self.view = view

  def create(self):
    self._init_layout()
    self._make_paging()
    self.window.refresh()

  def reset(self):
    self.destroy()
    self._init_layout()
    self._make_paging()
    self.window.refresh()

  def destroy(self):
    self.window.erase()

  def _init_layout(self):
    self.parent_height, self.parent_width = self.stdscr.getmaxyx()
    self.window = curses.newwin(2, self.parent_width, self.parent_height - 4, 0)

  def _end_curses(self, end=True):
    """ Terminates the curses application. """
    curses.nocbreak()
    self.window.keypad(0)
    if end:
      curses.echo()
      curses.endwin()

  # https://stackoverflow.com/a/53016371/9434894
  def _make_paging(self):
    begin_x = self.parent_width // 2 - 1
    current_selected = self.view.current_selected
    per_page = self.view.per_page
    data_size = self.view.data_size
    paging = "{0}/{1}".format((current_selected//per_page + 1), math.ceil(data_size/per_page))
    self.window.addstr(0, begin_x, paging,
                       self.colors.version | curses.A_BOLD)

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
  from box_selector import BoxSelector

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

  # turn off automatic echoing of keys to the screen
  curses.noecho()
  # Buffering off
  # https://docs.python.org/ja/3/library/curses.html#curses.cbreak
  curses.cbreak()
  # Aable the mouse cursor.
  curses.curs_set(0)

  colors = Colors(curses)
  stdscr.bkgd(colors.normal)

  model = Model(data)
  model.update_query('')
  _ = model.find()

  view = BoxSelector(stdscr, colors, model)
  view.helper.current_selected = 1
  view.helper.per_page = 5

  Paging(stdscr, colors, view)._loop()

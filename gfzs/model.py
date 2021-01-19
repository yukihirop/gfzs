from fuzzywuzzy import process as fuzzyprocess
from itertools import groupby
import re
import os, sys

# local

try:
    # need when 「python3 gfzs/model.py」
    if __name__ == '__main__':
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        from utils import debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.utils import debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    from utils import debug
    
class Model:
    # e.g.) collection = [{ title, url, abstract }, ...]
    def __init__(self, collection):
        self.collection = collection
        self.result = []
        self.query = self.old_query = None
        self.char_regex = re.compile(r'^\w|\W+')
        # https://qiita.com/ganariya/items/42fc0ed3dcebecb6b117
        self.code_regex = re.compile(
            '[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]')
        self.space_regex = re.compile(r'^[ 　]')
        self._result_nested_by_url = self._collection_nested_by("url")

    @property
    def summary_count(self):
        return len(self.collection)

    @property
    def data_size(self):
        return len(self.result)

    def should_search_again(self):
        return self.query != self.old_query

    def update_query(self, query):
        self.old_query = self.query
        self.query = query

    def push_query(self, char):
        self.old_query = self.query
        self.query += char

    def validate(self, query=None) -> bool:
        def fn(q):
            if q is None or q is '\0':
                return False

            trimed = self.code_regex.sub('', q)
            is_not_empty = trimed != ''

            if is_not_empty:
                m = self.space_regex.match(trimed)
                is_space_start = m != None
                if is_space_start:
                    return False

                m = self.char_regex.match(trimed)
                is_char = m != None
                return is_char
            else:
                return False

        if query is None:
            return fn(self.query)
        else:
            return fn(query)

    def find(self, query=None, score=30):
        if query != None and query != '':
            self.update_query(query)

        if self.validate():
            self.result = self._make_result_from_scored(score)
        else:
            self.result = self.collection

        return self.result

    def can_search_again(self):
        return self.query != self.old_query

    def _make_result_from_scored(self, score) -> list:
        result = []

        # From title
        scored_result_at_title = self._make_scored_result('title', score)
        # From abstract
        scored_result_at_abstract = self._make_scored_result('abstract', score)

        all_urls = list(set(scored_result_at_title.keys())) + list(set(scored_result_at_abstract.keys()))

        added = []
        for url in all_urls:
            score_at_title = 0
            score_at_abstract = 0
            title_len = 1
            abstract_len = 1

            if url in scored_result_at_title:
                data_at_title = scored_result_at_title[url]
                score_at_title = data_at_title["score"]
                title_len = len(data_at_title["data"]["title"])

            if url in scored_result_at_abstract:
                data_at_abstract = scored_result_at_abstract[url]
                score_at_abstract = data_at_abstract["score"]
                abstract_len = len(data_at_abstract["data"]["abstract"])

            score = (title_len / (title_len + abstract_len)) * score_at_title + (abstract_len / (title_len + abstract_len)) * score_at_abstract
            
            added.append({
                "score": score,
                "url": url
            })
        
        added = sorted(added, key=lambda x: x["score"], reverse=True)
        for item in added:
            url = item["url"]
            result.append(self._result_nested_by_url[url])

        return result


    def _make_scored_result(self, key, score) -> dict:
        result = {}

        # From key
        data_grouped_by_key = self._collection_nested_by(key)
        keys = data_grouped_by_key.keys()
        fuzzysorted = fuzzyprocess.extract(
            self.query, keys, limit=len(keys))

        # fuzzysorted reutrns an array of tuples: [('one', 45), ('three', 45), ('two', 0)]
        for item in fuzzysorted:
            if item[1] > score:
                scored = {}

                match_data = data_grouped_by_key.get(item[0])
                url = match_data["url"]
                result[url] = {
                    "data": match_data,
                    "score": item[1]
                }
        
        return result


    def _collection_nested_by(self, key) -> dict:
        data = {}

        for c in self.collection:
            key_data = c[key]
            data[key_data] = c

        return data


if __name__ == '__main__':
    import signal
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

    model = Model(data)
    result = model.find('Amazon', 30)

    print('Search (query=Amazon, score=30):  %d / %d' %
          (model.data_size, model.summary_count))
    for i in range(len(result)):
        print(result[i]['title'])

    result = model.find('\0', 30)
    print('Search (query=\0, score=30):  %d / %d' %
          (model.data_size, model.summary_count))
    for i in range(len(result)):
        print(result[i]['title'])

from fuzzywuzzy import process as fuzzyprocess
from itertools import groupby
import re
import os, sys

# local

try:
    # need when 「python3 gfzs/model.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        import runtime.opts as runtime_opts
        import utils.logger as logger

        if os.environ.get("DEBUG"):
            import utils.debug as debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        import gfzs.runtime.opts as runtime_opts
        import gfzs.utils.logger as logger

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    import runtime.opts as runtime_opts
    import utils.logger as logger

    if os.environ.get("DEBUG"):
        import utils.debug as debug


class Model:
    # e.g.) collection = [{ title, url, abstract }, ...]
    def __init__(self, collection):
        logger.debug("[Model] init")
        self.collection = collection
        self.result = []
        self.query = self.old_query = None
        self.errors = []

        self.char_regex = re.compile(r"^\w|\W+")
        # https://qiita.com/ganariya/items/42fc0ed3dcebecb6b117
        self.code_regex = re.compile(
            "[!\"#$%&'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]"
        )
        self.space_regex = re.compile(r"^[ 　]")
        self._result_nested_by_url = self._collection_nested_by("url")

    @property
    def data_size(self):
        return len(self.result)

    def update_query(self, query):
        logger.debug("[Model] update query from '%s' to '%s'" % (self.query, query))
        self.old_query = self.query
        self.query = query

    def push_query(self, char):
        self.old_query = self.query
        self.query += char

    def valid(self) -> bool:
        logger.debug("[Model] validate")
        if not self._validate_json(self.collection):
            logger.error("[Model] data is invalid.")
            self.errors.append(
                Exception(
                    "Invalid json format. Please pass in an array of json that keeps `title`, `url` and `abstract` as keys."
                )
            )
            return False
        elif not self._validate_blank(self.collection):
            logger.error("[Model] data is invalid.")
            self.errors.append(Exception("The result passed was empty."))
            return False
        else:
            logger.debug("[Model] data is valid")
            return True

    def validate_query(self, query=None) -> bool:
        logger.debug("[Model] validate query: '%s'" % query or self.query)

        def fn(q):
            if q is None or q is "\0":
                return False

            trimed = self.code_regex.sub("", q)
            is_not_empty = trimed != ""

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

    def find(self, query=None):
        logger.debug("[Model] find with query: '%s'" % query or self.query)
        score = runtime_opts.score

        if query != None and query != "":
            self.update_query(query)

        if self.validate_query():
            self.result = self._make_result_from_scored(score)
        else:
            self.result = self.collection

        return self.result

    def _validate_json(self, data) -> bool:
        result = []

        for item in data:
            if "url" in item:
                result.append(True)
            else:
                result.append(False)

            if "abstract" in item:
                result.append(True)
            else:
                result.append(False)

            if "url" in item:
                result.append(True)
            else:
                result.append(False)

        return all(result)

    def _validate_blank(self, data) -> bool:
        if len(data) != 0:
            return True
        else:
            return False

    def _make_result_from_scored(self, score) -> list:
        result = []

        # From title
        scored_result_at_title = self._make_scored_result("title", score)
        # From abstract
        scored_result_at_abstract = self._make_scored_result("abstract", score)

        all_urls = list(set(scored_result_at_title.keys())) + list(
            set(scored_result_at_abstract.keys())
        )

        added = []
        for url in set(all_urls):
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

            score = (title_len / (title_len + abstract_len)) * score_at_title + (
                abstract_len / (title_len + abstract_len)
            ) * score_at_abstract

            added.append({"score": score, "url": url})

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
        fuzzysorted = fuzzyprocess.extract(self.query, keys, limit=len(keys))

        # fuzzysorted reutrns an array of tuples: [('one', 45), ('three', 45), ('two', 0)]
        for item in fuzzysorted:
            if item[1] > score:
                scored = {}

                match_data = data_grouped_by_key.get(item[0])
                url = match_data["url"]
                result[url] = {"data": match_data, "score": item[1]}

        return result

    def _collection_nested_by(self, key) -> dict:
        data = {}

        for c in self.collection:
            key_data = c[key]
            data[key_data] = c

        return data


if __name__ == "__main__":

    class TestModel(Model):
        @property
        def summary_count(self):
            return len(self.collection)


if __name__ == "__main__":
    import json
    import signal
    import argparse

    progname = "gfzs.model"
    properties = {"progname": progname, "severity": 0, "log_path": "./tmp/gfzs.log"}
    logger.init_properties(**properties)
    logger.debug("start %s" % progname)

    def handle_sigint(signum, frame):
        logger.debug("detect SIGINT (Ctrl-c)")
        logger.debug("exit 0")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)

    json_str = open("fixtures/rust.json", "r").read()
    data = json.loads(json_str)

    args = argparse.Namespace(score=30)
    runtime_opts.init(args)

    model = TestModel(data)

    result = model.find("Amazon")
    logger.debug(
        "Search (query=Amazon, score=%d):  %d / %d"
        % (runtime_opts.score, model.data_size, model.summary_count)
    )
    print(
        "Search (query=Amazon, score=%d):  %d / %d"
        % (runtime_opts.score, model.data_size, model.summary_count)
    )
    for i in range(len(result)):
        print(result[i]["title"])

    result = model.find("\0")
    logger.debug(
        "Search (query=\0, score=%d):  %d / %d"
        % (runtime_opts.score, model.data_size, model.summary_count)
    )
    print(
        "Search (query=\0, score=%d):  %d / %d"
        % (runtime_opts.score, model.data_size, model.summary_count)
    )
    for i in range(len(result)):
        print(result[i]["title"])

    result = model.find("a")
    logger.debug(
        "Search (query=\0, score=%d):  %d / %d"
        % (runtime_opts.score, model.data_size, model.summary_count)
    )
    print(
        "Search (query=\0, score=%d):  %d / %d"
        % (runtime_opts.score, model.data_size, model.summary_count)
    )
    for i in range(len(result)):
        print(result[i]["title"])

    logger.debug("end %s" % progname, new_line=True)

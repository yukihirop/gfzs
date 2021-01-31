import os
import sys

try:
    # need when 「python3 gfzs/views/footer.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        from utils.color import Color
        from runtime.config import RuntimeConfig
        import utils.logger as logger

        if os.environ.get("DEBUG"):
            import utils.debug as debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.utils.color import Color
        from gfzs.runtime.config import RuntimeConfig
        import gfzs.utils.logger as logger

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from utils.color import Color
    from runtime.config import RuntimeConfig
    import utils.logger as logger

    if os.environ.get("DEBUG"):
        import utils.debug as debug


class Base(object):
    def __init__(self, stdscr, model, view_name):
        logger.debug("[%s] init" % view_name.capitalize())
        self.stdscr = stdscr
        self.parent_height, self.parent_width = stdscr.getmaxyx()
        self.model = model
        self.runtime_config = RuntimeConfig.get_instance()
        self.color = Color.get_instance()
        self.color_data = self.runtime_config.data["view"][view_name]["color"]
        self.colors = self._create_colors(self.runtime_config, self.color_data)

    def _create_colors(self, runtime_config, color_data) -> dict:
        result = {}
        for view_name in color_data:
            result[view_name] = self.color.use(color_data[view_name])

        return result

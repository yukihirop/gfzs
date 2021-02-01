import os
import sys

try:
    # need when 「python3 gfzs/views/footer.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        import utils.color as color
        import runtime.config as runtime_config
        import utils.logger as logger

        if os.environ.get("DEBUG"):
            import utils.debug as debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        import gfzs.utils.color as color
        import gfzs.runtime.config as runtime_config
        import gfzs.utils.logger as logger

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    import utils.color as color
    import runtime.config as runtime_config
    import utils.logger as logger

    if os.environ.get("DEBUG"):
        import utils.debug as debug


class Base(object):
    def __init__(self, stdscr, model, view_name):
        logger.debug("[%s] init" % view_name.capitalize())
        self.stdscr = stdscr
        self.parent_height, self.parent_width = stdscr.getmaxyx()
        self.model = model
        self.color = color
        self.color_data = runtime_config.data["view"][view_name]["color"]
        self.colors = self._create_colors(self.color_data)

    def _create_colors(self, color_data) -> dict:
        result = {}
        for view_name in color_data:
            result[view_name] = self.color.use(color_data[view_name])

        return result

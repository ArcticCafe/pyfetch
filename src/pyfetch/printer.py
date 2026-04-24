from dis import show_code

import rich
from rich.align import Align

from pyfetch.info_collector import InfoCollector


class Printer:
    def __init__(self):
        self.console = rich.get_console()

    def print(self, info_dict):
        for key, dicts in info_dict.items():
            self.console.rule(
                key,
            )
            for sub_key, sub_value in dicts.items():
                self.console.print(Align.right(f"{sub_key}: {sub_value}"))


if __name__ == "__main__":
    printer = Printer()
    collector = InfoCollector()
    printer.print(collector.get_info_dict())

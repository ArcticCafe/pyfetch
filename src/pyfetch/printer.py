import rich

from pyfetch.info_collector import InfoCollector


class Printer:
    def __init__(self): ...

    def print(self, info_dict):
        for key, value in info_dict.items():
            print(key)
            print(value)


if __name__ == "__main__":
    printer = Printer()
    collector = InfoCollector()
    printer.print(collector.get_info_dict())

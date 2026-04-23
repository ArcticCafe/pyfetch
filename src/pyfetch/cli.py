from pyfetch.info_collector import InfoCollector


def main():
    collector = InfoCollector()
    print(collector.os_info)
    print(collector.cpu_info)
    print(collector.memory_info)

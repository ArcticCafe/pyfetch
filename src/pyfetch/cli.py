from pyfetch.info_collector import InfoCollector


def main():
    collector = InfoCollector()
    print(collector.os_release)
    print(collector.cpu_info)

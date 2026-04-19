import os
import platform


class InfoCollector:
    def __init__(self): ...

    def _get_os_release(self):
        os_info = platform.freedesktop_os_release()
        return os_info.get("PRETTY_NAME", "Unknown OS")

    def _get_cpu_info(self):
        cpu_info = platform.machine()
        return cpu_info

    @property
    def os_release(self):
        return self._get_os_release()

    @property
    def cpu_info(self):
        return self._get_cpu_info()

import platform


class InfoCollector:
    def __init__(self): ...

    def _get_os_release(self):
        os_info = platform.freedesktop_os_release()
        return os_info.get("PRETTY_NAME", "Unknown OS")

    @property
    def os_release(self):
        return self._get_os_release()

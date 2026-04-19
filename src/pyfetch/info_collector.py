import platform

from pydantic import BaseModel


class CPUInfo(BaseModel):
    model_name: str
    cores: int
    cpu_freq: float
    raw_data: dict[str, str]


class OSInfo(BaseModel):
    distro_name: str
    kernel_version: str
    architecture: str
    system: str
    server_name: str


def _get_os_info_object() -> OSInfo:
    return OSInfo(
        distro_name=platform.freedesktop_os_release().get("PRETTY_NAME", "Unknown OS"),
        kernel_version=platform.release(),
        architecture=platform.machine(),
        system=platform.system(),
        server_name=platform.node(),
    )


def _get_first_core_raw_data() -> dict:
    """Parses /proc/cpuinfo and return a dictionary of the first core's raw data."""
    current_core = {}
    with open("/proc/cpuinfo", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                if current_core:
                    return current_core
            key, value = line.split(":", 1)
            current_core[key.strip()] = value.strip()
    return current_core if current_core else {}


class InfoCollector:
    def __init__(self):
        self.os_info = _get_os_info_object()

    def _get_os_release(self):
        return self.os_info.distro_name

    def _get_cpu_info(self):
        cpu_info = platform.machine()
        return cpu_info

    @property
    def os_release(self):
        return self._get_os_release()

    @property
    def cpu_info(self):
        return self._get_cpu_info()


if __name__ == "__main__":
    collector = InfoCollector()
    print(collector.os_release)
    print(collector.cpu_info)

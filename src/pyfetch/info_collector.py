import platform

import psutil
from pydantic import BaseModel

from pyfetch.collectors import linux, macos


class CPUInfo(BaseModel):
    model_name: str
    cores: int
    cpu_freq: float
    threads: int


class OSInfo(BaseModel):
    distro_name: str
    kernel_version: str
    architecture: str
    system: str
    server_name: str
    user_name: str


class MemoryInfo(BaseModel):
    total: int
    free: int
    memory_usage: float


def _get_memory_raw_data() -> dict:
    """Returns a dictionary of the system's memory usage. The data is in bytes."""
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "free": mem.free,
        "memory_usage": mem.percent,
    }


def _select_backend():
    system = platform.system()
    if system == "Linux":
        return linux
    if system == "Darwin":
        return macos
    raise RuntimeError(f"Unsupported platform: {system}")


class InfoCollector:
    def __init__(self):
        backend = _select_backend()
        self.system = platform.system()
        self.os_info = OSInfo(**backend.get_os_raw())
        self.cpu_info = CPUInfo(**backend.get_cpu_raw())
        self.memory_info = MemoryInfo(**_get_memory_raw_data())

    def get_info_dict(self) -> dict:
        return {
            "os_info": self.os_info.model_dump(),
            "cpu_info": self.cpu_info.model_dump(),
            "memory_info": self.memory_info.model_dump(),
        }


if __name__ == "__main__":
    collector = InfoCollector()
    print(collector.get_info_dict())

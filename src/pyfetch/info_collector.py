import getpass
import platform

import psutil
from pydantic import BaseModel, Field


class CPUInfo(BaseModel):
    model_name: str = Field(alias="model name")
    cores: int = Field(alias="cpu cores")
    cpu_freq: float = Field(alias="cpu MHz")
    threads: int = Field(alias="siblings")


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


def _get_os_info_object() -> OSInfo:
    return OSInfo(
        distro_name=platform.freedesktop_os_release().get("PRETTY_NAME", "Unknown OS"),
        kernel_version=platform.release(),
        architecture=platform.machine(),
        system=platform.system(),
        server_name=platform.node(),
        user_name=getpass.getuser(),
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


def _get_cpu_info_object() -> CPUInfo:
    cpu_raw_data = _get_first_core_raw_data()
    return CPUInfo(**cpu_raw_data)


def _get_memory_raw_data() -> dict:
    """Returns a dictionary of the system's memory usage. The data is in bytes."""
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "free": mem.free,
        "memory_usage": mem.percent,
    }


def _get_memory_info_object() -> MemoryInfo:
    memory_raw_data = _get_memory_raw_data()
    return MemoryInfo(**memory_raw_data)


class InfoCollector:
    def __init__(self):
        self.os_info = _get_os_info_object()
        self.cpu_info = _get_cpu_info_object()
        self.memory_info = _get_memory_info_object()

    def get_info_dict(self) -> dict:
        return {
            "os_info": self.os_info.model_dump(),
            "cpu_info": self.cpu_info.model_dump(),
            "memory_info": self.memory_info.model_dump(),
        }


if __name__ == "__main__":
    collector = InfoCollector()
    print(collector.get_info_dict())

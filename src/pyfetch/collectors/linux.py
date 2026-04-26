import getpass
import platform


def _get_first_core_raw_data() -> dict:
    """Parses /proc/cpuinfo and returns a dictionary of the first core's raw data."""
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


def get_os_raw() -> dict:
    return {
        "distro_name": platform.freedesktop_os_release().get("PRETTY_NAME", "Unknown OS"),
        "kernel_version": platform.release(),
        "architecture": platform.machine(),
        "system": platform.system(),
        "server_name": platform.node(),
        "user_name": getpass.getuser(),
    }


def get_cpu_raw() -> dict:
    raw = _get_first_core_raw_data()
    return {
        "model_name": raw.get("model name", "Unknown"),
        "cores": int(raw.get("cpu cores", 0)),
        "cpu_freq": float(raw.get("cpu MHz", 0.0)),
        "threads": int(raw.get("siblings", 0)),
    }

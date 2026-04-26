import getpass
import platform
import plistlib
import struct
import subprocess


def _sysctl(key: str) -> str:
    return subprocess.check_output(["sysctl", "-n", key], text=True).strip()


def _walk_dicts(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk_dicts(v)
    elif isinstance(node, list):
        for item in node:
            yield from _walk_dicts(item)


def _max_freq_hz_from_dvfs() -> int:
    """Reads CPU DVFS tables from IORegistry (pmgr).

    The kernel publishes per-cluster (P/E) voltage-frequency tables under
    keys named like `voltage-states5-sram` (P-cluster) and
    `voltage-states1-sram` (E-cluster). Each value is a packed sequence of
    little-endian (freq_hz: u32, voltage_uv: u32) pairs. We return the max
    frequency seen across all such tables — that's the boost frequency of
    the highest-performance cluster.
    """
    output = subprocess.check_output(
        ["ioreg", "-arc", "AppleARMIODevice", "-n", "pmgr"]
    )
    plist = plistlib.loads(output)
    max_freq = 0
    for node in _walk_dicts(plist):
        for key, value in node.items():
            if not (key.startswith("voltage-states") and key.endswith("-sram")):
                continue
            if not isinstance(value, bytes):
                continue
            for offset in range(0, len(value) - 7, 8):
                freq, _voltage = struct.unpack_from("<II", value, offset)
                if freq > max_freq:
                    max_freq = freq
    return max_freq


def _get_cpu_freq_mhz() -> float:
    try:
        return int(_sysctl("hw.cpufrequency_max")) / 1_000_000
    except (subprocess.CalledProcessError, ValueError):
        pass
    try:
        return _max_freq_hz_from_dvfs() / 1_000_000
    except (subprocess.CalledProcessError, plistlib.InvalidFileException, struct.error):
        return 0.0


def get_os_raw() -> dict:
    mac_ver = platform.mac_ver()[0]
    return {
        "distro_name": f"macOS {mac_ver}" if mac_ver else "macOS",
        "kernel_version": platform.release(),
        "architecture": platform.machine(),
        "system": platform.system(),
        "server_name": platform.node(),
        "user_name": getpass.getuser(),
    }


def get_cpu_raw() -> dict:
    return {
        "model_name": _sysctl("machdep.cpu.brand_string"),
        "cores": int(_sysctl("hw.physicalcpu")),
        "cpu_freq": _get_cpu_freq_mhz(),
        "threads": int(_sysctl("hw.logicalcpu")),
    }

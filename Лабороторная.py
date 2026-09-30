import platform
import os
import sys
import socket
import getpass
import shutil
import json
from pathlib import Path
from datetime import datetime


def detect_os():
    system = platform.system()

    if system == "Darwin":
        return "macOS"

    return system


def collect_system_info():
    return {
        "os": {
            "name": detect_os(),
            "release": platform.release(),
            "version": platform.version()
        },
        "hostname": socket.gethostname(),
        "architecture": platform.machine()
    }


def collect_hardware_info():
    return {
        "processor": platform.processor() or None,
        "logical_cpu_count": os.cpu_count()
    }


def collect_python_info():
    return {
        "version": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": sys.platform,
        "executable": sys.executable
    }


def collect_user_info():
    return {
        "username": getpass.getuser(),
        "working_directory": str(Path.cwd())
    }


def collect_storage_info():
    disk = shutil.disk_usage(Path.cwd())

    return {
        "total_bytes": disk.total,
        "used_bytes": disk.used,
        "free_bytes": disk.free
    }


def main():
    data = {
        "metadata": {
            "collected_at": datetime.now().astimezone().isoformat()
        },
        "system": collect_system_info(),
        "hardware": collect_hardware_info(),
        "python": collect_python_info(),
        "user": collect_user_info(),
        "storage": collect_storage_info()
    }

    with open("system_info.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("Информация успешно собрана.")
    print("Результат сохранён в:")
    print(Path("system_info.json").resolve())
    os.startfile("system_info.json")


if __name__ == "__main__":
    main()
import platform
import sys
from typing import Optional
from enum import Enum

class OSType(Enum):
    Unknown = 0
    Windows = 1
    Linux = 2
    Darwin = 3

class OSArch(Enum):
    Unknown = 0
    X86 = 1
    X64 = 2
    Arm64 = 3


arch: Optional[str] = None
system: Optional[OSType] = None

def get_system_name():
    match sys.platform:
        case "win32":
            system = OSType.Windows
        case "darwin":
            system = OSType.Darwin
        case "linux":
            system = OSType.Linux
        case _:
            system = OSType.Unknown

def get_system_arch():
    match platform.machine().lower():
        case "i386" | "i686" | "32bits":
            arch = OSArch.X86
        case "x86_64" | "amd64" | "64bits":
            arch = OSArch.X64
        case "aarch64" | "arm64":
            arch = OSArch.Arm64
        case _:
            arch = OSArch.Unknown

get_system_arch()

get_system_name()
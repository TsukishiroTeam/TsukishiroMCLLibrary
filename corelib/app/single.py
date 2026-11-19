import ctypes
import tempfile
from pathlib import Path

mutex = None

file_lock_handle = None

ERR_ALREAD_EXIST = 183

def get_lock() -> bool:
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Local/TsukishiroMC")
    if ctypes.get_last_error() == ERR_ALREAD_EXIST:
        ctypes.windll.kernel32.CloseHandle(mutex)
        return False
    return True
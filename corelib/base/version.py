from typing import Optional, Iterable
from functools import total_ordering

@total_ordering
class Version:
    major: int
    minor: Optional[int] = None
    patch: Optional[int] = None
    build: Optional[int] = None

    def __init__(self, ver: str | Iterable[int]):
        if isinstance(ver, str):
            self.__init__version_str__(ver)
        else:
            self.__init__version_numbers__(ver)

    def __init__version_str__(self, ver: str):
        if ".." in ver or ver.endswith(".") or ver.startswith("."):
            raise VersionException("无效的版本字符串")
        versions = ver.split(".")
        if len(versions) == 1 and not versions[0]:
            raise VersionException("无效的版本字符串")
        match len(versions):
            case 1:
                self.major = int(versions[0])
            case 2:
                self.major = int(versions[0])
                self.minor = int(versions[1])
            case 3:
                self.major = int(versions[0])
                self.minor = int(versions[1])
                self.patch = int(versions[2])
            case 4:
                self.major = int(versions[0])
                self.minor = int(versions[1])
                self.patch = int(versions[2])
                self.build = int(versions[3])
            case _:
                raise VersionException(f"版本字符串过长: {".".join(versions)}")
            
    def __init__version_numbers__(self, ver: Iterable[int]):
        return self.__init__version_str__(".".join(str(v) for v in ver))
    
    def _cast_to_tuple(self) -> tuple[int,int,int,int]:
        return (
            self.major,
            self.minor or 0,
            self.patch or 0,
            self.build or 0
        )

    def __eq__(self, value):
        if not isinstance(value, Version):
            return NotImplemented
        return self._cast_to_tuple() == value._cast_to_tuple()
    
    def __lt__(self, value):
        if not isinstance(value, Version):
            return NotImplemented
        return self._cast_to_tuple() < value._cast_to_tuple()

    def is_default(self):
        ver = self._cast_to_tuple()
        return ver != (0,0,0,0) and ver != (999,999,999,999)
    
class VersionException(Exception):
    pass
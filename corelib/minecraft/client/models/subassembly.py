from enum import Enum

class SubAssembly:
    assembly_type: SubAssemblyType

class SubAssemblyType(Enum):
    Game = 1
    ModLoader = 2
    ShaderLoader = 3
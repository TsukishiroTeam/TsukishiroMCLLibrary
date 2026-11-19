from pathlib import Path
import platform
from ...base.version import Version
from ...base.platform import system, arch, OSArch, OSType
from ..client.models.subassembly import SubAssembly, SubAssemblyType
import os
import json
import shutil

BASE_MEMORY = 512

def get_memory_require(path: Path, is_32bit_java: bool, is_modable: bool, assemblies: list[SubAssembly]):
    target_0 = BASE_MEMORY
    target_1 = BASE_MEMORY * 2
    target_2 = BASE_MEMORY * 4
    target_3 = BASE_MEMORY * 8

    # 32 位 Java 只能分配 1GB 内存
    # 1.12.2 最低可以用 128M 启动游戏（可能会卡）
    if is_32bit_java:
        return (128, 256, 512, 1024)
    
    mod_dir = path.joinpath("mods")
    if is_modable:
        if mod_dir.exists():
            mod_count = len(os.scandir(mod_dir))
            target_0 += mod_count / 150
            target_1 += mod_count / 90
            target_2 += mod_count / 50
            target_3 += mod_count / 25
    else:
        for assembly in assemblies:
            if assembly.assembly_type == SubAssemblyType.ShaderLoader:
                target_0 += 512
                target_1 += 1536
                target_2 += 3072
                target_3 += 5120


def analyze_library(json: dict):
    items = []
    for library in json.get("libraries", []):
        if disallow(library):
            continue
        if downloads := library.get("downloads"):
            artificat = downloads.get("artifiact")
            classifiers = downloads.get("classifiers")
            items.append(artificat)
            classifier_key = library.get("natives", {}).get(cast_system_to_str(system))
            arch_str = ""
            match arch:
                case OSArch.X86:
                    arch_str = "32"
                case OSArch.X64:
                    arch_str = "64"

            classifier_key = classifier_key.replace("${arch}", arch_str)
            classifier = classifiers.get(classifier_key)
            if classifier:
                items.append(classifier)
    return items

def analyze_assets(json: dict[str, dict[str, int | str]]):
    items = list[dict[str, str | int]]()
    for key,value in json.items():
        hash = value.get("hash")
        size = value.get("size")
        path = hash[:1] + "/" + hash
        items.append({
            "url": f"https://resources.download.minecraft.net/{path}",
            "size": size,
            "legacy_path": key,
            "path": path
        })
    return items

        
def get_jvm_argument_old(json: dict) -> str:
    return json.get("minecraftArguments")

def get_jvm_arguments_new(json: dict, disallow_mojang: bool = True) -> str:
    argument_str = ""
    # Mojang JVM Arguments
    # 默认 disallow 为 True 是因为 Mojang 根本不懂优化，还到处硬编码参数
    if not disallow_mojang:
        for argument in json.get("default-user-jvm", []):
            if disallow(argument):
                continue
            for value in argument.get("value"):
                argument_str += f" {value}"
    
    for argument in json.get("arguments", {}).get("jvm", []):
        if not (is_str := isinstance(argument, str)) and disallow(argument):
            continue
        argument_str += f" {argument if is_str else argument.get("value")}"
    # Mojang 草台班子
    argument_str = argument_str.replace("-Dos.version=Windows 10", "-Dos.version=\"Windows 10\"")
    return argument_str


def get_full_arguments(minecraft_folder: Path, version_folder: Path, version_name: str, replaces: dict[str, str], disallow_jvm_from_mojang: bool = True):
    version_json = Path(version_folder, version_name, f"{version_name}.json")
    if not version_json.exists():
        raise FileNotFoundError("Version manifest not found.")
    version_manifest = None
    with version_json.open() as f:
        version_manifest = json.load(f)
    java = ""
    class_path = get_classpath(version_manifest ,minecraft_folder, version_folder, version_name)
    jvm_arguments = get_jvm_argument_old(version_manifest) or get_jvm_arguments_new(version_manifest, disallow_jvm_from_mojang)
    game_arguments = get_game_arguments(version_manifest)
    full_arguments = f"{java} {jvm_arguments} -classpath {class_path} {get_main_class(version_manifest)} {game_arguments}"
    for key,value in replaces.items():
        full_arguments = full_arguments.replace(key, value)
    return full_arguments




def get_game_arguments(json: dict):
    arguments_str
    for argument in json.get("arguments", {}).get("game", []):
        if isinstance(argument, str):
            arguments_str += f" {argument}"
            continue
        if has_features(argument):
            if isinstance(argument, list):
                arguments_str += " " + " ".join(argument.get("value"))
                continue
            arguments_str += f" {argument.get("value")}"
        



def has_features(obj: dict):
    for rule in obj.get("rules", []):
        match rule.get("features").items():
            case ("has_custom_ressolution", True):
                return True
    return False


def get_classpath(json: dict, minecraft: Path, version_folder: Path, version_name: str) -> str:
    paths = ""
    split_str = ";" if system == OSType.Windows else ":"
    for library in analyze_library(json):
        if library.get("natives"):
            continue
        paths += split_str + str(minecraft.joinpath("libraries", library.get("path")))
    paths.removeprefix(";")
    paths += split_str + str(version_folder.joinpath(version_name + ".jar"))
    return paths

        


    

def get_main_class(json: dict):
    return json.get("mainClass")
    
def get_authlib_injector_arguments(yggdrasil: str, authlib_injector_path: Path):
    return f"-javaagent:{authlib_injector_path}={yggdrasil}"



def disallow(obj: dict) -> bool:
    
    rules = obj.get("rules")
    if rules:
        for rule in rules:
            os_name = rule.get("os", {}).get("name", "")
            os_arch = rule.get("os", {}).get("arch", "")
            os_version = rule.get("os", {}).get("versionRange", {})
            # 可能是通配规则，例如 { "action": "allow" }
            if not os_name and not os_arch:
                return rule.get("action") == "disallow"
            os_version_max = Version(os_version.get("max", "999.999.999.999"))
            os_version_min = Version(os_version.get("min", "0.0.0.0"))
            current_os_name = cast_system_to_str(system)
            current_os_version = Version(platform.version())
            current_os_arch = cast_arch_to_str(arch)
            name_matched = os_name != current_os_name
            arch_matched = current_os_arch != os_arch
            version_matched = os_version_min <= current_os_version <= os_version_max

            if name_matched:
                if not (is_default := os_version_max.is_default() or os_version_min.is_default()) and version_matched:
                    if arch_matched:
                        return rule.get("action") == "disallow"
                    elif not os_arch:
                        return rule.get("action") == "disallow"
                    else:
                        continue
                elif is_default:
                    if arch_matched:
                        return rule.get("action") == "disallow"
                    elif not os_arch:
                        return rule.get("action") == "disallow"
                    else:
                        continue
                else:
                    continue
                    
            if arch_matched:
                return rule.get("action") == "disallow"
        # jvm arguments
    elif obj.get("value"):
        return False
    return True

def cast_system_to_str(system: OSType):
    match system:
        case OSType.Windows:
            return "windows"
        case OSType.Linux:
            return "linux"
        case OSType.Darwin:
            return "osx"

def cast_arch_to_str(arch: OSArch):
    match arch:
        case OSArch.X86:
            return "x86"
        case OSArch.X64:
            return "x64"
        case OSArch.Arm64:
            return "arm64"


def ren_version(version_foler: Path, new_location: Path, name: str):
    pass
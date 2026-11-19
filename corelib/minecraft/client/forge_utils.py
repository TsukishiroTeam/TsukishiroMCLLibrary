from pathlib import Path

def handle_forge_install():
    pass

def _forge_install_v1():
    pass

def _forge_install_v2():
    pass

def _forge_install_v3(profile: dict, output_dir: Path, base_libraries_path: Path):
    for processor in profile.get("processors"):
        is_client = False
        for side in processor.get("sides"):
            if side != "client":
                continue
            is_client = True
        if not is_client:
            continue
        

def _forge_install_v4():
    pass


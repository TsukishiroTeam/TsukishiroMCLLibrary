from typing import Optional
from ..instance_utils import analyze_library as analyze

def analyze_library(json: dict, requires: Optional[dict[str, dict]] = None):
    items = []
    for require in json.get("requires", []):
        items.append(analyze_library(requires.get(require.get("uid"))))
    items.extend(analyze(json))


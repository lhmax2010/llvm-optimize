"""Check the new clang RPM against the retained B1 provider."""
from pathlib import PurePosixPath
import re

MODULES = ("/usr/lib/libscanbuild", "/usr/lib/libear")
PYTHON = re.compile(r"python|pythondist", re.IGNORECASE)
CACHE_NAME = re.compile(r"(.+?)\.[^.]+(?:\.opt-\d+)?\.pyc")


def dependency_diff(before, after):
    added = sorted(set(after.splitlines()) - set(before.splitlines()))
    return {"added": added, "added_python": [line for line in added if PYTHON.search(line)]}


def module_files(paths):
    return {path for path in paths if any(path == root or path.startswith(root + "/") for root in MODULES)}


def bytecode_audit(paths):
    files = module_files(paths)
    sources = {path for path in files if path.endswith(".py")}
    caches = {path for path in files if "__pycache__" in PurePosixPath(path).parts}
    bytecode = {path for path in files if path.endswith(".pyc")}
    owners = {}
    for path in sorted(bytecode):
        item = PurePosixPath(path)
        if item.parent.name == "__pycache__":
            match = CACHE_NAME.fullmatch(item.name)
            source = str(item.parent.parent / (match[1] + ".py")) if match else None
        else:
            source = str(item.with_suffix(".py"))
        owners[path] = source if source in sources else None
    cache_dirs = {str(PurePosixPath(path).parent) for path in bytecode if PurePosixPath(path).parent.name == "__pycache__"}
    orphan = sorted({path for path, source in owners.items() if source is None} | (caches - bytecode - cache_dirs))
    coverage = sorted(sources - set(owners.values())) if bytecode else []
    status = "FAIL" if orphan or coverage else "PASS"
    return {"status": status, "bytecode": "PRESENT" if bytecode else "ABSENT",
            "files": sorted(files), "sources": sorted(sources), "orphans": orphan,
            "missing_bytecode": coverage, "covered_bytecode_paths": sorted(bytecode | (cache_dirs & files))}

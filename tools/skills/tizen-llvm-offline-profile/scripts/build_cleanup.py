"""Remove a project build tree after a read-only filesystem boundary check."""
import argparse
from contextlib import ExitStack
import os
from pathlib import Path
import stat

FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW


def mount_points():
    """Return the visible mount paths, including same-device bind mounts."""
    import re

    try:
        lines = Path("/proc/self/mountinfo").read_text().splitlines()
    except FileNotFoundError:
        return set()
    return {
        Path(re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), line.split()[4]))
        for line in lines
    }


def visit(fd, path, device, mounts, delete):
    if path in mounts or os.fstat(fd).st_dev != device:
        raise ValueError(f"mount or different st_dev under build tree: {path}")
    for name in os.listdir(fd):
        child = path / name
        info = os.stat(name, dir_fd=fd, follow_symlinks=False)
        if info.st_dev != device or child in mounts:
            raise ValueError(f"mount or different st_dev under build tree: {child}")
        if stat.S_ISDIR(info.st_mode):
            nested = os.open(name, FLAGS, dir_fd=fd)
            try:
                if not os.path.samestat(info, os.fstat(nested)):
                    raise ValueError(f"build directory changed during cleanup: {child}")
                visit(nested, child, device, mounts, delete)
                if delete:
                    os.rmdir(name, dir_fd=fd)
            finally:
                os.close(nested)
        elif delete:
            os.unlink(name, dir_fd=fd)


def remove_tree(project_root, target):
    root, tree = Path(project_root), Path(target)
    for path in (root, tree):
        if not path.is_absolute() or path.resolve(strict=True) != path:
            raise ValueError(f"expected a canonical, symlink-free directory: {path}")
    if root == Path("/") or root == tree or not tree.is_relative_to(root):
        raise ValueError(f"build tree is outside the designated project directory: {tree}")
    with ExitStack() as stack:
        parent = os.open(tree.anchor, FLAGS)
        stack.callback(os.close, parent)
        for part in tree.parent.parts[1:]:
            parent = os.open(part, FLAGS, dir_fd=parent)
            stack.callback(os.close, parent)
        fd = os.open(tree.name, FLAGS, dir_fd=parent)
        stack.callback(os.close, fd)
        device = os.fstat(parent).st_dev
        visit(fd, tree, device, mount_points(), delete=False)
        visit(fd, tree, device, mount_points(), delete=True)
        if not os.path.samestat(os.fstat(fd), os.stat(tree.name, dir_fd=parent, follow_symlinks=False)):
            raise ValueError(f"build tree changed during cleanup: {tree}")
        os.rmdir(tree.name, dir_fd=parent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root")
    parser.add_argument("target")
    args = parser.parse_args()
    try:
        remove_tree(args.project_root, args.target)
    except (OSError, ValueError) as error:
        parser.exit(1, f"STOP: {error}\n")

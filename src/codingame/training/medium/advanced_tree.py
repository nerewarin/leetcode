"""
https://www.codingame.com/training/medium/advanced-tree
"""

from __future__ import annotations  # for compatibility with Python 3.11 used in autograder

import sys
from collections.abc import Callable
from typing import Any, TypedDict


def debug(msg):
    print(msg, file=sys.stderr, flush=True)


class DepthParserError(Exception):
    pass


def _depth_parser(raw_flag):
    try:
        return int(raw_flag.split(" ")[-1])
    except ValueError as exc:
        raise DepthParserError(f"for {raw_flag=}") from exc


class FlagSpec(TypedDict):
    arg_name: str
    # not used for calling; just documentation
    value_handler: Callable[[str], Any] | type


class Path:
    def __init__(
        self,
        name: str,
        parent: Path | None = None,
        children: list[Path] | None = None,
        is_last_child: bool | None = False,
    ):
        self.name = name
        self.parent = parent
        self.children = children or []
        self.is_last_child = is_last_child

    @property
    def sorting_key(self):
        name = self.name.lower()
        while name.startswith("."):
            name = name[1:]
        return name

    def __str__(self):
        revered_path = [self.name]
        path = self
        while path.parent:
            revered_path.append(path.parent.name)
            path = path.parent
        return "/".join(reversed(revered_path))

    @property
    def is_hidden(self):
        return self.name.startswith(".")

    @property
    def is_dir(self):
        return bool(self.children)

    @property
    def is_file(self):
        return not self.is_dir

    def get_or_add_child(self, child: Path):
        for existing in self.children:
            if existing.name == child.name:
                return existing

        self.children.append(child)
        return child

    def get_children(self, display_hidden: bool | None = False, directories_only: bool | None = False) -> list[Path]:
        children = []
        for child in self.children:
            if child.is_hidden and not display_hidden:
                continue

            if child.is_file and directories_only:
                continue

            children.append(child)

        res = sorted(children, key=lambda child: child.sorting_key)
        for i, r in enumerate(res):
            if i != len(res) - 1:
                r.is_last_child = False
            else:
                r.is_last_child = True

        return res

    def __truediv__(self, other: str):
        """Implements `self / other`."""
        return type(self)(other, self)

    def __rtruediv__(self, other: Path):
        """Implements `other / self` (optional, for reversed operands)."""
        return type(self)(self.name, other)


class Tree:
    _valid_flags: dict[str, FlagSpec] = {
        "-a": {"arg_name": "display_hidden", "value_handler": lambda x: True},
        "-d": {"arg_name": "directories_only", "value_handler": lambda x: True},
        "-L": {"arg_name": "depth", "value_handler": _depth_parser},
    }

    def __init__(
        self,
        root: Path,
        display_hidden: bool | None = False,
        directories_only: bool | None = False,
        depth: int | None = None,
        invalid_root: bool | None = False,
    ):
        self._root = root
        self._display_hidden = display_hidden  # -a : Display hidden directories and files.
        self._directories_only = directories_only  # -d: Only display directories (modifies the report line, see below).
        self._depth = depth  # -L depth: Limit the "depth" of the tree.

        self._summary_is_ready = False  # cache flag
        self._directories = 0
        self._files = 0

        self.invalid_root = invalid_root

    def _clear_cache(self):
        self._summary_is_ready = False  # cache flag
        self._directories = 0
        self._files = 0

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value: Path):
        self._root = value
        self._clear_cache()

    @property
    def display_hidden(self):
        return self._display_hidden

    @display_hidden.setter
    def display_hidden(self, value: bool):
        self._display_hidden = value
        self._clear_cache()

    @property
    def directories_only(self):
        return self._directories_only

    @directories_only.setter
    def directories_only(self, value: bool):
        self._directories_only = value
        self._clear_cache()

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value: int):
        self._depth = value
        self._clear_cache()

    @staticmethod
    def _format_tree_element(path: Path, level: int, is_last_child: bool) -> str:
        string = ""
        for current_level in range(level):
            parent = path
            for i in range(level - current_level - 1):
                if parent.parent is None:
                    raise ValueError(f"there must be parent for {parent}!")
                parent = parent.parent
            parent_is_last_child = parent.is_last_child

            if current_level == level - 1:
                if is_last_child:
                    string += "`-- "
                else:
                    string += "|-- "
            else:
                if parent_is_last_child:
                    string += "    "
                else:
                    string += "|   "

        return string + path.name

    def as_string(self):
        self._clear_cache()

        def dfs(path: Path, level: int, is_last_child: bool):
            line = self._format_tree_element(path, level, is_last_child)

            if level == 0:
                pass
            elif path.is_dir:
                self._directories += 1
            elif path.is_file:
                self._files += 1
            else:
                raise ValueError(f"both is_dir and is_file are False for {path}")

            if self.depth and level >= self.depth:
                return line

            children = path.get_children(self.display_hidden, self.directories_only)
            first_children, last_child = children[:-1], children[-1:]

            for child in first_children:
                line += "\n" + dfs(child, level + 1, False)
            for child in last_child:
                line += "\n" + dfs(child, level + 1, True)

            return line

        res = dfs(path=self.root, level=0, is_last_child=False)
        if not self.invalid_root or not self.root.children:
            res += " [error opening dir]"

        self._summary_is_ready = True
        return res

    def build(self, text: list[str]):
        root_exists = False
        for line in text:
            if self.root.name == ".":
                pass
            else:
                this = "./"
                if line.startswith(this) and not self.root.name.startswith(this):
                    line = line[len(this) :]

                if not line.startswith(self.root.name):
                    continue

            root_exists = True

            # +1 to cut "/" too
            path_relative_to_root = line[len(self.root.name) + 1 :]
            if not path_relative_to_root:
                continue

            parts = path_relative_to_root.split("/")

            path = self.root
            for part in parts:
                new_path = path / part
                new_path = path.get_or_add_child(new_path)
                path = new_path

        self.invalid_root = root_exists

    def filter(self, f: str):
        """
        - -a : Display hidden directories and files.
        - -d: Only display directories (modifies the report line, see below).
        - -L depth: Limit the "depth" of the tree.
        Args:
            f: str e.g. '-L -2,-e,-a'

        Returns:

        """
        flags = self._parse_flags(f)

        return type(self)(self.root, invalid_root=self.invalid_root, **flags)

    def _parse_flags(self, f: str) -> dict[Any, Any]:
        raw_flags = f.split(",")
        flags = {}
        for raw_flag in raw_flags:
            raw_flag = raw_flag.strip()
            for key, value in self._valid_flags.items():
                if raw_flag.startswith(key):
                    try:
                        flags[value["arg_name"]] = value["value_handler"](raw_flag)
                    except DepthParserError:
                        continue
                    break
        return flags

    def get_summary(self):
        if not self._summary_is_ready:
            self.as_string()
        if not self._summary_is_ready:
            raise RuntimeError("Summary is not ready yet.")

        directories = self._directories
        summary = str(directories)
        if directories == 1:
            summary += " directory"
        else:
            summary += " directories"

        if not self.directories_only:
            summary += f", {self._files} file"
            if self._files != 1:
                summary += "s"

        return summary


def main(s, f, n, lines):
    if len(lines) != n:
        raise ValueError("lines must have length equal to n")

    s = Path(s, is_last_child=True)
    tree = Tree(s)
    tree.build(lines)
    filtered_tree = tree.filter(f)

    res = filtered_tree.as_string() + "\n\n" + filtered_tree.get_summary()
    return res


if __name__ == "__main__":
    s = input()
    f = input()
    n = int(input())
    debug(f"{s=}")
    debug(f"{f=}")
    debug(f"{n=}")

    lines = []
    for i in range(n):
        line = input()
        debug(f"{line=}")
        lines.append(line)
    debug(f"{lines=}")

    print(main(s, f, n, lines))

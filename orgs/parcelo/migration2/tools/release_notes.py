"""Print the Unreleased section of CHANGELOG.md grouped by area."""
import re
import sys
from collections import defaultdict
from pathlib import Path

BULLET = re.compile(r"^- \[(?P<ticket>[A-Z]+-\d+)\] (?P<area>[a-z_]+): (?P<text>.+)$")


def unreleased(text):
    match = re.search(r"## Unreleased\n(.*?)(\n## |\Z)", text, re.S)
    return match.group(1) if match else ""


def main(path="CHANGELOG.md"):
    groups = defaultdict(list)
    for line in unreleased(Path(path).read_text()).splitlines():
        found = BULLET.match(line.strip())
        if found:
            groups[found["area"]].append(f"{found['text']} ({found['ticket']})")
    for area in sorted(groups):
        print(area)
        for item in groups[area]:
            print("  -", item)


if __name__ == "__main__":
    main(*sys.argv[1:])

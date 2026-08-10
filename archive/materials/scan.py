import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(ROOT, "project_dump.txt")

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "build",
    "dist",
    ".idea",
    ".vscode",
    "venv",
    ".venv"
}

IGNORE_FILES = {
    "project_dump.txt",
    "scan.py"
}


def scan_dir(path, level=0):
    lines = []

    for name in sorted(os.listdir(path)):
        if name in IGNORE_FILES:
            continue

        full_path = os.path.join(path, name)
        indent = "    " * level

        if os.path.isdir(full_path):
            if name in IGNORE_DIRS:
                continue

            lines.append(f"{indent}[DIR] {name}")
            lines.extend(scan_dir(full_path, level + 1))

        else:
            lines.append(f"{indent}[FILE] {name}")
            lines.append(f"{indent}----- content start -----")

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    for line in f:
                        lines.append(indent + line.rstrip())
            except:
                lines.append(indent + "<binary or unreadable file>")

            lines.append(f"{indent}----- content end -----\n")

    return lines


def main():
    output = []
    output.append(f"ROOT: {ROOT}\n")

    output.extend(scan_dir(ROOT))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
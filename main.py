import os
from pathlib import Path
import subprocess
import sys

def main(base: str, head: str):
    command = f"git --no-pager log --oneline {base}...{head}"
    result = subprocess.run(command.split(" "), stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8")
    feat = []
    fix = []
    chore = []
    other = []

    for line in result.split("\n"):
        if len(line) < 8:
            continue
        elif "feat:" in line:
            feat.append(line)
        elif "fix:" in line:
            fix.append(line)
        elif "chore:" in line:
            chore.append(line)
        else:
            other.append(line)

    output_lines = []

    if len(feat) > 0:
        output_lines.append("## Features 🔨")
        output_lines.extend(feat)
    if len(fix) > 0:
        output_lines.append("## Fixes 🐛")
        output_lines.extend(fix)
    if len(other) > 0:
        output_lines.append("## Other changes 📝")
        output_lines.extend(other)
    if len(chore) > 0:
        output_lines.append("## Chores 👷‍♂️")
        output_lines.extend(chore)

    output = "\n".join(output_lines) # newline character for gh actions output

    output_file = Path(os.environ.get("GITHUB_OUTPUT", "output.txt"))
    output_file.write_text(f"output={output}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
import os
from pathlib import Path
import re
import subprocess
import sys

COMMIT_HASH_LENGTH = 8

def run_command(command: str):
    result = subprocess.run(command.split(" "), stdout=subprocess.PIPE)

    if result.returncode != 0:
        raise Exception(f"Command failed: {command}")

    return result.stdout.decode("utf-8")

def is_semantic(prefix: str, line: str):
    """
    Check if line is a semantic commit message of the form:
    <commit hash> <prefix>(<scope>): <message>

    examples of input lines:
    
        12345678 feat(backend): add new feature
        12345678 feat: add new feature
    """
    return re.match(r"(.+)"+ prefix + r"(\(.+\))*\:.*", line) is not None

def main(base: str, head: str):
    run_command("git config --global --add safe.directory /github/workspace")
    result = run_command(f"git --no-pager log --oneline {base}...{head}")
    
    feat = []
    fix = []
    chore = []
    other = []

    for line in result.split("\n"):
        if len(line) < COMMIT_HASH_LENGTH:
            continue
        elif is_semantic("feat",line):
            feat.append(line)
        elif is_semantic("fix",line):
            fix.append(line)
        elif is_semantic("chore",line):
            feat.append(line)
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


    output = "\n".join(output_lines)

    # use '<br>' as delimiter for gh actions output
    # https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#multiline-strings
    output_file = Path(os.environ.get("GITHUB_OUTPUT", "output.txt"))
    output_file.write_text(f"changelog<<<br>\n{output}\n<br>")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
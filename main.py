import os
from pathlib import Path
import subprocess
import sys

COMMIT_HASH_LENGTH = 8

def run_command(command: str):
    result = subprocess.run(command.split(" "), stdout=subprocess.PIPE)

    if result.returncode != 0:
        raise Exception(f"Command failed: {command}")

    return result.stdout.decode("utf-8")

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


    output = "\n".join(output_lines)

    # use 'nl' as delimeiter for gh actions output
    # https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#multiline-strings
    output_file = Path(os.environ.get("GITHUB_OUTPUT", "output.txt"))
    output_file.write_text(f"changelog<<nl\n{output}\nnl")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
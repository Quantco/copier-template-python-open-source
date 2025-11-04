import os
from pathlib import Path

from scripts.common import get_latest_github_tag


def update_workflow_actions(file_path: Path):
    text = file_path.read_text()
    lines = text.splitlines(keepends=True)

    new_lines: list[str] = []

    for line in lines:
        if "uses: " not in line:
            new_lines.append(line)
        else:
            action_with_rest = line.split(":")[1].strip()
            action, current_sha_with_version = action_with_rest.split("@")
            action_repo = "/".join(action.split("/")[:2])
            current_sha, current_version = current_sha_with_version.split("#")
            current_sha = current_sha.strip()
            current_version = current_version.strip()
            new_version, new_sha = get_latest_github_tag(action_repo)
            print(f"{action}: {current_version} -> {new_version}")
            new_line = line.replace(current_sha, new_sha).replace(
                current_version, new_version
            )
            new_lines.append(new_line)

    file_path.write_text("".join(new_lines))


def update_project_workflows(path: str = "template/.github/workflows/"):
    for file in os.listdir(path):
        print(f"Updating `{file}`")
        update_workflow_actions(Path(path) / file)


if __name__ == "__main__":
    update_project_workflows()

import os
from pathlib import Path

import ruamel.yaml

from scripts.common import get_latest_github_tag


def get_latest_pin(action: str, current_version: str) -> str:
    latest_tag_name, latest_tag_sha = get_latest_github_tag(action)

    pin_by_major = current_version.startswith("v")

    if pin_by_major:
        major = latest_tag_name.split(".")[0]
        return major
    else:
        return latest_tag_sha


def update_workflow_actions(file_path: Path, dry_run: bool = False):
    yaml = ruamel.yaml.YAML(typ="jinja2")
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.width = 1000  # Prevent default wrapping

    with open(file_path) as f:
        workflow = yaml.load(f)

    for job in workflow.get("jobs", {}).values():
        for step in job.get("steps", []):
            if "uses" in step:
                action_ref = step["uses"]
                action, _, current_version = action_ref.partition("@")
                new_version = get_latest_pin(action, current_version)
                print(
                    f"{action}:"
                    f" current version: {current_version},"
                    f" latest version: {new_version}"
                )
                if new_version != current_version and not dry_run:
                    step["uses"] = f"{action}@{new_version}"

    with open(file_path, "w") as f:
        yaml.dump(workflow, f)


def update_project_workflows(
    path: str = "template/.github/workflows/", dry_run: bool = False
):
    for file in os.listdir(path):
        print(f"Updating {file}")
        update_workflow_actions(Path(path) / file, dry_run=dry_run)


if __name__ == "__main__":
    update_project_workflows()

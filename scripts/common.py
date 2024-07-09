import json
import subprocess


def get_latest_github_tag(repo_name: str) -> tuple[str, str]:
    output = subprocess.check_output(["gh", "api", f"repos/{repo_name}/tags"])

    latest_tag = json.loads(output)[0]
    return latest_tag["name"], latest_tag["commit"]["sha"]

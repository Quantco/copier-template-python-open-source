# Copyright (c) QuantCo 2024-2025
# SPDX-License-Identifier: LicenseRef-QuantCo

import json
import re
import subprocess

TAG_REGEX = r"^v\d+\.\d+\.\d+$"


def get_latest_github_tag(repo_name: str) -> tuple[str, str]:
    output = subprocess.check_output(["gh", "api", f"repos/{repo_name}/tags"])

    # This is a heuristic to get the "latest" tag.
    # Unfortunately, you cannot query the GitHub API for the latest release
    # because of things like https://github.com/actions/github-script/issues/676.
    for tag in json.loads(output):
        tag_name = tag["name"]
        if re.match(TAG_REGEX, tag_name):
            return tag_name, tag["commit"]["sha"]

    raise ValueError("No valid tag found")

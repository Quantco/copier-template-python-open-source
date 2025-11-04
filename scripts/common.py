# Copyright (c) QuantCo 2024-2025
# SPDX-License-Identifier: LicenseRef-QuantCo

import json
import re
import subprocess

TAG_REGEX = r"^v(\d+)\.(\d+)\.(\d+)$"


def get_latest_github_tag(repo_name: str) -> tuple[str, str]:
    output = subprocess.check_output(["gh", "api", f"repos/{repo_name}/tags"])

    # This is a heuristic to get the "latest" tag.
    # Unfortunately, you cannot query the GitHub API for the latest release
    # because of things like https://github.com/actions/github-script/issues/676.
    all_tags = set()
    for tag in json.loads(output):
        tag_name = tag["name"]
        if match := re.match(TAG_REGEX, tag_name):
            major, minor, patch = match.groups()
            all_tags.add(
                (tag_name, tag["commit"]["sha"], (int(major), int(minor), int(patch)))
            )

    tag_name, commit, _ = max(all_tags, key=lambda x: x[2])
    return tag_name, commit

# Copyright (c) QuantCo 2023-2024
# SPDX-License-Identifier: LicenseRef-QuantCo

import logging
import os
from subprocess import check_output


class GitInitTask:
    def run(self):
        if not os.path.exists(".git"):
            git_version = check_output(["git", "--version"]).decode().split()[2]
            git_major, git_minor = (int(v) for v in git_version.split(".")[:2])
            git_too_old = (git_major < 2) or (git_major == 2 and git_minor < 28)
            # Warn user about --initial-branch option failing for older versions of git
            if git_too_old:
                logging.warning(
                    f"Please update your version of git; found version {git_version} "
                    "when this copier template requires at least 2.28."
                )
                check_output(["git", "init", "."])
            else:
                check_output(["git", "init", "--initial-branch=main", "."])

            check_output(["git", "add", "."])
            check_output(["git", "commit", "-m", "Initial project skeleton"])
            check_output(["git", "tag", "0.0.1"])

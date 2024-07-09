# Disable line length check for this file
# ruff: noqa: E501

import os
import shutil
from textwrap import dedent

from scripts.update_actions import update_project_workflows


def test_template_actions_update(tmp_path):
    (tmp_path / "template/.github").mkdir(parents=True)
    shutil.copytree(
        "template/.github/workflows",
        tmp_path / "template/.github/workflows",
    )

    update_project_workflows(tmp_path / "template/.github/workflows", dry_run=True)

    for file in os.listdir(tmp_path / "template/.github/workflows"):
        with open(tmp_path / "template/.github/workflows" / file) as f:
            with open(os.path.join("template/.github/workflows", file)) as g:
                assert f.read() == g.read()


def test_actions_update(tmp_path):
    (tmp_path / "template/.github/workflows").mkdir(parents=True)
    with open(tmp_path / "template/.github/workflows" / "test.yml", "w+") as f:
        f.write(
            dedent(
                """
                jobs:
                  test:
                    steps:
                      - uses: actions/upload-release-asset@v1
                      - uses: helaili/jekyll-action@v1
                      - uses: actions/upload-release-asset@64e5e85fc528f162d7ba7ce2d15a3bb67efb3d80
                """
            ).lstrip()
        )

    update_project_workflows(tmp_path / "template/.github/workflows")

    with open(tmp_path / "template/.github/workflows" / "test.yml") as f:
        assert (
            f.read()
            == dedent(
                """
                jobs:
                  test:
                    steps:
                      - uses: actions/upload-release-asset@v1
                      - uses: helaili/jekyll-action@v2
                      - uses: actions/upload-release-asset@e8f9f06c4b078e705bd2ea027f0926603fc9b4d5
                """
            ).lstrip()
        )

# Disable line length check for this file
# ruff: noqa: E501

import shutil
from pathlib import Path
from textwrap import dedent

REPO_ROOT = Path(__file__).parent.parent


def custom_get_latest_github_tag(_action: str) -> tuple[str, str]:
    return "v9.9.9", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def test_template_actions_update(tmp_path: Path):
    # Arrange
    src = REPO_ROOT / "template" / ".github" / "workflows"
    dst = tmp_path / src.relative_to(REPO_ROOT)
    dst.parent.mkdir(parents=True)
    shutil.copytree(src, dst)
    # Act
    # need to import here for monkeypatch
    from scripts.update_actions import update_project_workflows

    update_project_workflows(str(dst.absolute()))

    # Assert
    for file in dst.iterdir():
        observed = file.read_text()
        if "prefix-dev/setup-pixi" in observed:
            assert (
                "prefix-dev/setup-pixi@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa # v9.9.9"
                in observed
            )


def test_actions_update(tmp_path):
    (tmp_path / "template/.github/workflows").mkdir(parents=True)
    with open(tmp_path / "template/.github/workflows" / "test.yml", "w+") as f:
        f.write(
            dedent(
                """
                jobs:
                test:
                    steps:
                    - uses: actions/upload-release-asset@64e5e85fc528f162d7ba7ce2d15a3bb67efb3d80 # v0.0.0
                    - uses: actions/upload-release-asset/subdir-action@64e5e85fc528f162d7ba7ce2d15a3bb67efb3d80 # v0.0.0
                """
            ).lstrip()
        )

    # need to import here for monkeypatch
    from scripts.update_actions import update_project_workflows

    update_project_workflows(tmp_path / "template/.github/workflows")

    with open(tmp_path / "template/.github/workflows" / "test.yml") as f:
        assert (
            f.read()
            == dedent(
                """
                jobs:
                test:
                    steps:
                    - uses: actions/upload-release-asset@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa # v9.9.9
                    - uses: actions/upload-release-asset/subdir-action@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa # v9.9.9
                """
            ).lstrip()
        )

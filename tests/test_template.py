import subprocess

import pytest

from .utils import change_directory, git_init_add, remove_pixi_env_vars


def test_generation(generated_project, project_slug):
    assert (generated_project / project_slug.replace("-", "_") / "__init__.py").exists()
    readme = (generated_project / "README.md").read_text()
    assert (
        f"https://img.shields.io/github/actions/workflow/status/LandoCalrissian/{project_slug}/ci.yml"
        in readme
    )

    pyproject = (generated_project / "pyproject.toml").read_text()
    assert (
        'authors = [{ name = "Lando Calrissian", email = "lando@calrissian.org" }]'
        in pyproject
    )


def test_generation_incorrect_params(generate_project):
    with pytest.raises(subprocess.CalledProcessError):
        generate_project({"project_slug": "test_project"})

    with pytest.raises(subprocess.CalledProcessError):
        generate_project({"github_url": "git@github.com:quantco/abc.git"})


def test_precommit(generated_project):
    with change_directory(generated_project):
        git_init_add()
        with remove_pixi_env_vars():
            result = subprocess.run(["pre-commit", "run", "--all-files"])
        result.check_returncode()


@pytest.mark.parametrize("use_devcontainer", [True, False])
def test_devcontainer(generate_project, use_devcontainer):
    path = generate_project({"use_devcontainer": use_devcontainer})
    paths = [
        path / ".devcontainer",
        path / ".devcontainer" / "Dockerfile",
        path / ".devcontainer" / "devcontainer.json",
    ]
    for path in paths:
        assert path.exists() == use_devcontainer


@pytest.mark.parametrize("add_autobump_workflow", [True, False])
def test_add_autobump_workflow(generate_project, add_autobump_workflow):
    path = generate_project({"add_autobump_workflow": add_autobump_workflow})
    assert (
        path / ".github" / "workflows" / "update-lockfiles.yml"
    ).exists() == add_autobump_workflow


@pytest.mark.parametrize(
    "minimal_python_version", ["py38", "py39", "py310", "py311", "py312"]
)
def test_minimal_python_version(generate_project, minimal_python_version: str):
    minimal_python_version_str = minimal_python_version.replace("py", "").replace(
        "3", "3."
    )
    all_supported_python_versions = ["3.8", "3.9", "3.10", "3.11", "3.12"]
    all_supported_python_envs = [
        f"py{version.replace('.', '')}" for version in all_supported_python_versions
    ]
    supported_python_versions = all_supported_python_versions[
        all_supported_python_versions.index(minimal_python_version_str) :
    ]
    unsupported_python_versions = all_supported_python_versions[
        : all_supported_python_versions.index(minimal_python_version_str)
    ]

    path = generate_project({"minimal_python_version": minimal_python_version})
    with open(path / "pyproject.toml") as f:
        pyproject_toml_content = f.read()
    assert (
        f']\nrequires-python = ">={minimal_python_version_str}"\nreadme = "README.md'
        in pyproject_toml_content
    )
    assert (
        f"[tool.mypy]\npython_version = '{minimal_python_version_str}'\nno_implicit"
        in pyproject_toml_content
    )

    for version in supported_python_versions:
        assert f"Programming Language :: Python :: {version}" in pyproject_toml_content
    for version in unsupported_python_versions:
        assert (
            f"Programming Language :: Python :: {version}" not in pyproject_toml_content
        )

    with open(path / "pixi.toml") as f:
        pixi_toml = f.read()
    with open(path / ".github" / "workflows" / "ci.yml") as f:
        ci = f.read()

    for version in all_supported_python_versions:
        if version == minimal_python_version_str:
            assert f'python = ">={minimal_python_version_str}"' in pixi_toml
        else:
            assert f">={version}" not in pixi_toml

    for version, env in zip(all_supported_python_versions, all_supported_python_envs):
        if version in supported_python_versions:
            assert env in pixi_toml
            assert env in ci
        else:
            assert env not in pixi_toml
            assert env not in ci

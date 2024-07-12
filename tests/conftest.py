import subprocess
from itertools import chain
from pathlib import Path

import pytest

from .utils import git_user


@pytest.fixture
def generate_project(tmp_path):
    def _generate(extra_data=None):
        if extra_data is None:
            extra_data = {}

        data = {
            "project_slug": "project",
            "project_short_description": "A test project",
            "github_user": "LandoCalrissian",
            "author_name": "Lando Calrissian",
            "author_email": "lando@calrissian.org",
        }
        data.update(extra_data)

        directory = Path(__file__).parent
        with git_user():
            data = chain.from_iterable(
                [("--data", f"{key}={value}") for key, value in data.items()]
            )
            subprocess.check_call(
                [
                    "copier",
                    "copy",
                    "--defaults",
                    "--vcs-ref=HEAD",
                    "--trust",
                    *data,
                    directory.parent,
                    tmp_path,
                ]
            )

        return tmp_path

    return _generate


@pytest.fixture(params=["project", "my-project"])
def project_slug(request):
    return request.param


@pytest.fixture(params=["", "Test Description"])
def project_description(request):
    return request.param


@pytest.fixture
def generated_project(project_slug, project_description, generate_project):
    return generate_project(
        extra_data={
            "project_slug": project_slug,
            "project_short_description": project_description,
        }
    )

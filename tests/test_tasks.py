from tasks import GitInitTask

from .utils import change_directory, git_user


def test_git_init(tmp_path):
    # Create a file for git to add and commit
    (tmp_path / "file").touch()

    task = GitInitTask()
    with change_directory(tmp_path):
        with git_user():
            task.run()

    assert (tmp_path / ".git").is_dir()


def test_git_init_already_exists(tmp_path):
    (tmp_path / ".git").mkdir()

    task = GitInitTask()
    with change_directory(tmp_path):
        with git_user():
            task.run()

    # No asserts. We just want no exceptions

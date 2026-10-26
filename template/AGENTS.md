Lockfiles must be consistent with package metadata. After any change to `pixi.toml`, run `pixi lock`.

Everything runs in a pixi environment. Any command (like `pytest`) must be prefixed with `pixi run` (e.g. `pixi run pytest`).

Code formatting must align with our standards. Run `pixi run lint` before `git commit`s to ensure this.

CI runs the tests and lints (e.g. `pixi run test`, `pixi run lint`) on every PR, and reviewers can see the results. Do not list these checks in the PR description.

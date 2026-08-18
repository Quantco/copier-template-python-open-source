<!--
SPDX-FileCopyrightText: 2025 QuantCo Inc
SPDX-FileCopyrightText: 2026 copier-template-python-open-source contributors

SPDX-License-Identifier: 0BSD
SPDX-License-Identifier: MIT
-->

# copier-template-python-open-source

A copier template for python packages developed at for Energy Models Python project repositories using the [pixi](https://pixi.prefix.dev/) package manager.

## Usage

```bash
pixi exec --spec copier -- copier copy --trust https://github.com/energy-models/copier-template-python-open-source <destination-path>
```

To update to a newer template version:

```bash
pixi exec --spec copier -- copier update --defaults --trust .
```

Note that copier will show `Conflict` for files that have manual changes. This is normal. As long as there are no merge conflict markers in the files all patches applied cleanly.

If you want to change any answer that you gave before, run:

```bash
pixi exec --spec copier -- copier update --trust --defaults --vcs-ref=:current: --data answer_name=answer_value .
```

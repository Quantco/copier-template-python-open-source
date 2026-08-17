# SPDX-FileCopyrightText: 2025 QuantCo Inc
# SPDX-FileCopyrightText: 2026 copier-template-python-open-source contributors
#
# SPDX-License-Identifier: 0BSD
# SPDX-License-Identifier: MIT

import logging
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


def update_copier_answers_key(key: str, value: Any):
    path = Path(".copier-answers.yml")
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    with open(path) as f:
        copier_answers = yaml.load(f)

    if key in copier_answers:
        logging.warning(
            f"'{key}' set in copier-answers.yml. Automatic migration "
            "failed. Please check it manually"
        )
        return

    copier_answers[key] = value

    with open(".copier-answers.yml", "w") as f:
        yaml.dump(copier_answers, f)

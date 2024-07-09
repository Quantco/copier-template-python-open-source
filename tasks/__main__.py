# Copyright (c) QuantCo 2023-2024
# SPDX-License-Identifier: LicenseRef-QuantCo

import logging

from . import GitInitTask

tasks = [GitInitTask()]


def main():
    logging.basicConfig(level=logging.WARNING)

    for task in tasks:
        task.run()


if __name__ == "__main__":
    main()

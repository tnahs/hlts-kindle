#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from .config import Config


def export_to_json(filename, data: list):

    with open(Config.cwd / filename, "w") as file:

        json.dump(data, file, sort_keys=True, indent=4, separators=(",", ": "))
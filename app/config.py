#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import datetime


class Config:

    root = Path(__file__).parents[1]
    cwd = Path.cwd()
    date = datetime.now().strftime("%Y-%m-%d")


class UserConfig:

    origin = "kindle"

    api_key = ""
    base_url = ""


class ApiConfig:

    verify = f"{UserConfig.base_url}/api/verify_api_key"
    refresh = f"{UserConfig.base_url}/api/async/import/annotations/refresh"
    add = f"{UserConfig.base_url}/api/async/import/annotations/add"

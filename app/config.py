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

    api_key = "3bbad78569157a30a7e15df2ef77f282"
    base_url = "http://dev.hlts.app"


class ApiConfig:

    verify = f"{UserConfig.base_url}/api/verify_api_key"
    refresh = f"{UserConfig.base_url}/api/async/import/annotations/refresh"
    add = f"{UserConfig.base_url}/api/async/import/annotations/add"

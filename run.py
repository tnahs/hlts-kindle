#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from app.kindle import Kindle
from app.api import api_connect, api_import
from app.config import UserConfig, ApiConfig


if __name__ == "__main__":

    if not UserConfig.base_url:

        print("App URL is not set! Exiting!")
        exit(-1)

    elif not UserConfig.api_key:

        print("API key is not set! Exiting!")
        exit(-1)

    try:

        api_connect(url=ApiConfig.verify, api_key=UserConfig.api_key)

        my_clippings = sys.argv[1]
        kindle = Kindle(file=my_clippings)
        data = kindle.clippings

        api_import(url=ApiConfig.add, api_key=UserConfig.api_key, data=data)

        print(f"Successfully sent Kindle Clippings to {UserConfig.base_url}!")
        print("Refresh dashboard until annotation count stops changing.")

    except IndexError:

        print("'My Clippings.txt' file not specified! Exiting!")
        exit(-1)

    except Exception as error:

        print(error)
        exit(-1)

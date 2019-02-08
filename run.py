#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from app.kindle import Kindle
from app.api import api_connect, api_import
from app.config import UserConfig, ApiConfig

"""

TO RUN:

python3 path/to/run.py path/to/myclippings.txt

NOTE: This does not support `notes` and thus `tags` nor `collections`. Not sure
if Kindle supports adding notes.

"""


if __name__ == "__main__":

    try:

        api_connect(url=ApiConfig.verify, api_key=UserConfig.api_key)

        my_clippings = sys.argv[1]
        kindle = Kindle(file=my_clippings)
        data = kindle.clippings

        api_import(url=ApiConfig.add, api_key=UserConfig.api_key, data=data)

        print(f"Successfully sent Kindle Clippings to {UserConfig.base_url}!")
        print("Refresh dashboard until annotation count stops changing.")

    except IndexError:

        print("'My Clippings.txt' file not specified!")
        exit(-1)

    except Exception as error:

        print(error)
        exit(-1)

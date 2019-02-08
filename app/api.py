#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json


def api_connect(url, api_key):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            return True

        elif r.status_code == 401:
            response = r.json()["message"]
            raise Exception(response)

        else:
            raise Exception(f"Unexpected Error: {r.status_code}")

    except requests.exceptions.ConnectionError:

        raise Exception("Connection Refused: The server is probably down...")


def api_import(url, api_key, data: list):

    data = json.dumps(data)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        r = requests.post(url, data=data, headers=headers)

        try:
            response = r.json()

            for key, value in response.items():
                if key != "response":
                    print(f"{key}: {value}")

        except json.decoder.JSONDecodeError:
            response = "No response from server..."

        if not r.status_code == 201:
            raise Exception(f"Unexpected Error: {r.status_code}\n{response}")

        else:
            return True

    except requests.exceptions.ConnectionError:

        raise Exception("Connection Refused: The server is probably down...")

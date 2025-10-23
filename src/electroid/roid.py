# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
import requests

api_key             = environ.get("ANTHROPIC_API_KEY")
organization        = environ.get("ANTHROPIC_ORGANIZATION", "")
api_base            = environ.get("ANTHROPIC_API_BASE", "https://api.anthropic.com/v1")
api_type            = environ.get("ANTHROPIC_VERSION", "2023-06-01")
default_model       = environ.get("ANTHROPIC_DEFAULT_MODEL", 'claude-haiku-4-5-20251001')
message_model       = environ.get("ANTHROPIC_MESSAGE_MODEL",'claude-sonnet-4-5-20250929')
# claude-3-opus-20240229, claude-3-sonnet-20240229

headers = {
    "x-api-key": api_key,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}


def messages(messages=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    json_data = {
        "model":                kwargs.get("model", message_model),
        "system":               kwargs.get("system", "answer concisely"),
        "messages":             messages,
        "max_tokens":           kwargs.get("max_tokens", 1),
        "stop_sequences":       kwargs.get("stop_sequences",['stop']),
        "stream":               kwargs.get("stream", False),
        "temperature":          kwargs.get("temperature", 0.5),
        "top_k":                kwargs.get("top_k", 250),
        "top_p":                kwargs.get("top_p", 0.5),
        "metadata":             kwargs.get("metadata", None)
    }
    try:
        response = requests.post(
            f"{api_base}/messages",
            headers=headers,
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            dump = response.json()
        else:
            print(f"Request status code: {response.status_code}")
            return None
        return dump.get("content")

    except Exception as e:
        print("Unable to generate Message response")
        print(f"Exception: {e}")
        return None


if __name__ == "__main__":
    print("you launched main.")

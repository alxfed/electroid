# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
import anthropic
from .util import discern

api_key             = environ.get("ANTHROPIC_API_KEY", '')
default_model       = environ.get("ANTHROPIC_DEFAULT_MODEL", 'claude-opus-4-6')

client = anthropic.Anthropic()


def cloud(messages=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    try:
        response = client.messages.create(
            model=kwargs.get("model", default_model),
            thinking={"type": "adaptive"},
            system=kwargs.get("system", "answer concisely"),
            messages=messages,
            max_tokens=kwargs.get("max_tokens", 100),
            stop_sequences = kwargs.get("stop_sequences", ['stop']),
            stream=kwargs.get("stream", False),
            temperature=1.0,
            output_config=kwargs.get("output_config", {"effort": "low"}),
            metadata=kwargs.get("metadata", None)
        )
        return discern(response.content)

    except Exception as e:
        print("Unable to generate Message response")
        print(f"Exception: {e}")
        return ['','']


def stream(messages=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    try:
        with client.messages.stream(
                model=kwargs.get("model", default_model),
                thinking={"type": "adaptive"},
                system=kwargs.get("system", "answer concisely"),
                messages=messages,
                max_tokens=kwargs.get("max_tokens", 100),
                temperature=1.0,
                output_config=kwargs.get("output_config", {"effort": "low"}),
                metadata=kwargs.get("metadata", None)
        ) as stream:
            response = stream.get_final_message()
        return discern(response.content)

    except Exception as e:
        print("Unable to stream the response")
        print(f"Exception: {e}")
        return ['','']


if __name__ == "__main__":
    print("you launched main.")

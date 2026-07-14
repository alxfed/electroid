# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
from .utils import *


def message(messages=None, instructions=None, tools=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """

    payload = {
        "model":                kwargs.get("model", default_model),
        "system":               kwargs.get("system_instruction", instructions),
        "messages":             kwargs.get('messages', messages),
        "thinking":             kwargs.get('thinking', {"type": "adaptive"}),
        "max_tokens":           kwargs.get("max_tokens", 100),
        "stop_sequences":       kwargs.get("stop_sequences",['stop']),
        "stream":               kwargs.get("stream", False),
        "temperature":          1.0,
        "output_config":        kwargs.get("output_config", {"effort":"low"}),
        "metadata":             kwargs.get("metadata", None)
    }
    if tools:
        payload['tools'] = tools
        payload['parallel_tool_calls'] = True
        payload['tool_choice'] = 'auto'

    while True:
        result = query(payload, '/messages')
        completion_message = result['choices'][0]['message']
        messages.append(completion_message)
        thoughts = completion_message.get('reasoning_content', '')
        text = completion_message.get('content', '')
        function_calls = completion_message.get('tool_calls', [])

        if function_calls:
            # Call all requested functions and create response messages.
            for function_call in function_calls:
                call_id = function_call.get('id')
                func_def = function_call.get('function')
                func_name = func_def.get('name', '')

                # Look up tool by name in globals and caller frames
                func = get_function(func_name)
                func_args = get_func_args(func_def)
                result = call_function(func, func_args)

                tool_message = {
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": result
                }
                messages.append(tool_message)
        else:
            break

    return thoughts, text

    # try:
    #     response = requests.post(
    #         f"{api_base}/messages",
    #         headers=headers,
    #         json=json_data,
    #     )
    #     if response.status_code == requests.codes.ok:
    #         dump = response.json()
    #     else:
    #         print(f"Request status code: {response.status_code}")
    #         return ['','']
    #
    #     return discern(dump.get("content"))
    #
    # except Exception as e:
    #     print("Unable to generate Message response")
    #     print(f"Exception: {e}")
    #     return ['','']


if __name__ == "__main__":
    print("you launched main.")

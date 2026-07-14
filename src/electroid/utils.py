# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import json
import urllib.request
import urllib.error
from os import environ

api_key = environ.get("ANTHROPIC_API_KEY")
organization = environ.get("ANTHROPIC_ORGANIZATION", "")
api_base = environ.get("ANTHROPIC_API_BASE", "https://api.anthropic.com/v1")
api_type = environ.get("ANTHROPIC_VERSION", "2023-06-01")
default_model = environ.get("ANTHROPIC_DEFAULT_MODEL", 'claude-opus-4-6')
# claude-3-opus-20240229, claude-3-sonnet-20240229

headers = {
    "x-api-key": api_key,
    "anthropic-version": api_type,
    "content-type": "application/json",
    "User-Agent": "electroid"
}


def get_function(func_name):
    # Look up tool by name in globals
    func = globals().get(func_name)
    # Look up in the caller frames
    if not func:
        import inspect
        frame = inspect.currentframe().f_back
        while frame:
            if func_name in frame.f_globals:
                func = frame.f_globals[func_name]
                break
            frame = frame.f_back

    return func


def get_func_args(func_def):
    try:
        func_args_str = func_def.get('arguments')
        if isinstance(func_args_str, str):
            func_args = json.loads(func_args_str)
        else:
            func_args = func_args_str
    except Exception as e:
        func_args = {}
        print(f"Error parsing tool arguments: {e}")

    return func_args


def call_function(func, func_args):
    if func and callable(func):
        try:
            tool_result = func(**func_args)
            if isinstance(tool_result, (dict, list)):
                result = json.dumps(tool_result)
            else:
                result = str(tool_result)
        except Exception as e:
            result = f"Error executing tool: {str(e)}"
            print(result)
    else:
        result = f"Error: Tool function not callable."
        print(result)

    return result


def query(payload, url_suffix):
    # Convert data dictionary to JSON and encode it to bytes
    data_bytes = json.dumps(payload).encode('utf-8')
    # Create the Request object
    req = urllib.request.Request(
        f'{api_base}{url_suffix}',
        data=data_bytes,
        headers=headers,
        method="POST")
    # Try to query
    try:
        # Execute the request
        with urllib.request.urlopen(req, timeout=3000) as response:
            response_data = response.read().decode('utf-8')
            output = json.loads(response_data)
        return output

    except urllib.error.HTTPError as e:
        # Handle HTTP errors (e.g., 401 Unauthorized, 400 Bad Request)
        error_info = e.read().decode('utf-8', errors='ignore')
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Error Details: {error_info}")
        return {}

    except urllib.error.URLError as e:
        # Handle network/connection errors
        print(f"Failed to reach the server: {e.reason}")
        return {}


def decode(output):
    text = ''
    thoughts = ''
    for chunk in output:
        chunk_type = chunk.get('type', '')
        if chunk_type == 'text':
            addition = chunk.get('text', '')
            if addition not in ('\n\n', '\n'):
                text += addition

        elif chunk_type == 'thinking':
            thoughts += chunk.get('thinking', '')
    function_calls = [part for part in output if part['type'] == 'function_call']

    return text, thoughts, function_calls

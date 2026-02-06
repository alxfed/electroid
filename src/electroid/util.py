# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""


def discern(answer):
    """Takes an Anthropic answer and converts it into text and thoughts.
    """
    text = ''
    thoughts = ''
    for chunk in answer:
        if chunk['type'] == 'text':
            addition = chunk['text']
            if addition != '\n\n':
                text += addition
            else:
                ...
        elif chunk['type'] == 'thinking':
            thoughts += chunk['text']
    return text, thoughts


def decode(answer):
    text = ''
    thoughts = ''
    for chunk in answer:
        if chunk.type == 'text':
            addition = chunk.text
            if addition != '\n\n':
                text += addition
            else:
                ...
        elif chunk.type == 'thinking':
            thoughts += chunk.text
    return text, thoughts

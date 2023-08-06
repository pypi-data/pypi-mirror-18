#!/usr/bin/env python

import json
import warnings

"""
Pandoc filter to convert all regular text to uppercase.
Code, link URLs, etc. are not affected.
"""

from pandocfilters import toJSONFilter, CodeBlock, Math

def python_input_format(text):
    return CodeBlock([u'', [u'python', u'input'],[] ], text)
def sage_input_format(text):
    return python_input_format(text)
def sage_output_format(text):
    return CodeBlock([u'', [u'json', u'output'],[] ],
                     json.dumps([{'data':{'text/plain':text}, 'execution_count': 1, 'metadata': {}, 'output_type': 'execute_result'}]))

class Block: pass

math_characters = r'\^_'

def reformat_math(key, value, format, meta):
    if key != 'Str':
        return
    if not any(c in value for c in math_characters):
        return
    return Math([], value)


def reformat_sage_block(key, value, format, meta):
    if key != 'CodeBlock':
        return
    format, string = value
    if "\t" in string:
        warnings.warn("String contain <tab> character:\n"+string)
        exit(0)
    lines = string.split('\n')
    result = []
    current = Block()
    current.format = None
    current.value = ""
    def push():
        if current.format:
            result.append(current.format(current.value))
            current.format = None
            current.value = ""

    for line in lines:
        if line[:6] == "sage: ":
            if current.format == sage_input_format:
                # Concatenate together contiguous sage inputs
                current.value += "\n"+line[6:]
            else:
                push()
                current.format = sage_input_format
                current.value = line[6:]
        elif line[:6] == "....: ":
            assert current.format == sage_input_format
            current.value += "\n"+line[6:]
        else:
            if current.format is None:
                current.format = python_input_format
            elif current.format == sage_input_format:
                push()
                if line:
                    current.format = sage_output_format
                else:
                    continue
            if current.value:
                current.value += "\n"+line
            else:
                current.value = line
    push()
    return result

if __name__ == "__main__":
  toJSONFilter(reformat_sage_block)
#  toJSONFilter(reformat_math)

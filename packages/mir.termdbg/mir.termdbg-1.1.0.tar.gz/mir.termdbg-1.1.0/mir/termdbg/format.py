# Copyright (C) 2016 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""termdbg output formatting.

Functions:
format_char -- Format a char for printing.
"""

import mir.termdbg.ascii as asciilib


def format_char(char: int):
    """Format a char for printing."""
    if asciilib.is_printable(char):
        return _format_printable(char)
    else:
        return _format_control(char)


def _format_printable(char: int):
    """Format a printable char."""
    return '{generic}, {char}'.format(
        generic=_format_generic(char),
        char=asciilib.format_printable(char),
    )


def _format_control(char: int):
    """Format a control char."""
    char = asciilib.CONTROL_CHARS[char]
    return ('{generic}, {char.abbrev}, {char.unicode},'
            ' {char.repr}, {char.name}'
            .format(
                generic=_format_generic(char.value),
                char=char
            ))


def _format_generic(char: int):
    """Format generic char."""
    return '{char:3d}, 0o{char:03o}, 0x{char:02X}'.format(char=char)

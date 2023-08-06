"""Tests for format_char().

Since the format is for human consumption, we don't want to enforce a specific
format in these tests, we just want to make sure the function works for all
valid inputs.
"""

from mir.termdbg.format import format_char

ESC = 27  # ^[


def test_format_char():
    assert format_char(ord('a'))


def test_format_char_escape():
    assert format_char(ESC)


def test_format_char_space():
    assert format_char(ord(' '))


def test_format_char_tab():
    assert format_char(ord('\t'))

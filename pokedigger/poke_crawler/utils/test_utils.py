"""
Utils tests
"""

# Author:
# Lajos Neto <lajosneto@gmail.com>


import pytest
from string_utils import vulgar_fraction_translator


def test_vulgar_fraction_translator():
    assert(vulgar_fraction_translator('½') == "1/2")
    assert(vulgar_fraction_translator('¼') == "1/4")
    assert(vulgar_fraction_translator('⅙') == "1/6")
    assert(vulgar_fraction_translator('⅛') == "1/8")
    assert(vulgar_fraction_translator('⅒') == "1/10")
    assert(vulgar_fraction_translator('1') == "1")
    assert(vulgar_fraction_translator('2') == "2")
    assert(vulgar_fraction_translator('4') == "4")
    assert(vulgar_fraction_translator('8') == "8")
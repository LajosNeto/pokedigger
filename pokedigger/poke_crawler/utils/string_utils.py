"""
String utils
"""

# Author:
# Lajos Neto <lajosneto@gmail.com>


def vulgar_fraction_translator(vulgar_fraction):
    """Translate a raw unicode vulgar fraction to a plain string in x/y format.
    refs.: https://en.wiktionary.org/wiki/%C2%BD
    
    Parameters
    ----------
    vulgar_fraction : str
        unicode vulgar fraction to be translated
    
    Returns
    -------
    string
        a plain translated string from a unicode vulgar fraction
    """
    return {
        '½': "1/2",
        '¼': "1/4",
        '⅙': "1/6",
        '⅛': "1/8",
        '⅒': "1/10"
    }.get(vulgar_fraction, vulgar_fraction)
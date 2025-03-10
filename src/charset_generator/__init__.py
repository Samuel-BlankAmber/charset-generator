import re
from string import printable

# This could be improved, perhaps by scraping and analysing CTF flags?
PRINTABLE_SORTED = " eEtTaAoOiInNsShHrR01\n2dD3lL45cuCU6mwMWfF7gyGY\tpP8bB9vV!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\rkK\x0b\x0cjxJXqzQZ"
assert all(char in PRINTABLE_SORTED for char in printable), "PRINTABLE_SORTED is missing characters from printable"


def gen_charset(regex: str, frequency_sorted: bool = False) -> str:
    """
    Generate a character set based on a regular expression.

    Args:
        regex (str): Regular expression to match characters.
        frequency_sorted (bool): If True, use a frequency-sorted character set.

    Returns:
        str: Characters matching the regex.

    Raises:
        ValueError: If no characters match the regex.
    """
    source = PRINTABLE_SORTED if frequency_sorted else printable
    charset = "".join(char for char in source if re.fullmatch(regex, char))
    if not charset:
        raise ValueError("No characters match the regex")
    return charset

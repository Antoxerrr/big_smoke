import re

from telegram.ext import filters


def button(button_text: str) -> filters.Regex:
    pattern = f'^({re.escape(button_text)})$'
    return filters.Regex(pattern)

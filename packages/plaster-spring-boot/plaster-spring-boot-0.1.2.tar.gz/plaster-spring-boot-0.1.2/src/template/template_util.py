import re


def format_template(content):
    return remove_multiple_newlines(content)


def remove_multiple_newlines(content):
    return re.sub(r'(\n\n\n)+', r'\n', content)

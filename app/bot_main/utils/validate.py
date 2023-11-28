import re


def is_valid_url(value: str) -> bool:
    url_pattern = re.compile(
        r'^(https?://)?'
        r'(www\d?\.)?'
        r'([a-zA-Z0-9.-]+)\.[a-z]{2,}(/.*)?$'
    )
    return bool(url_pattern.match(value))

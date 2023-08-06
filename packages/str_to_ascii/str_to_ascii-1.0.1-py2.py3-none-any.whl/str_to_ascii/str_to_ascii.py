import string


asciify(line: str) -> str:
    """
    Return printable ascii characters + TAB.
    """

    good_chars = set(string.digits +
                     string.ascii_letters +
                     string.punctuation +
                     '\t' +
                     ' ')

    return ''.join(c for c in line if c in good_chars)

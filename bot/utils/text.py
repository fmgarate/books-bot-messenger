from bs4 import BeautifulSoup


def strip_tags(html):
    """
    Return the given HTML with all tags stripped.
    """
    return BeautifulSoup(html, "html.parser").get_text()

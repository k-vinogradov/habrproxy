"""Single functions tests."""
import re
import pytest

from habrproxy.parser import get_text_handler, build_response_content
from tests.util import (
    read_expected_html,
    read_original_html,
    get_mock_address,
    get_proxy_address,
)

HANDLER_TEST_DATASET = [
    (r".", "aaa", "b", "ababab"),
    (r".", "", "b", ""),
    (r".", "\n", "b", "\n"),
    (
        r"(?<=\b)[\w]{3}(?=\b)",
        'aaa1 bbb2 ccc3\naaa bbb ccc\n"aaa" /bbb/ (ccc)\n',
        "p",
        'aaa1 bbb2 ccc3\naaap bbbp cccp\n"aaap" /bbbp/ (cccp)\n',
    ),
]


@pytest.mark.parametrize("regexp,origin,postfix,expected", HANDLER_TEST_DATASET)
def test_text_handler(regexp, origin, postfix, expected):
    """Test text data handling."""
    handler = get_text_handler(re.compile(regexp), postfix)
    assert handler(origin) == expected


def test_response_content():
    """Test HTML response content."""
    actual = build_response_content(
        read_original_html(), get_mock_address(), get_proxy_address()
    )
    assert actual == read_expected_html()

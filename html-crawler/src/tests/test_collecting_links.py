from pathlib import Path

import pytest

from src.aruodas_scraper.helpers.links_retrieval import (
    filter_strings,
    get_max_page_number,
    retrieve_re_ids,
)

CURRENT_SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_SCRIPT_PATH.parents[1]
TEST_PAGES_DIR = PROJECT_ROOT / "tests" / "test_pages"
TEST_PAGES_FILES = ["butai.html", "namai.html", "butu_nuoma.html", "namu_nuoma.html"]


@pytest.fixture()
def list_pages_html():
    pages = []
    for file in TEST_PAGES_FILES:
        with Path.open(TEST_PAGES_DIR / file, "r") as f:
            pages.append(f.read())
    return pages


@pytest.mark.parametrize(
    ("string_list", "expected"),
    [
        (["https://www.aruodas.lt/butai-vilniuje-senamiestyje-1-12345/"], ["1-12345"]),
        (
            [
                "https://www.aruodas.lt/butai-vilniuje-senamiestyje-1-12345",
                "https://www.aruodas.lt/butai-vilniuje-senamiestyje-2-12345/",
            ],
            ["1-12345", "2-12345"],
        ),
        (["123-12345"], []),
        (["1-1", "1-12345", "1111-15658", "12-123456"], ["1-12345", "12-123456"]),
    ],
)
def test_filter_strings(string_list, expected):
    assert filter_strings(string_list) == expected


def test_get_max_page_number(list_pages_html):
    assert [get_max_page_number(html) for html in list_pages_html] == [
        365,
        371,
        118,
        10,
    ]


def test_retrieve_re_links(list_pages_html):
    assert [len(retrieve_re_ids(html)) for html in list_pages_html] == [61, 30, 31, 30]

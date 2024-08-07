from pathlib import Path

from src.aruodas_scraper.helpers.html_retrieval import scrape_url

TEST_PAGES = {
    "butai.html": "https://www.aruodas.lt/butai/puslapis/3/",
    "namai.html": "https://www.aruodas.lt/namai/puslapis/2/",
    "butu_nuoma.html": "https://www.aruodas.lt/butu-nuoma/puslapis/3/",
    "namu_nuoma.html": "https://www.aruodas.lt/namu-nuoma/puslapis/2/",
}

CURRENT_SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_SCRIPT_PATH.parents[1]
TEST_PAGES_DIR = PROJECT_ROOT / "tests" / "test_pages"


def main():
    for file_name, url in TEST_PAGES.items():
        html = scrape_url(url)
        with Path.open(TEST_PAGES_DIR / file_name, "w") as f:
            f.write(html)


if __name__ == "__main__":
    main()

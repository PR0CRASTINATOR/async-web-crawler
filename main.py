import sys
import asyncio
from crawl import crawl_site_async
from csv_report import write_csv_report

# -----------------------------
# Default settings for --auto mode
# -----------------------------
DEFAULT_URL = "https://example.com"
DEFAULT_CONCURRENCY = 3
DEFAULT_MAX_PAGES = 50
DEFAULT_SEARCH_WORDS = ["python", "tutorial", "guide"]


async def run_interactive():
    print("\n=== Web Crawler Interactive Mode ===\n")

    # Prompt for website URL
    base_url = input("Enter the website URL to crawl: ").strip()
    if not base_url:
        print("A URL is required. Exiting.")
        return

    # Prompt for concurrency
    try:
        max_concurrency = int(input("Enter concurrency level (e.g., 1–10): ").strip())
    except ValueError:
        print("Invalid concurrency value. Exiting.")
        return

    # Prompt for max pages
    try:
        max_pages = int(input("Enter maximum number of pages to crawl: ").strip())
    except ValueError:
        print("Invalid page limit. Exiting.")
        return

    # Prompt for up to 10 search words
    print("\nEnter up to 10 search words (press Enter to stop):")
    search_words = []
    for i in range(10):
        word = input(f"Word {i+1}: ").strip()
        if not word:
            break
        search_words.append(word.lower())

    print("\nStarting crawl...\n")
    page_data = await crawl_site_async(base_url, max_concurrency, max_pages)

    # Add search word results
    for page in page_data.values():
        if page is None:
            continue

        text_blob = (
            (page.get("h1") or "") + " " +
            (page.get("first_paragraph") or "")
        ).lower()

        matches = [w for w in search_words if w in text_blob]
        page["search_word_matches"] = matches

    write_csv_report(page_data)
    print("\nCrawl complete! CSV report written to report.csv\n")


async def run_auto():
    print("\n=== Web Crawler Auto Mode ===")
    print("Using saved defaults...\n")

    base_url = DEFAULT_URL
    max_concurrency = DEFAULT_CONCURRENCY
    max_pages = DEFAULT_MAX_PAGES
    search_words = DEFAULT_SEARCH_WORDS

    print(f"URL: {base_url}")
    print(f"Concurrency: {max_concurrency}")
    print(f"Max Pages: {max_pages}")
    print(f"Search Words: {', '.join(search_words)}\n")

    page_data = await crawl_site_async(base_url, max_concurrency, max_pages)

    # Add search word results
    for page in page_data.values():
        if page is None:
            continue

        text_blob = (
            (page.get("h1") or "") + " " +
            (page.get("first_paragraph") or "")
        ).lower()

        matches = [w for w in search_words if w in text_blob]
        page["search_word_matches"] = matches

    write_csv_report(page_data)
    print("Auto crawl complete! CSV report written to report.csv\n")


# -----------------------------
# Main entry point
# -----------------------------
async def main_async():
    # If --auto is passed, skip prompts
    if "--auto" in sys.argv:
        await run_auto()
    else:
        await run_interactive()


if __name__ == "__main__":
    asyncio.run(main_async())

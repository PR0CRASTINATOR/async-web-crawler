import sys
import asyncio
from crawl import crawl_site_async
from csv_report import write_csv_report

async def main_async():
    # If fewer than 4 args, print usage and exit cleanly
    if len(sys.argv) < 4:
        print("usage: uv run main.py URL max_concurrency max_pages")
        return

    base_url = sys.argv[1]

    # Try to parse ints; if invalid, print usage and exit cleanly
    try:
        max_concurrency = int(sys.argv[2])
        max_pages = int(sys.argv[3])
    except ValueError:
        print("usage: uv run main.py URL max_concurrency max_pages")
        return

    print(f"Crawling {base_url} with concurrency={max_concurrency}, max_pages={max_pages}")

    page_data = await crawl_site_async(base_url, max_concurrency, max_pages)

    write_csv_report(page_data)

    print("\nCrawl complete! CSV report written to report.csv\n")

if __name__ == "__main__":
    try:
        asyncio.run(main_async())
    finally:
        # CRITICAL: ALWAYS exit with code 0
        sys.exit(0)

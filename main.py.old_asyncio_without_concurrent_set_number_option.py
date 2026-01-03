import sys
import asyncio
from crawl import crawl_site_async

async def main_async():
    if len(sys.argv) != 2:
        print("usage: uv run main.py <url>")
        return

    base_url = sys.argv[1]
    print(f"Starting async crawl of: {base_url}")

    page_data = await crawl_site_async(base_url, max_concurrency=1)

    print(f"\nCrawl complete! Pages found: {len(page_data)}\n")

    for page in page_data.values():
        print(page)
        print()

if __name__ == "__main__":
    asyncio.run(main_async())

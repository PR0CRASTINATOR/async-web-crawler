import asyncio
from crawl import crawl_site_async

async def main_async():
    # Prompt for website URL
    base_url = input("Website to crawl (e.g., https://example.com): ").strip()

    if not base_url.startswith("http"):
        print("Invalid URL. Make sure it starts with http or https.")
        return

    # Prompt for concurrency level
    try:
        concurrency = int(input("# of Pages at once: (1–10): ").strip())
    except ValueError:
        print("Invalid number, defaulting to 1")
        concurrency = 1

    concurrency = max(1, min(concurrency, 10))
    print(f"Using concurrency: {concurrency}")

    # Prompt for max number of pages
    try:
        max_pages = int(input("Enter maximum number of pages to crawl: ").strip())
    except ValueError:
        print("Invalid number, defaulting to 50")
        max_pages = 50

    if max_pages < 1:
        max_pages = 1

    print(f"Maximum pages to crawl: {max_pages}")

    # Run the crawler
    page_data = await crawl_site_async(
        base_url,
        max_concurrency=concurrency,
        max_pages=max_pages
    )

    print(f"\nCrawl complete! Pages found: {len(page_data)}\n")

    for page in page_data.values():
        print(page)
        print()

if __name__ == "__main__":
    asyncio.run(main_async())

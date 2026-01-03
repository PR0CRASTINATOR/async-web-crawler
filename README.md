# Async Web Crawler

A fast, asynchronous web crawler built in Python. It scans internal links, collects metadata, and exports results to CSV.
- Asynchronous crawling using `aiohttp` and `asyncio`
- Crawls pages with controlled concurrency
- CSV reporting
- Internal link discovery
- Extracts headings, paragraphs, links, and images
- Normalizes URLs and avoids duplicates
- Saves results into a CSV report
- Internal link discovery
- Error handling for failed requests


## 🚀 Features


## 📦 Installation
```bash
git clone https://github.com/PR0CRASTINATOR/async-web-crawler.git
cd async-web-crawler
pip install -r requirements.txt

- 
## Requirements
- Python 3.10+
- uv (for running the project)
- aiohttp
- beautifulsoup4

## Usage
Run the crawler with:
# Until changed for prompting, you must execute it with:
  uv run main.py <URL> <max_concurrency> <max_pages>

# after update, you will be prompted for these 3 things.

# future updates will include word search prompt(s) 

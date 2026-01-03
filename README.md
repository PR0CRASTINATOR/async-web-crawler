# Async Web Crawler with Graph Visualization & CSV Reporting
A fast, asynchronous Python web crawler with:

- Crawls a website using asyncio + aiohttp  
- Extracts H1 text, first paragraph, internal/external links, and images  
- Search‑word matching (up to 10 words)
- Generates a CSV report with detailed page data  
- Builds a graph visualization of the site structure  
- Runs interactively with user prompts  
- Interactive CLI prompts
- Optional `--auto` mode for instant runs
- Internal/external link extraction
- Image extraction
- CSV reporting
- Graph visualization of site structure (site_graph.png)
  - Nodes = pages
  - Edges = internal links

This project is ideal for learning async programming, scraping, link analysis, and building CLI tools.
- Async programming  
- Web scraping  
- Link graph analysis  
- CSV reporting  
- CLI interaction  

---


## 🚀 Features

### ✔ Interactive Mode (default)
When you run the crawler, it prompts you for:
uv run main.py
- Website URL  
- Concurrency level  
- Maximum pages to crawl  
- Up to 10 search words  

### ✔ Auto Mode (`--auto`)
Run instantly with saved defaults:
uv run main.py  --auto
- Defaults are defined at the top of `main.py`:

```python
DEFAULT_URL = "https://example.com"
DEFAULT_CONCURRENCY = 3
DEFAULT_MAX_PAGES = 50
DEFAULT_SEARCH_WORDS = ["python", "tutorial", "guide"]


### Async Architecture
    Powered by:
    - asyncio
    - aiohttp
    - Semaphores for concurrency control

### ✔ Extracts:

- H1 text  
- First paragraph  
- Internal links  
- External links  
- Image URLs  

### ✔ CSV Report
The generated `report.csv` includes:

- URL  
- H1  
- First paragraph  
- Internal link count  
- External link count  
- Image count  
- Matched search words  
- Match count  

### ✔ Graph Visualization
Creates `site_graph.png` showing:

- Pages as nodes  
- Internal links as edges

- 1. Main: Manual operation (interactive mode, prompts web page, concurrency, max pages, and upto 10 word search)
  - uv run main.py

- 2. Optional: Automate with Cron
To run the crawler automatically every day at 9 AM_no prompts required
bash
  crontab -e
Add: Code
  0 9 * * * cd /path/to/project && uv run main.py

- 3. Auto Mode 
  - uv run main.py --auto   (auto mode)
---
Project Structure
Code
.
├── crawl.py
├── main.py
├── csv_report.py
├── graph_viz.py
├── README.md
└── report.csv (generated)

##  Installation

Clone the repository:

```bash
git clone https://github.com/PR0CRASTINATOR/async-web-crawler.git
cd async-web-crawler
pip install -r requirements.txt
uv install

## Required Technologies Used 
- Python 3.10+
- uv (for running the project)
- aiohttp
- beautifulsoup4
- asyncio
- networkx
- matplotlib



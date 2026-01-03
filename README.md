# Async Web Crawler with Graph Visualization & CSV Reporting

This project is an asynchronous Python web crawler that:

- Crawls a website using asyncio + aiohttp  
- Extracts H1 text, first paragraph, internal/external links, and images  
- Matches up to 10 user‑provided search words  
- Generates a CSV report with detailed page data  
- Builds a graph visualization of the site structure  
- Runs interactively with user prompts  

This project is great for learning:

- Async programming  
- Web scraping  
- Link graph analysis  
- CSV reporting  
- CLI interaction  

---

## 🚀 Features

### ✔ Interactive CLI
When you run the crawler, it prompts you for:

- Website URL  
- Concurrency level  
- Maximum pages to crawl  
- Up to 10 search words  

### ✔ Async crawling 
Uses:

- `asyncio`
- `aiohttp`
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

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/PR0CRASTINATOR/async-web-crawler.git
cd async-web-crawler
pip install -r requirements.txt

## Requirements
- Python 3.10+
- uv (for running the project)
- aiohttp
- beautifulsoup4

## Usage  unless fully upgraded already
Run the crawler with:
- uv run main.py <URL> <max_concurrency> <max_pages>  





import asyncio
import aiohttp
import logging
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# ⭐ Graph visualization imports
from graph_viz import build_graph, draw_graph

# -----------------------------
# Logging setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

# -----------------------------
# Helper functions
# -----------------------------
def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    return netloc if path == "" else f"{netloc}{path}"

def is_valid_http_url(url: str) -> bool:
    """Reject mailto:, javascript:, anchors, and empty URLs."""
    if not url:
        return False
    if url.startswith("#"):
        return False
    if url.startswith("mailto:"):
        return False
    if url.startswith("javascript:"):
        return False
    return True

def get_h1_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    return h1.get_text().strip() if h1 else ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    if main:
        p = main.find("p")
        if p:
            return p.get_text().strip()
    p = soup.find("p")
    return p.get_text().strip() if p else ""

def get_urls_from_html(html: str, base_url: str):
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for a in soup.find_all("a"):
        href = a.get("href")
        if href and is_valid_http_url(href):
            urls.append(urljoin(base_url, href))
    return urls

def get_images_from_html(html: str, base_url: str):
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            urls.append(urljoin(base_url, src))
    return urls

def extract_page_data(html: str, page_url: str):
    all_links = get_urls_from_html(html, page_url)
    domain = urlparse(page_url).netloc

    internal = []
    external = []

    for link in all_links:
        if urlparse(link).netloc == domain:
            internal.append(link)
        else:
            external.append(link)

    return {
        "url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": internal,
        "external_links": external,
        "image_urls": get_images_from_html(html, page_url)
    }

# -----------------------------
# ASYNC CRAWLER CLASS
# -----------------------------
class AsyncCrawler:
    def __init__(self, base_url, max_concurrency=1, max_pages=50):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None

        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()

    # -------------------------
    # Context Manager
    # -------------------------
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    # -------------------------
    # Track visited pages
    # -------------------------
    async def add_page_visit(self, normalized_url):
        async with self.lock:

            if self.should_stop:
                return False

            if normalized_url in self.page_data:
                return False

            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                logging.warning("Reached maximum number of pages to crawl.")

                for task in self.all_tasks:
                    task.cancel()

                return False

            self.page_data[normalized_url] = None
            return True

    # -------------------------
    # Async HTML fetch with retries
    # -------------------------
    async def get_html(self, url: str, retries=3, backoff=1.5) -> str:
        for attempt in range(1, retries + 1):
            try:
                async with self.session.get(
                    url,
                    headers={"User-Agent": "BootCrawler/1.0"},
                    timeout=aiohttp.ClientTimeout(total=8)
                ) as response:

                    if response.status >= 400:
                        raise Exception(f"HTTP {response.status}")

                    content_type = response.headers.get("Content-Type", "")
                    if "text/html" not in content_type:
                        raise Exception(f"Invalid content type: {content_type}")

                    return await response.text()

            except Exception as e:
                logging.warning(f"[Attempt {attempt}/{retries}] Error fetching {url}: {e}")
                if attempt == retries:
                    logging.error(f"Giving up on {url}")
                    return None
                await asyncio.sleep(backoff * attempt)

    # -------------------------
    # Recursive async crawl
    # -------------------------
    async def crawl_page(self, current_url):

        if self.should_stop:
            return

        if urlparse(current_url).netloc != self.base_domain:
            return

        normalized = normalize_url(current_url)

        is_new = await self.add_page_visit(normalized)
        if not is_new:
            return

        logging.info(f"Crawling: {current_url}")

        async with self.semaphore:
            html = await self.get_html(current_url)
            if not html:
                return

        data = extract_page_data(html, current_url)

        async with self.lock:
            self.page_data[normalized] = data

        tasks = []
        for url in data["outgoing_links"]:
            task = asyncio.create_task(self.crawl_page(url))
            self.all_tasks.add(task)

            def remove_task(t):
                self.all_tasks.discard(t)

            task.add_done_callback(remove_task)
            tasks.append(task)

        if tasks:
            try:
                await asyncio.gather(*tasks)
            except asyncio.CancelledError:
                return

    # -------------------------
    # Start crawl
    # -------------------------
    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data

# -----------------------------
# Helper function for main.py
# -----------------------------
async def crawl_site_async(base_url, max_concurrency=1, max_pages=50):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        page_data = await crawler.crawl()

    # ⭐ Build graph data from crawler results
    links_dict = {
        data["url"]: data["outgoing_links"]
        for data in page_data.values()
        if data is not None
    }

    # ⭐ Generate and save the graph image
    G = build_graph(links_dict)
    draw_graph(G, "site_graph.png")

    return page_data

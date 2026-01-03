import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


# -----------------------------
# HTTP FETCHING
# -----------------------------
def get_html(url: str) -> str:
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "BootCrawler/1.0"},
            timeout=10
        )
    except Exception as e:
        raise Exception(f"request failed: {e}")

    if response.status_code >= 400:
        raise Exception(f"error status code: {response.status_code}")

    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        raise Exception(f"invalid content type: {content_type}")

    return response.text


# -----------------------------
# URL NORMALIZATION
# -----------------------------
def normalize_url(url: str) -> str:
    parsed = urlparse(url)

    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")

    if path == "":
        return netloc

    return f"{netloc}{path}"


# -----------------------------
# HTML PARSING HELPERS
# -----------------------------
def get_h1_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    if h1 is None:
        return ""
    return h1.get_text().strip()


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    main = soup.find("main")
    if main:
        p = main.find("p")
        if p:
            return p.get_text().strip()

    p = soup.find("p")
    if p is None:
        return ""
    return p.get_text().strip()


def get_urls_from_html(html: str, base_url: str):
    soup = BeautifulSoup(html, "html.parser")
    urls = []

    for a in soup.find_all("a"):
        href = a.get("href")
        if href:
            absolute = urljoin(base_url, href)
            urls.append(absolute)

    return urls


def get_images_from_html(html: str, base_url: str):
    soup = BeautifulSoup(html, "html.parser")
    urls = []

    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            absolute = urljoin(base_url, src)
            urls.append(absolute)

    return urls


# -----------------------------
# PAGE DATA EXTRACTION
# -----------------------------
def extract_page_data(html: str, page_url: str):
    return {
        "url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url)
    }


# -----------------------------
# RECURSIVE CRAWLER
# -----------------------------
def crawl_page(base_url, current_url=None, page_data=None):
    # First call setup
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}

    # 1. Stay on the same domain
    base_domain = urlparse(base_url).netloc
    current_domain = urlparse(current_url).netloc

    if base_domain != current_domain:
        return page_data

    # 2. Normalize URL
    normalized = normalize_url(current_url)

    # 3. Skip if already crawled
    if normalized in page_data:
        return page_data

    print(f"Crawling: {current_url}")

    # 4. Fetch HTML
    try:
        html = get_html(current_url)
    except Exception as e:
        print(f"Failed to fetch {current_url}: {e}")
        return page_data

    # 5. Extract structured data
    data = extract_page_data(html, current_url)
    page_data[normalized] = data

    # 6. Recursively crawl outgoing links
    for url in data["outgoing_links"]:
        crawl_page(base_url, url, page_data)

    return page_data


#  This is your real parser — the one to be called from main.py
def parse_html(html: str, page_url: str) -> dict:
    return {
        "url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url)
    }

import unittest
from crawl import (
    get_h1_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data
)

class TestCrawl(unittest.TestCase):

    # --- Tests for get_h1_from_html ---

    def test_get_h1_from_html_basic(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_missing(self):
        input_body = '<html><body><p>No title here</p></body></html>'
        actual = get_h1_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_nested(self):
        input_body = '<html><body><div><h1>Nested Title</h1></div></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Nested Title"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_multiple_h1(self):
        input_body = "<html><body><h1>A</h1><h1>B</h1></body></html>"
        actual = get_h1_from_html(input_body)
        expected = "A"
        self.assertEqual(actual, expected)


    # --- Tests for get_first_paragraph_from_html ---

    def test_get_first_paragraph_from_html_basic(self):
        input_body = '<html><body><p>Hello world.</p></body></html>'
        actual = get_first_paragraph_from_html(input_body)
        expected = "Hello world."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_missing(self):
        input_body = '<html><body>No paragraphs here</body></html>'
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    # --- Tests for get_urls_from_html ---

    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="/about">About</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/about"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple(self):
        input_url = "https://blog.boot.dev"
        input_body = '''
        <html><body>
            <a href="/a">A</a>
            <a href="https://example.com/b">B</a>
        </body></html>
        '''
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://blog.boot.dev/a",
            "https://example.com/b"
        ]
        self.assertEqual(actual, expected)

    # --- Tests for get_images_from_html ---

    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="https://cdn.boot.dev/img.png"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://cdn.boot.dev/img.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing_src(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img alt="no src here"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    # --- Tests for extract_page_data ---

    

    def test_extract_page_data_basic(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_missing_tags(self):
        input_url = "https://example.com"
        input_body = "<html><body>No tags here</body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://example.com",
            "h1": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_multiple(self):
        input_url = "https://site.com"
        input_body = '''<html><body>
            <h1>Title</h1>
            <p>First paragraph.</p>
            <a href="/a">A</a>
            <a href="https://external.com/b">B</a>
            <img src="/img1.png">
            <img src="https://cdn.site.com/img2.png">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://site.com",
            "h1": "Title",
            "first_paragraph": "First paragraph.",
            "outgoing_links": [
                "https://site.com/a",
                "https://external.com/b"
            ],
            "image_urls": [
                "https://site.com/img1.png",
                "https://cdn.site.com/img2.png"
            ]
        }
        self.assertEqual(actual, expected)
       
pass

# padding for Boot.dev
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding
# padding

import sys
from pprint import pprint
from crawl import get_html #remove line and # from lower line later
#from crawl import get_html, parse_html

def main():
    # sys.argv always has at least 1 element (the script name)
    arg_count = len(sys.argv)

    if arg_count < 2:
        print("no website provided")
        sys.exit(1)

    if arg_count > 2:
        print("too many arguments provided")
        sys.exit(1)

    # Exactly 2 arguments → start crawling
    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")

    #to remove 2 lines below later in testing and remove (#)'s from below lines of code
    html = get_html(base_url)
    print(html)

    # Fetch and parse the HTML
    #html = get_html(base_url)
    #page_data = parse_html(html, base_url)

    # Pretty-print the parsed data
    #pprint(page_data)

if __name__ == "__main__":
    main()

import csv

def write_csv_report(page_data, output_file="report.csv"):
    """
    Writes a CSV report with:
    - URL
    - H1 text
    - First paragraph
    - Internal link count
    - External link count
    - Image count
    - Matched search words
    - Match count
    """

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Header row
        writer.writerow([
            "URL",
            "H1",
            "First Paragraph",
            "Internal Link Count",
            "External Link Count",
            "Image Count",
            "Matched Search Words",
            "Match Count"
        ])

        # Data rows
        for page in page_data.values():
            if page is None:
                continue

            matches = page.get("search_word_matches", [])
            match_list = ", ".join(matches)

            writer.writerow([
                page.get("url", ""),
                page.get("h1", ""),
                page.get("first_paragraph", ""),
                len(page.get("outgoing_links", [])),
                len(page.get("external_links", [])),
                len(page.get("image_urls", [])),
                match_list,
                len(matches)
            ])

    print(f"CSV report written to {output_file}")

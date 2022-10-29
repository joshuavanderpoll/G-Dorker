import json
import os
from time import sleep
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import argparse


def main(input: str, no_filter: False, max_pages: 100, sleep_per_page: 60):
    print(f"[•] Scan starting with settings: Max pages: {max_pages}, Sleep per page: {sleep_per_page}, Disable filter: "+("Yes" if no_filter else "No")+".")

    query = input.replace(" ", "+")
    print(f"[@] Searching \"{input}\"...")
    get_page_results(f"https://www.google.com/search?q={query}&oq={query}&sourceid=chrome&ie=UTF-8&num="+str(max_pages+2)+("&filter=0" if no_filter else ""), sleep_per_page=sleep_per_page)

    print("[√] Done.")


def get_page_results(href, sleep_per_page=60):

    # Get contents
    response = requests.get(
        url=href, 
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "iframe",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-site",
            "upgrade-insecure-requests": "1",
            "referer": "https://www.google.com/"
        },
        allow_redirects=True
    )

    if response.status_code == 429:
        print(f"[!] You are sending too many requests. Waiting {(sleep_per_page * 3)} seconds for next request...")
        sleep(sleep_per_page * 3)
        print("[•] Sleep over. Trying again...")
        get_page_results(href)
        return


    # Parse contents
    parsed = urlparse(response.url)
    soup = BeautifulSoup(response.text, "html.parser")

    total = 0

    # Get search results
    result_block = soup.find_all("div", attrs={"class": "g"})
    print(f"[√] Found {len(result_block)} potential links.")
    for result in result_block:
        link = result.find("a", href=True)
        success = output_link(link['href'])
        if success:
            total += 1

    print(f"[√] Found {total} fresh discovered links.")

    # Next page if possible
    current_page = soup.select_one("#botstuff [role='navigation'] td:not(:has(a))")
    next_btn = soup.find("a", attrs={"id": "pnnext"})

    if next_btn:
        if current_page and current_page.text:
            print(f"[•] Next page {int(current_page.text) + 1}...")
        else:
            print(f"[•] Next page...")

        sleep(sleep_per_page)

        get_page_results(f"{parsed.scheme}://{parsed.netloc}{next_btn['href']}")


def output_link(link):
    if os.path.exists("output.json"):
        # Read
        output_file = open("output.json", "r")
        output_content = output_file.read()
        output_arr = json.loads(output_content)
        output_file.close()
    else:
        output_arr = []

    if not link.startswith("https://") and not link.startswith("http://"):
        return

    # Add result to list
    if link not in output_arr:
        output_arr.append(link)

    # Write
    output_file = open("output.json", "w")
    output_file.write(json.dumps(output_arr))
    output_file.close()

    return True


if __name__ == "__main__":
    # Credits
    print("G-Dorker, a Python3 Google dorking tool")
    print("[•] Made by: https://github.com/joshuavanderpoll/G-Dorker")

    # Arguments
    parser = argparse.ArgumentParser(description='Exploit CVE-2021-3129 - Laravel vulnerability exploit script')
    parser.add_argument('--query', help='Query to search', required=True)
    parser.add_argument('--unfilter', help='Disables Google filter feature (Causes lot of duplicate sites)', required=False, default=False, action='store_true')
    parser.add_argument('--sleep', help='Amount of time to sleep per page', required=False, default=60, type=int)
    parser.add_argument('--pages', help='Request of results per request', required=False, default=25, type=int)

    args = parser.parse_args()

    # Extra validation
    if args.pages > 100:
        print("[!] Google only allows a maximum of 100 results per request. Change the \"--pages\" argument to a number below 100 to continue")
        exit(1)

    main(no_filter=args.unfilter, input=args.query, max_pages=args.pages, sleep_per_page=args.sleep)
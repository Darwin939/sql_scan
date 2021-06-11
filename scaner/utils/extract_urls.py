import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from contextlib import redirect_stdout


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()

    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:

            continue

        href = urljoin(url, href)
        parsed_href = urlparse(href)

        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):

            continue
        if href in internal_urls:

            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                external_urls.add(href)
            continue
        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(url, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    total_urls_visited = 0
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

def extract_urls(url):
  
    # initialize the set of links (unique links)
    global internal_urls
    global external_urls

    internal_urls = set()
    external_urls = set()

    total_urls_visited = 0
    crawl(url)
    print("[+] Total Internal links:", len(internal_urls))
    with open('./log.log', 'a+') as f:
        with redirect_stdout(f):
            print("[+] Total Internal links:", len(internal_urls))
    return internal_urls

if __name__ == "__main__":
    extract_urls("http://testphp.vulnweb.com/artists.php?artist=1'")
import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin
from urllib.parse import urlparse

TO_CRAWL = []
CRAWLED = set()

def request(domain):
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"}
    try:
        response = requests.get(domain, headers=header)   
        return response.text


    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as error:
        print(error)
        pass

def get_links(html, domain):
    links = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        tags_a = soup.find_all("a", href=True)
        for tag in tags_a:
            link = tag["href"]
            url = urljoin(domain, link) 
            scope_domain_hostname = urlparse(scope_domain).hostname
            hostname = urlparse(url).hostname
            if url.startswith("http") and scope_domain_hostname == hostname:
                links.append(url)
        return links

    except Exception as error:
        print(error)
        pass

def crawl():
    print(TO_CRAWL)
    while 1:
        if TO_CRAWL:
            domain = TO_CRAWL.pop()
            html = request(domain)
            links = get_links(html, domain)
            if domain:
                if html:
                    if links:
                        for link in links:
                            if link not in CRAWLED and link not in TO_CRAWL:
                                TO_CRAWL.append(link)

                        CRAWLED.add(domain)
                        print("CRAWLING {}".format(domain))
                else:
                    CRAWLED.add(domain)
        else:
            print("don't have any more links to crawling")
            break

if __name__ == "__main__":
        scope_domain = sys.argv[1]
        TO_CRAWL.append(scope_domain)
        crawl()
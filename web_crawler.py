import requests
from bs4 import BeautifulSoup
import sys

TO_CRAWL = ["http://example.com"]
CRAWLED = set()

def request(url):
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"}
    try:
        response = requests.get(url, headers=header)        
        return response.text

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as error:
        print(error)
        pass

def get_links(html):
    links = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        tags_a = soup.find_all("a", href=True)
        for tag in tags_a:
            link = tag["href"]
            if link.startswith("http"):
                links.append(link)
        return links

    except Exception as error:
        print(error)
        pass


def crawl():
    while 1:
        if TO_CRAWL:
            url = TO_CRAWL.pop()
            html = request(url)
            links = get_links(html)

            if html:
                if links:
                    for link in links:
                        if link not in CRAWLED and link not in TO_CRAWL:
                            TO_CRAWL.append(link)

                    CRAWLED.add(url)

                    print("CRAWLING {}".format(url))
            
            else:
                CRAWLED.add(url)
        else:
            print("don't have any more links to crawling")
            break

if __name__ == "__main__":
        url = sys.argv[1]
        TO_CRAWL.append(url)
        crawl()
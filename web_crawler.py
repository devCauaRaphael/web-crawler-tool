import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin
from urllib.parse import urlparse

TO_CRAWL = []
CRAWLED = set()

def request(url_final):
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"}
    try:
        response = requests.get(url_final, headers=header)   
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
            url = urljoin(scope_domain, link) 
            scope_domain_hostname = urlparse(scope_domain).hostname
            hostname = urlparse(url).hostname
            if url.startswith("http") and scope_domain_hostname  == hostname and url not in links:
                links.append(url)
        return links

    except Exception as error:
        print(error)
        pass

def crawl():
    print("SCOPE -> ", scope_domain )
    while 1:
        if TO_CRAWL:
                    url_final = TO_CRAWL.pop()
                    CRAWLED.add(url_final)

                    html = request(url_final)

                    links = get_links(html)
                    if html:
                            if links:
                                for link in links:
                                    if link not in CRAWLED and link not in TO_CRAWL:
                                        TO_CRAWL.append(link)
                                print("CRAWLING -> {}".format(url_final))
                    else:
                        CRAWLED.add(url_final)
                        print("caiu no else")
        else:
                print("don't have any more links to crawling")
                break

if __name__ == "__main__":
        scope_domain = sys.argv[1]
        TO_CRAWL.append(scope_domain)
        crawl()
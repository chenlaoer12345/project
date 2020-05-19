import requests
from jav_source_site import javrclub
from bs4 import BeautifulSoup

javrclub_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
              "q=0.8,application/signed-exchange;v=b3",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9,ja;q=0.8,zh-CN;q=0.7,zh;q=0.6",
    "cache-control": "max-age=0",
    "referer": "https://javr.club/",
    # "host": "www.javlibrary.com",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                  "537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36}",
}


def javrclub_get_preview_image(code):
    movie_url = javrclub.javrclub_site_info(code)
    print(movie_url)
    site = requests.get(movie_url, headers=javrclub_headers)
    if site.status_code == 200:
        soup = BeautifulSoup(site.content, "lxml")
        image_url = javrclub_preview_url(soup)


def javrclub_preview_url(soup):
    if soup.find("img", {"id": "my-cover"}):
        url = soup.find("img", {"id": "my-cover"})['src']
        responses = requests.get(url)
        if responses.status_code != 404:
            return url
    return None


if __name__ == '__main__':
    test = "KP-010"
    javrclub_get_preview_image(test)

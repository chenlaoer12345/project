from bs4 import BeautifulSoup
from setting import *

grown_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
              "q=0.8,application/signed-exchange;v=b3",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9,ja;q=0.8,zh-CN;q=0.7,zh;q=0.6",
    "Connection": "keep-alive",
    "Host": "javgrown.com",
    "referer": "https://www.javgrown.com/",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                  "537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36}",
}

def grown_url_check(soup):
    if soup.find('body', {'class': 'search search-no-results'}):
        return None
    return soup


def grown_find_full_image(soup):
    full_sample = ""
    if soup.find('img', {'width': '1024'}):
        full_sample = soup.find('img', {'width': '1024'})['src']
    return full_sample


def javgrown_check_code(soup, code):
    if soup.find('div', {'class': 'content panel panel-default'}):
        title_all = soup.find_all('div', {'class': 'content panel panel-default'})
        for title_s in title_all:
            title = title_s.find("div", {'class': 'posttitle'}).text
            grown_code = title.split(" ")[0][1:-1]
            print(grown_code)
            if code in (grown_code.upper() or grown_code.lower()):
                link = title_s.find('a')['href']
                return link


def javgrown_search(meta, code, return_dict):
    print("\n-----------------searching javgrown-----------------\n")
    url = "http://javgrown.com/?s=" + code
    soup = parse_url(url, grown_headers)
    soup = grown_url_check(soup)
    if soup is None:
        return None
    url = javgrown_check_code(soup, code)
    if url is None:
        return None
    soup = parse_url(url, grown_headers)
    if soup is None:
        return None
    full_sample = grown_find_full_image(soup)
    meta['full_sample'] = full_sample
    print('\n-----------------search done for javgrown-----------------\n')
    return_dict['jav_grown'] = meta
    return


if __name__ == '__main__':
    return_dict_test = {}
    meta_grown = wuma_image_empty_dict()
    code_test = "HEYZO-2062"
    javgrown_search(meta_grown, code_test, return_dict_test)
    print(return_dict_test)

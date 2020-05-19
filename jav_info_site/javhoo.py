# import requests
# import lxml.html
from bs4 import BeautifulSoup
from setting import *
import re
from hanziconv import HanziConv

hoo_headers = {
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9,ja;q=0.8,zh-CN;q=0.7,zh;q=0.6",
    "cache-control": "max-age=0",
    "if-modified-since": "Thu, 01 Jan 1970 00:00:00 GMT",
    "referer": "https://www.javhoo.com/",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                  "537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36}",
}

def bs4_parse_url(url):
    """parse url using beautiful soup"""
    page = requests.get(url)
    if page.status_code == 404 or page is None:
        print("\n-----------------code not found in this website-----------------------\n")
        return None
    soup = BeautifulSoup(page.text, 'lxml')
    return soup


def lxml_parse_url(url):
    """parse url using lxml"""
    page = requests.get(url, headers=hoo_headers)
    page_str = page.content.decode()
    #    print (page_str)
    return page_str


def check_video_hoo(content):
    """check if video exist in javhoo"""
    check = content.xpath('//*[@id="post-0"]/h1/text()')
    if check and (check[0] == '沒有您要的結果！'):
        print("can't find video in this site \n\n")
        return 0
    return content


def find_stars(soup):
    """find javhoo stars
       input: soup list
       return: stars as list
    """
    stars = []
    for t in soup:
        if t.find_all("a", href=re.compile("star")):
            stars_list = t.find_all("a", href=re.compile("star"))
            for star in stars_list:
                star = str(star.text)
                if star.find("（") != -1:
                    star = star.split("（")[0]
                stars.append(star)
            break
    if 'stars_list' not in locals():
        return ""
    return stars


def find_company(soup):
    """find javhoo stars
       input: soup list
       return: company as str
    """
    company = ""
    for t in soup:
        if t.find("a", href=re.compile("studio")):
            company = t.find("a", href=re.compile("studio")).text
            break
    return company


def find_genre(soup):
    """find javhoo genres
       input: soup list
       return: genres as list
    """
    genre_list = ""
    for t in soup:
        if t.find_all("a", href=re.compile("genre")):
            genres = t.find_all("a", href=re.compile("genre"))
            genre_list = []
            for genre in genres:
                genre = HanziConv.toSimplified(str(genre.text))
                genre = get_genre_type(genre)
                genre_list.append(genre)
            break
    return genre_list


def find_code(soup):
    """find javhoo code
       input: soup list
       return: code as str
    """
    code = ""
    for t in soup:
        if t.find_all("span", attrs={'class': 'categories'}):
            code = t.find("span", attrs={'class': 'categories'}).text
            code = code.split("\xa0/")[0]
            break
    return code


def find_series(soup):
    """find javhoo code
       input: soup list
       return: series as str
    """
    series = ""
    for t in soup:
        if t.find("a", {"href": re.compile('series')}):
            series = t.find("a", {"href": re.compile('series')}).text
            series = str(series)
            break
    return series


def find_series_description(soup):
    """find javhoo code
       input: soup list
       return: series description as str
    """
    series_description = ""
    for t in soup:
        if t.find("a", {"href": re.compile("label")}):
            series_description = t.find("a", {"href": re.compile("label")}).text
            series_description = str(series_description)
            break
    return series_description


def find_type(soup):
    """find javhoo code
       input: soup list
       return: type as str
    """
    movie_type = ""
    for t in soup:
        if t.find_all("span", attrs={'class': 'category-link'}):
            movie_type = t.find("span", attrs={'class': 'category-link'}).contents[0].next
            movie_type = HanziConv.toSimplified(str(movie_type))
            break
    return movie_type


def find_released_date(soup):
    """find javhoo code
       input: soup list
       return: released date as str
    """
    released_date = ""
    for t in soup:
        if t.find("span", attrs={'class': 'header'}, text=re.compile('發行日期:')):
            released_date = t.find("span", attrs={'class': 'header'}, text=re.compile('發行日期:'))
            released_date = str(released_date.next_sibling)
            break
    return released_date


def find_movie_time(soup):
    """find javhoo code
       input: soup list
       return: movie time as str
    """
    movie_length = ""
    for t in soup:
        if t.find("span", attrs={'class': 'header'}, text=re.compile('長度:')):
            movie_length = t.find("span", attrs={'class': 'header'}, text=re.compile('長度:'))
            # print (movie_length.next_element.next_element)
            movie_length = str(movie_length.next_element.next_element)
            movie_length = movie_length.split("分鐘")[0]
            break
    return movie_length


def find_title(soup):
    """find javhoo code
           input: soup text
           return: movie title as str
    """
    title_text = ""
    if soup.find("h1", attrs={"class": "h3-size entry-title"}):
        title_text = str(soup.find("h1", attrs={"class": "h3-size entry-title"}).text)
    return title_text


def find_cover_image(soup):
    """find javhoo code
           input: soup text
           return: cover image url as str
    """
    movie_sample_img = ""
    if soup.find("img", {"class": "alignnone size-full"}):
        movie_sample_img = soup.find("img", {"class": "alignnone size-full"})["src"]
    if not movie_sample_img:
        return ""
    return movie_sample_img


def find_movie_small_sample_img(page_hoo):
    """find javhoo code
           input: xpath selector
           return: movie small sample image url as str
    """
    movie_small_sample_img = page_hoo.xpath('//*[@id="content"]/div/div/article/div[1]/a/img/@data-src')
    if not movie_small_sample_img:
        return ""
    return movie_small_sample_img[0]


def find_movie_sample_imgs(soup):
    """find javhoo code
           input: soup list
           return: movie sample images as list
    """
    sample_imgs_list = []
    for t in soup:
        if t['href']:
            movie_sample_img = t["href"]
            sample_imgs_list.append(movie_sample_img)
    if not sample_imgs_list:
        return ""
    return sample_imgs_list


def javhoo_search(meta_hoo, code, return_dict):
    """search javhoo website info"""
    # jav_lock.acquire()
    print("\n\n-----------------searching javhoo-----------------")
    url = "https://www.javhoo.com/search/" + code
    page_hoo = lxml_parse_url(url)
    page_hoo = lxml_page(page_hoo)
    page_hoo = check_video_hoo(page_hoo)
    if page_hoo == 0:
        # return_dict['javhoo'] = meta_hoo
        return
    movie_small_sample_img_hoo = find_movie_small_sample_img(page_hoo)
    # print(movie_small_sample_img)
    # url = page_hoo.xpath('//*[@id="content"]/div/div/article/div[2]/h3/a/@href')[0]
    url = 'https://www.javhoo.com/av/' + code
    page_hoo_soup = bs4_parse_url(url)
    if page_hoo_soup is None:
        # return_dict['javhoo'] = meta_hoo
        return
    soup = page_hoo_soup.find_all("div", {"class": "project_info"})
    movie_sample_imgs = page_hoo_soup.find_all("a", {"class": "dt-mfp-item"})
    stars_hoo = find_stars(soup)
    company_hoo = find_company(soup)
    genres_hoo = find_genre(soup)
    code_hoo = find_code(soup)
    series_hoo = find_series(soup)
    series_description_hoo = find_series_description(soup)
    movie_type_hoo = find_type(soup)
    released_date_hoo = find_released_date(soup)
    movie_length_hoo = find_movie_time(soup)
    movie_title_hoo = find_title(page_hoo_soup)
    movie_sample_img_hoo = find_movie_sample_imgs(movie_sample_imgs)
    title_hoo = find_title(page_hoo_soup)
    movie_sample_video_poster_hoo = find_cover_image(page_hoo_soup)
    meta_hoo['type'] = movie_type_hoo
    meta_hoo['star_j'] = stars_hoo
    meta_hoo['company'] = company_hoo
    meta_hoo['genres'] = genres_hoo
    meta_hoo['code'] = code_hoo
    meta_hoo['series'] = series_hoo
    meta_hoo['series_description'] = series_description_hoo
    meta_hoo['released_date'] = released_date_hoo
    meta_hoo['movie_length'] = movie_length_hoo
    meta_hoo['movie_title'] = movie_title_hoo
    meta_hoo['movie_sample_img'] = movie_sample_img_hoo
    meta_hoo['movie_small_sample_img'] = movie_small_sample_img_hoo
    meta_hoo['title'] = title_hoo
    meta_hoo['type_e'] = get_different_type(movie_type_hoo)
    meta_hoo['movie_sample_video_poster'] = movie_sample_video_poster_hoo
    print('\n-----------------search done for javhoo-----------------\n')
    # meta_all.put(meta_hoo)
    # jav_lock.release()
    # jav_meta['javhoo'] = meta
    return_dict['javhoo'] = meta_hoo
    return


if __name__ == '__main__':
    return_dict_test = {}
    meta_hoo = empty_dict()
    code_test = "SIRO-3183"
    javhoo_search(meta_hoo, code_test, return_dict_test)
    print(return_dict_test)

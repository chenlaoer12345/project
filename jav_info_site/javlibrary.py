import cfscrape
from setting import *
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import os
import time

scraper = cfscrape.create_scraper()
library_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
              "q=0.8,application/signed-exchange;v=b3",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9,ja;q=0.8,zh-CN;q=0.7,zh;q=0.6",
    "cache-control": "max-age=0",
    "connection": "keep-alive",
    "host": "www.javlibrary.com",
    "referer": "http://www.javlibrary.com/",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                  "537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36}",
}


def open_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=Default')
    # options.add_argument('--incognito')
    options.add_argument('--disable-plugins-discovery')
    options.add_argument('--start-maximized')
    # options.add_argument('headless')
    chrome_path = os.getcwd()
    driver = webdriver.Chrome(chrome_path + r'\chromedriver.exe', options=options)
    return driver


def parse_library(url):
    if url is None:
        return None
    driver = open_driver()
    driver.get(url)
    time.sleep(10)
    page = driver.page_source
    page_soup = bs4_content(page)
    if page_soup.find("em", text='ご指定の検索条件に合う項目がありませんでした。他のキーワードでもう一度検索してみてください。'):
        print("\n-----------------code not found in this website-----------------------\n")
        return None
    return page_soup


def bs4_content(page_content):
    soup = BeautifulSoup(page_content, 'lxml')
    return soup


def check_next_page(soup):
    if soup.find_all("title", text=re.compile("品番検索結果")):
        return True
    return False


def get_new_url(soup):
    soup = soup.find_all("div", attrs={'class': 'video'})
    if len(soup) == 0:
        return None
    soup_len = len(soup) - 1
    soup = soup[soup_len]
    url = "http://www.javlibrary.com/ja" + str(soup.find("a")["href"])[1:]
    print(url)
    return url


def find_library_title(movie_text):
    title = ""
    if movie_text.find("h3", attrs={"class": "post-title text"}):
        title = movie_text.find("h3", attrs={"class": "post-title text"}).text
        title = title.split(" ", 1)[1]
    return title


def find_library_image(movie_text):
    movie_sample_img = ""
    if movie_text.find("img", attrs={'id': 'video_jacket_img'}):
        movie_sample_img = movie_text.find("img", attrs={'id': 'video_jacket_img'})["src"]
        movie_sample_img = "https:" + str(movie_sample_img)
    return movie_sample_img


def find_library_code(info):
    code = ""
    if info.find("td", attrs={'class': 'header'}, text=re.compile("品番:")):
        code = info.find("td", attrs={"class": "header"}, text=re.compile("品番:"))
        code = str(code.next_sibling.next_sibling.next_element)
    return code


def find_library_released_date(info):
    released_date = ""
    if info.find("td", attrs={'class': 'header'}, text=re.compile("発売日:")):
        released_date = info.find("td", attrs={"class": "header"}, text=re.compile("発売日:"))
        released_date = str(released_date.next_sibling.next_sibling.next_element)
    return released_date


def find_library_movie_length(info):
    movie_length = ""
    if info.find("td", attrs={'class': 'header'}, text=re.compile("収録時間:")):
        movie_length = info.find("td", attrs={"class": "header"}, text=re.compile("収録時間:"))
        movie_length = str(movie_length.next_sibling.next_sibling.next_element.next_element)
    return movie_length


def find_library_company(info, language):
    company = ""
    if info.find("td", attrs={'class': 'header'}, text=re.compile("{}".format(language))):
        company = info.find("td", attrs={"class": "header"}, text=re.compile("{}".format(language)))
        company = str(company.next_sibling.next_sibling.next_element.next_element.next_element)
    return company


def find_library_series_description(info):
    series_description = ""
    if info.find("td", attrs={'class': 'header'}, text=re.compile("レーベル:")):
        series_description = info.find("td", attrs={"class": "header"}, text=re.compile("レーベル:"))
        series_description = str(series_description.next_sibling.next_sibling.next_element.next_element.next_element)
    return series_description


def find_library_star(movie_text):
    star_list = ""
    if movie_text.find_all("span", {"class": "star"}):
        star_list = []
        stars = movie_text.find_all("span", {"class": "star"})
        for star in stars:
            if star:
                star = star.text
                if star.find("（") != -1:
                    star = star.split("（")[0]
                star_list.append(star)
    return star_list


def find_library_genres(movie_text):
    genre_list = ""
    if movie_text.find_all("a", {"rel": "category tag"}, href=re.compile("genre")):
        genre_list = []
        genres = movie_text.find_all("a", {"rel": "category tag"}, href=re.compile("genre"))
        for genre in genres:
            if genre:
                genre = str(genre.text)
                # print(genre)
                if genre == "ぶっかけ":
                    continue
                if genre == "レイプ":
                    continue
                if genre == "ランジェリー":
                    continue
                genre = get_genre_type(genre)
                genre_list.append(genre)
    return genre_list


def find_library_search_e(meta, url):
    url_e = url.replace("/ja/", "/en/")
    library_soup_e = parse_library(url_e)
    movie_texts = library_soup_e.find_all("div", {"id": "content"})
    for movie_text in movie_texts:
        company_name_e = find_library_company(movie_text, "Maker:")
        meta['company_name_e'] = company_name_e
        title_e = find_library_title(movie_text)
        meta['title_e'] = title_e
        star_e = find_library_star(movie_text)
        meta['star_e'] = star_e
    return meta


def find_library_search_c(meta, url):
    url_c = url.replace("/ja/", "/cn/")
    library_soup_c = parse_library(url_c)
    movie_texts = library_soup_c.find_all("div", {"id": "content"})
    for movie_text in movie_texts:
        company_name_c = find_library_company(movie_text, "制作商:")
        meta['company_name_c'] = company_name_c
        # title_c = find_library_title(movie_text)
        # meta['title_c'] = title_c
        star_c = find_library_star(movie_text)
        meta['star_c'] = star_c

    return meta


def javlibrary_search(meta_library, code, return_dict):
    print("\n-----------------searching javlibrary-----------------\n")
    # jav_lock.acquire()
    url = 'http://www.javlibrary.com/ja/vl_searchbyid.php?keyword=' + code
    library_soup = parse_library(url)
    if library_soup is None:
        # meta_all.put("")
        # return_dict['javlibrary'] = meta_library
        return meta_library
    if check_next_page(library_soup):
        url = get_new_url(library_soup)
        library_soup = parse_library(url)
    if library_soup is None:
        return None
    movie_texts = library_soup.find_all("div", {"id": "content"})
    for movie_text in movie_texts:
        title_library = find_library_title(movie_text)
        movie_sample_video_poster_library = find_library_image(movie_text)
        code_library = find_library_code(movie_text)
        released_date_library = find_library_released_date(movie_text)
        movie_length_library = find_library_movie_length(movie_text)
        company_library = find_library_company(movie_text, "メーカー:")
        series_description_library = find_library_series_description(movie_text)
        stars_library = find_library_star(movie_text)
        genres = find_library_genres(movie_text)
        meta_library['title'] = title_library
        meta_library['movie_sample_video_poster'] = movie_sample_video_poster_library
        meta_library['code'] = code_library
        meta_library['released_date'] = released_date_library
        meta_library['movie_length'] = movie_length_library
        meta_library['company'] = company_library
        meta_library['series_description'] = series_description_library
        meta_library['star_j'] = stars_library
        meta_library['genres'] = genres

        # print(genres)
    meta_library = find_library_search_e(meta_library, url)
    meta_library = find_library_search_c(meta_library, url)
    # print(library_soup)
    # meta_all.put(meta_library)
    return_dict['javlibrary'] = meta_library
    print('\n-----------------search done for javlibrary-----------------\n')
    # jav_meta['javlibrary'] = meta
    return
    # jav_lock.release()


if __name__ == '__main__':
    os.chdir(r'C:\Users\NoMoneyForAlienWare\Desktop\project_devl')
    return_dict_test = {}
    meta_library_test = empty_dict()
    code_test = "LULU-010"
    javlibrary_search(meta_library_test, code_test, return_dict_test)
    print(return_dict_test)

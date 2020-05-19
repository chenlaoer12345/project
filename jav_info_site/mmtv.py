from hanziconv import HanziConv
from setting import *
from selenium import webdriver
import os
import time
import requests
from bs4 import BeautifulSoup
import re
from hanziconv import HanziConv

mmtv_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-length": "11",
    "content-type": "application/x-www-form-urlencoded",
    "referer": "https://7mmtv.tv/zh/searchform_search/all/index.html",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                  "537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36}",
}


def open_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=Default')
    # options.add_argument('--incognito')
    options.add_argument('--disable-plugins-discovery')
    options.add_argument('--start-maximized')
    options.add_argument('headless')
    chrome_path = os.getcwd()
    driver = webdriver.Chrome(chrome_path + r'\chromedriver.exe', options=options)
    return driver


def mmtv_search(driver, meta_mm, code, return_dict, av_type=1):
    if av_type == 1:
        meta_mm['type'] = "有码"
        meta_mm['type_e'] = "Censored"
        driver_search = mmtv_search_criteria(driver, code, "censored")
        if driver_search is None:
            driver_search2 = mmtv_search_criteria(driver, code, "amateurjav")
            if driver_search2 is None:
                return None
            else:
                parse_mmtv_page_info(driver=driver_search2, meta_mm=meta_mm, return_dict=return_dict, av_type=av_type)
        else:
            parse_mmtv_page_info(driver=driver_search, meta_mm=meta_mm, return_dict=return_dict, av_type=av_type)
    if av_type == 2:
        meta_mm['type'] = "无码"
        meta_mm['type_e'] = "Uncensored"
        driver_search = mmtv_search_criteria(driver, code, "uncensored")
        if driver_search is not None:
            parse_mmtv_page_info(driver=driver_search, meta_mm=meta_mm, return_dict=return_dict, av_type=av_type)
        else:
            code = mmtv_code_modifier(code)
            driver_search2 = mmtv_search_criteria(driver, code, "uncensored")
            if driver_search2 is not None:
                parse_mmtv_page_info(driver=driver_search2, meta_mm=meta_mm, return_dict=return_dict, av_type=av_type)
    return return_dict

def mmtv_code_modifier(code):
    if "-" in code:
        code = code.replace("-", "_")
    else:
        code = code.replace("_", "-")
    return code

def parse_mmtv_page_info_e(driver, meta_mm):
    url_e = driver.current_url
    url_e = url_e.replace("/zh/", "/en/")
    driver.get(url_e)
    soup = driver.page_source
    soup = BeautifulSoup(soup, "lxml")
    meta_mm['title_e'] = mmtv_title(soup)
    mmtv_company_e(soup, meta_mm)
    # meta_mm['star_e'] = mmtv_stars(soup)
    pass


def parse_mmtv_page_info(driver, meta_mm, return_dict, av_type=1):
    soup = driver.page_source
    soup = BeautifulSoup(soup, "lxml")
    meta_mm['title'] = mmtv_title(soup)
    meta_mm['movie_sample_video_poster'] = mmtv_sample_image_poster(soup)
    meta_mm['movie_sample_img'] = mmtv_movie_sample_img(soup)
    if av_type == 2:
        meta_mm['movie_small_sample_img'] = meta_mm['movie_sample_video_poster']
    mmtv_code_date_length_company(soup, meta_mm)
    meta_mm['genres'] = mmtv_genre(soup)
    meta_mm['star_j'] = mmtv_stars(soup)
    parse_mmtv_page_info_e(driver, meta_mm)
    return_dict['7mmtv'] = meta_mm
    return return_dict


def mmtv_genre(soup):
    genres = ""
    if soup.find("span", {"class": "posts-inner-details-text-under"}):
        soup = soup.find("span", {"class": "posts-inner-details-text-under"})
        genres_mmtv = soup.find_all("span")
        genres = []
        for genre in genres_mmtv:
            genre = HanziConv.toSimplified(str(genre.text))
            genre = get_genre_type(genre)
            genres.append(genre)
    return genres


def mmtv_stars(soup):
    if soup.find("div", {"class": "actor-right-part"}):
        soup = soup.find("div", {"class": "actor-right-part"})
        stars_j = []
        stars_names = soup.find_all("p")
        for star in stars_names:
            star = str(star.text).split("(")[0]
            star = star.split("（")[0]
            if star == "素人":
                continue
            if star == "amateur":
                continue
            stars_j.append(star)
        if len(stars_j) == 0:
            return ""
        return stars_j


def mmtv_company_e(soup, meta_mm):
    if soup.find("div", {"class": "posts-inner-details-text-top"}):
        soup = soup.find_all("span", {"class": "posts-inner-details-text-left"})
        for text in soup:
            if text.find("li", text=re.compile("Studio:")):
                company = text.find("li", text=re.compile("Studio:")).next_sibling.next_sibling
                company = str(company.text)
                meta_mm['company_name_e'] = company
    return meta_mm


def get_min(time_str):
    try:
        h, m, s = time_str.split(':')
    except ValueError:
        m, s = time_str.split(":")
        return int(m)
    return int(h) * 60 + int(m)


def mmtv_code_date_length_company(soup, meta_mm):
    if soup.find("div", {"class": "posts-inner-details-text-top"}):
        soup = soup.find_all("span", {"class": "posts-inner-details-text-left"})
        for text in soup:
            if text.find("li", text=re.compile("番號:")):
                code = text.find("li", text=re.compile("番號:")).next_sibling.next_sibling
                code = str(code.text)
                meta_mm['code'] = code
            if text.find("li", text=re.compile("發行日期:")):
                released_date = text.find("li", text=re.compile("發行日期:")).next_sibling.next_sibling
                released_date = str(released_date.text)
                meta_mm['released_date'] = released_date
            if text.find("li", text=re.compile("影片時長:")):
                movie_length = text.find("li", text=re.compile("影片時長:")).next_sibling.next_sibling
                movie_length = str(movie_length.text)
                movie_length = movie_length.split('分')[0]
                if "min" in movie_length:
                    movie_length = movie_length.split("min")[0]
                if ":" in movie_length:
                    movie_length = str(get_min(movie_length))
                meta_mm['movie_length'] = movie_length
            if text.find("li", text=re.compile("製作商:")):
                company = text.find("li", text=re.compile("製作商:")).next_sibling.next_sibling
                company = str(company.text)
                meta_mm['company'] = company
    return meta_mm


def mmtv_sample_image_poster(soup):
    movie_sample_video_poster = ""
    if soup.find("div", {"class": "post-inner-details-img"}):
        movie_sample_video_poster = soup.find("div", {"class": "post-inner-details-img"}).find("img")['src']
        movie_sample_video_poster = str(movie_sample_video_poster)
        response = requests.get(movie_sample_video_poster)
        if response == 404:
            return ""
    return movie_sample_video_poster


def mmtv_movie_sample_img(soup):
    movie_sample_img = ""
    if soup.find("div", {"class": "video-introduction-images-list-row"}):
        movie_sample_img = []
        movie_sample_img_s = soup.find("div", {"class": "video-introduction-images-list-row"})
        movie_sample_img_all = movie_sample_img_s.find_all("li")
        for img in movie_sample_img_all:
            if img.find('img'):
                img_url = img.find('img')['src']
                if img_url == r"http://pic.javbooks.com/amateur/thumbnail_b/":
                    continue
                else:
                    movie_sample_img.append(img_url)
        if not movie_sample_img:
            return ""
    return movie_sample_img


def mmtv_title(soup):
    title = ""
    if soup.find("div", {"class": "post-inner-details-heading"}):
        title = soup.find("div", {"class": "post-inner-details-heading"}).find("h2").text
        title = str(title)
        title = title.split(']')[1]
    return title


def mmtv_search_criteria(driver, code, search_type):
    num = 1
    url = r"https://7mmtv.tv/zh/{}_search/all/{}/{}.html".format(search_type, code, num)
    while True:
        driver.get(url)
        movie_url = check_code_match(driver=driver, code=code)
        if movie_url:
            driver.get(movie_url)
            return driver
        num += 1
        url = check_page_num(driver)
        if url is None:
            break
    return None


def check_page_num(driver):
    soup = driver.page_source
    soup = BeautifulSoup(soup, "lxml")
    soup = soup.find_all("li", {"class": "page-item previous-next"})
    for stuff in soup:
        if stuff.find("i", {"class": "fa fa-angle-right"}):
            next_page = stuff.find('a')['href']
            return next_page
    return None


def check_code_match(driver, code):
    soup = driver.page_source
    soup = BeautifulSoup(soup, "lxml")
    soup = soup.find_all("div", {"class": "latest-korean-box-text"})
    if len(soup) == 0:
        return False
    for stuff in soup:
        if stuff.find("a"):
            movie_url = stuff.find("a")['href']
            driver.get(movie_url)
            soup_2 = BeautifulSoup(driver.page_source, "lxml")
            if soup_2.find("div", {"class": "posts-inner-details-text-top"}):
                soup_2 = soup_2.find_all("span", {"class": "posts-inner-details-text-left"})
                for text in soup_2:
                    if text.find("li", text=re.compile("番號:")):
                        code_match = text.find("li", text=re.compile("番號:")).next_sibling.next_sibling
                        code_match = str(code_match.text)
                        if mmtv_check_code_ways(code, code_match):
                            return driver.current_url
            driver.back()
        # code_match = stuff.find('h2').text
        # print(code_match)
        # code_match = str(code_match)
        # code_match = code_match.split("]")[0][1:]
        # code_match = code_match.split()
        # print(code_match)
        # for cod_match in code_match:
        #     if mmtv_check_code_ways(code_input=code, code_match=cod_match):
        #         url = stuff.find("a")['href']
        #         return url
    return False

def mmtv_check_code_ways(code_input, code_match):
    if code_input == code_match.upper() or code_input == code_match.lower():
        return True
    code_input = code_input.replace("_", "-")
    if code_input == code_match.upper() or code_input == code_match.lower():
        return True
    return False

def mmtv_check_content(response):
    if response.find('li', {'class': 'page-item current'}):
        return response
    else:
        return None


def mmtv_search_av(code, av_type, meta_mm, return_dict):
    print("-----------------searching 7mmtv-----------------")
    driver = open_driver()
    return_dict = mmtv_search(driver=driver, code=code, av_type=av_type, meta_mm=meta_mm, return_dict=return_dict)
    driver.close()
    print("-----------------search done for 7mmtv-----------------")
    return return_dict


if __name__ == '__main__':
    os.chdir(r"C:\Users\NoMoneyForAlienWare\Desktop\project_devl")
    driver_test = open_driver()
    code_test = "SIRO-3183"
    meta_test = empty_dict()
    return_dict_test = {}
    return_dict_test = mmtv_search(driver=driver_test, code=code_test, av_type=1, meta_mm=meta_test,
                                   return_dict=return_dict_test)
    print(return_dict_test)
    driver_test.close()

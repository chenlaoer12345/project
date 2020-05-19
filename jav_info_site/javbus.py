# from bs4 import BeautifulSoup
from setting import *
import re
from selenium import webdriver
import os

# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1200x600')
bus_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
              "q=0.8,application/signed-exchange;v=b3",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9,ja;q=0.8,zh-CN;q=0.7,zh;q=0.6",
    "cache-control": "max-age=0",
    "referer": "https://www.javbus.com/",
    # "host": "www.javlibrary.com",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                  "537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36}",
}

# def bus_check_type(meta, soup, code):
#     if soup is None:
#         print("检查影片是否无码.....")
#         url = "https://www.javbus.com/uncensored/search/" + code + "&type=1"
#         soup = parse_url(url, bus_headers)
#         if soup is None:
#             print("在javbus找不到影片")
#             return None
#         print("影片为无码")
#         meta['type'] = '无码'
#         meta['type_e'] = 'Uncensored'
#         return soup
#     meta['type'] = '有码'
#     meta['type_e'] = 'Censored'
#     return soup


def bus_find_small_cover_image(meta, soup, code):
    if soup.find("div", {"class": 'photo-frame'}):
        # movie_small_sample_img = str(soup.find("div", {"class": 'photo-frame'}).find("img")['src'])
        # meta['movie_small_sample_img'] = movie_small_sample_img
        url = soup.find_all("a", {'class': 'movie-box', 'href': re.compile('www.javbus.com')})
        for ur in url:
            if ur.find("div", {'class': 'photo-info'}).find('date'):
                if ur.find("div", {'class': 'photo-info'}).find('date').text == code.upper():
                    movie_small_sample_img = ur.find('div', {'class': 'photo-frame'}).find('img')['src']
                    meta['movie_small_sample_img'] = movie_small_sample_img
                    new_url = ur['href']
                    return new_url
        return "https://www.javbus.com/" + code
    else:
        return None
    # return https://www.javbus.com/GS-013


# def javbus_chrome_parse(url):
#     current_di = os.getcwd()
#     driver = webdriver.Chrome(current_di + r'\chromedriver.exe', options=options)
#     driver.get(url)
#     #    time.sleep(1)
#     data = driver.page_source
#     # time.sleep(1000)
#     driver.close()
#     soup = BeautifulSoup(data, "lxml")
#     return soup


def bus_find_title(soup):
    title = ""
    if soup.find("a", {"class": "bigImage"}):
        title_elem = soup.find("a", {"class": "bigImage"})
        title = title_elem.find("img")['title']
    return title


def bus_find_movie_sample_poster(soup):
    movie_sample_img = ""
    if soup.find("a", {"class": "bigImage"}):
        title_elem = soup.find("a", {"class": "bigImage"})
        movie_sample_img = title_elem.find("img")['src']
    return movie_sample_img


def bus_find_code(t):
    code = ""
    if t.find("span", {'class': 'header'}, text=re.compile('識別碼:')):
        code = str(t.find("span", {'style': 'color:#CC0000;'}).text)
    return code


def bus_find_released_date(t):
    released_date = ""
    if t.find("span", {'class': 'header'}, text=re.compile('發行日期:')):
        released_date = t.find("span", {'class': 'header'}, text=re.compile('發行日期:'))
        released_date = str(released_date.next_sibling).strip()
    return released_date


def bus_find_movie_length(t):
    movie_length = ""
    if t.find("span", {'class': 'header'}, text=re.compile('長度:')):
        movie_length = t.find("span", {'class': 'header'}, text=re.compile('長度:'))
        movie_length = str(movie_length.next_sibling).strip().split('分鐘')[0]
    return movie_length


def bus_find_company(t):
    company = ""
    if t.find("span", {'class': 'header'}, text=re.compile('製作商:')):
        company = t.find("span", {'class': 'header'}, text=re.compile('製作商:'))
        company = str(company.next_sibling.next_sibling.text).strip()
    return company


def bus_find_series_description(t):
    series_description = ""
    if t.find("span", {'class': 'header'}, text=re.compile('發行商:')):
        series_description = t.find("span", {'class': 'header'}, text=re.compile('發行商:'))
        series_description = str(series_description.next_sibling.next_sibling.text).strip()
    return series_description


def bus_find_genres(t):
    genre_list = ""
    if t.find("span", {'class': 'genre'}):
        genres = t.find_all('span', {'class': 'genre'})
        genre_list = []
        for genre_t in genres:
            if genre_t.find("a", {'href': re.compile('/genre/')}):
                genre = genre_t.find("a", {'href': re.compile('/genre/')})
                genre = str(genre.text)
                genre = get_genre_type(genre)
                genre_list.append(genre)
    return genre_list


def bus_find_stars(t):
    star_list = ""
    if t.find('span', {'class': 'genre'}):
        star_list = []
        genres = t.find_all('span', {'class': 'genre'})
        for genre_t in genres:
            if genre_t.find("a", {'href': re.compile('/star/')}):
                star = genre_t.find('a', {'href': re.compile('/star/')})
                star = str(star.text.strip())
                star_list.append(star)
    return star_list


def bus_find_performer_cover_image_url(soup):
    performer_cover_image_url = ""
    if soup.find("div", {'id': 'avatar-waterfall'}).find('a', {'class': 'avatar-box'}):
        star_list = {}
        star_texts = soup.find_all("a", {'class': 'avatar-box'})
        for s in star_texts:
            star_url = s.find('img')['src']
            star_name = s.find('img')['title']
            star_list[star_name] = star_url
        performer_cover_image_url = star_list
    return performer_cover_image_url


# def bus_find_magnet_link(soup):
#     magnet_dict = ""
#     if soup.find("table", {'id': 'magnet-table'}).find("tr", {
#         'onmouseover': "this.style.backgroundColor='#F4F9FD';this.style.cursor='pointer';"}):
#         texts = soup.find("table", {'id': 'magnet-table'}).find_all("tr", {
#             'onmouseover': "this.style.backgroundColor='#F4F9FD';this.style.cursor='pointer';"})
#         magnet_dict = {}
#         for magnet in texts:
#             magnet_table = []
#             ma = magnet.find_all('a')
#             magnet_link = magnet.find("td", {'width': '70%'}).find('a')['href'].split('&dn=')[0]
#             counter = 1
#             for a in ma:
#                 magnet_stuff = dict()
#                 magnet_name = str(a.text).strip()
#                 if magnet_name == '高清':
#                     magnet_stuff['高清'] = 'True'
#                     magnet_table.append(magnet_stuff)
#                     continue
#                 if magnet_name == '字幕':
#                     magnet_stuff['字幕'] = 'True'
#                     magnet_table.append(magnet_stuff)
#                     continue
#                 magnet_stuff[str(counter)] = magnet_name
#                 counter += 1
#                 magnet_table.append(magnet_stuff)
#             magnet_dict[magnet_link] = magnet_table
#     return magnet_dict


def bus_find_movie_sample_img(soup):
    movie_sample_img = ""
    if soup.find('div', {'id': 'sample-waterfall'}):
        samples = soup.find('div', {'id': 'sample-waterfall'}).find_all('a', {'class': 'sample-box'})
        movie_sample_img = []
        for sample in samples:
            img = sample['href']
            movie_sample_img.append(img)
    return movie_sample_img


def javbus_search(meta_bus, code, return_dict, wuma=0):
    # jav_lock.acquire()
    print("\n-----------------searching javbus-----------------\n")
    if wuma == 0:
        url = "https://www.javbus.com/search/" + code + "&type=&parent=ce"
        soup = parse_url(url, bus_headers)
        if soup is None:
            return None
        meta_bus['type'] = '有码'
        meta_bus['type_e'] = 'Censored'
    else:
        url = "https://www.javbus.com/uncensored/search/" + code + "&type=1"
        soup = parse_url(url, bus_headers)
        if soup is None:
            return None
        meta_bus['type'] = '无码'
        meta_bus['type_e'] = 'Uncensored'
    bus_url = bus_find_small_cover_image(meta_bus, soup, code)
    soup = parse_url(bus_url, bus_headers)
    texts = soup.find_all("div", {'class': 'col-md-3'})
    if soup.find("div", {'id': 'avatar-waterfall'}) is None:
        # meta_all.put("")
        return_dict['javbus'] = meta_bus
        return None
    for t in texts:
        code_bus = bus_find_code(t)
        released_date_bus = bus_find_released_date(t)
        movie_length_bus = bus_find_movie_length(t)
        company_bus = bus_find_company(t)
        series_description_bus = bus_find_series_description(t)
        genres_bus = bus_find_genres(t)
        stars_bus = bus_find_stars(t)
    performer_cover_image_url_bus = bus_find_performer_cover_image_url(soup)
    # magnet_dict_bus = bus_find_magnet_link(soup)
    movie_sample_img_bus = bus_find_movie_sample_img(soup)
    title_bus = bus_find_title(soup)
    movie_sample_video_poster_bus = bus_find_movie_sample_poster(soup)
    meta_bus['code'] = code_bus
    meta_bus['released_date'] = released_date_bus
    meta_bus['movie_length'] = movie_length_bus
    meta_bus['company'] = company_bus
    meta_bus['series_description'] = series_description_bus
    meta_bus['genres'] = genres_bus
    meta_bus['star_j'] = stars_bus
    meta_bus['performer_cover_image_url'] = performer_cover_image_url_bus
    # meta_bus['magnet_dict'] = magnet_dict_bus
    meta_bus['movie_sample_img'] = movie_sample_img_bus
    meta_bus['title'] = title_bus
    meta_bus['movie_sample_video_poster'] = movie_sample_video_poster_bus
    print('\n-----------------search done for javbus-----------------\n')
    # meta_all.put(meta_bus)
    return_dict['javbus'] = meta_bus
    # jav_lock.release()
    return


if __name__ == '__main__':
    os.chdir(r"C:\Users\NoMoneyForAlienWare\Desktop\project")
    test_dict = {}
    meta_bus_test = empty_dict()
    code_test = "SIRO-3183"
    javbus_search(meta_bus_test, code_test, test_dict, 1)
    print(test_dict)


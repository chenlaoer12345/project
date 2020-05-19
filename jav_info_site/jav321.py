from setting import *
import re
import requests

jav321_headers = {
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9,ja;q=0.8,zh-CN;q=0.7,zh;q=0.6",
    "cache-control": "max-age=0",
    "content-length": "11",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.jav321.com",
    "referer": "https://www.jav321.com/search",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                  "537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36}",
}


def post_parse_url(url, data):
    """using post method get html data from jav321
       return 0 if video not found
       :rtype: xpath if video found
               none if not found
    """
    page_321 = requests.post(url, data=data, headers=jav321_headers).content.decode()
    return page_321


def check_video_321(content):
    """check if video exist in jav321"""
    check = content.xpath('//html/body/div[2]/div/div/@class')[0]
    if check == 'alert alert-danger':
        print("can't find video in jav321 \n")
        return 0
    return content


def find_star(page_321):
    """find all jav321 star
       input: request decode object
       return: list of star names if exist
               empty if not
    """
    stars = page_321.xpath('//html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/a[contains(@href,"star")]/text()')
    if not stars:
        stars = ""
    else:
        star_set = set()
        for star in stars:
            star_set.add(star)
        stars = []
        for star in star_set:
            stars.append(star)
    return stars


def find_title(lxml_page_321):
    """find jav321 title
       input: xpath selector
       return: title as str
               empty if not
    """
    title = str(lxml_page_321.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/h3/text()')[0])
    if not title:
        title = ""
    return title


def find_company(lxml_page_321):
    """find jav321 company
       input: xpath selector
       return: company as str
               empty if not
    """
    company = str(lxml_page_321.xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/a'
                                      '[contains(@href,"company")]/text()')[0])
    if not company:
        company = ""
    return company


def find_genre(lxml_page_321):
    """find jav321 genres
       input: xpath selector
       return: genres as list
    """
    genres = lxml_page_321.xpath(
        '/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/a[contains(@href,"genre")]/text()')
    if not genres:
        return ""
    genre_list = []
    for genre in genres:
        genre = get_genre_type(genre)
        genre_list.append(genre)
    return genre_list


def find_release_date(page_321):
    """find jav321 released date
       input: request decode object
       return: released date as str
    """
    released_date = str(re.search('发行日期</b>(.*?)<', page_321, re.S).group(1))
    if not released_date:
        return ""
    return released_date.split(":")[1].strip()


def find_time(page_321):
    """find jav321 movie time
       input: request decode object
       return: movie time as str
    """
    movie_time = str(re.search('播放时长</b>(.*?)<', page_321, re.S).group(1)).split(":")
    if not movie_time:
        return ""
    return movie_time[1].split()[0]


def find_small_sample_image(lxml_page_321):
    """find jav321 small sample image
       input: xpath selector
       return: small sample image url as str
    """
    small_sample_image = str(lxml_page_321.xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/img/@src')[0])
    if not small_sample_image:
        return ""
    response = requests.get(small_sample_image)
    if response.status_code == 404:
        return ""
    return small_sample_image


def find_movie_poster(lxml_page_321):
    """find jav321 movie poster
       input: xpath selector
       return: movie poster url as str
    """
    poster = lxml_page_321.xpath('/html/body/div[2]/div[2]/div[1]/p/a/img/@src')
    if "-001.jpg" in poster:
        poster = str(lxml_page_321.xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/img/@src')[0])
    if not poster:
        return ""
    response = requests.get(poster[0])
    if response.status_code == 404:
        return ""
    return str(poster[0])


def find_sample_movie(lxml_page_321):
    """find jav321 sample movie url
       input: xpath selector
       return: movie url as str
    """
    sample_movie = lxml_page_321.xpath('//*[@class="video-js vjs-default-skin vjs-big-play-centered"]/source/@src')
    if not sample_movie:
        return ""
    return sample_movie[0]


def find_sample_images(lxml_page_321):
    """find jav321 sample images
       input: xpath selector
       return: sample images as list
    """
    sample_images = lxml_page_321.xpath('/html/body/div[2]/div[2]/div[*]/p/a/img/@src')
    # cut first image if it is cover image
    if "-001.jpg" not in sample_images[0]:
        sample_images = sample_images[1:]
    if not sample_images:
        return ""
    for a in sample_images:
        num = 0
        response = requests.get(a)
        if response.status_code == 404:
            sample_images.pop(num)
        num += 1
    if not sample_images:
        return ""
    return sample_images


def find_code(page_321):
    """find jav321 codemovie_small_sample_img
       input: request decode object
       return: code as str
    """
    code_321 = str(re.search('番号</b>(.*?)<', page_321, re.S).group(1)).split(":")
    if not code_321:
        return ""
    return code_321[1].strip()


def find_series(lxml_page_321):
    """find jav321 sample images
           input: xpath selector
           return: series as str
    """
    series = lxml_page_321.xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/'
                                 '/a[contains(@href, "series")]/text()')
    if not series:
        return ""
    return series[0]


def star_cover_image(lxml_page_321, stars):
    """find jav321 star cover image
       input: xpath selector
              stars list
       return: star dictionary with star as key, cover image as value
    """
    if len(stars) == 0:
        return stars
    stars_cover = {}
    for star in stars:
        print(star)
        stars_cover[star] = lxml_page_321.xpath('//html/body/div[2]/div[1]/div[*]/div[2]/div[1]/div/div[1]/div'
                                                '/a[text() = "{}"]/img/@src'.format(star))
        if not stars_cover[star]:
            stars_cover = ""
        else:
            stars_cover[star] = stars_cover[star][0]
    return stars_cover


def jav321_search(meta_321, code, return_dict):
    """search jav321 website info"""
    # jav_lock.acquire()
    url = "https://www.jav321.com/search"
    data = {"sn": code}
    print('\n-----------------searching jav321-----------------\n')
    page_321 = post_parse_url(url, data)
    if page_321 is None:
        return_dict['jav321'] = meta_321
        print("\n-----------------code not found in this website-----------------------\n")
        return meta_321
    lxml_page_321 = lxml_page(page_321)
    lxml_page_321 = check_video_321(lxml_page_321)
    if lxml_page_321 == 0:
        # meta_all.put("")
        return_dict['jav321'] = meta_321
        return None
    code_321 = find_code(page_321)
    series_321 = find_series(lxml_page_321)
    stars_321 = find_star(lxml_page_321)
    title_321 = find_title(lxml_page_321)
    company_321 = find_company(lxml_page_321)
    genres_321 = find_genre(lxml_page_321)
    released_date_321 = find_release_date(page_321)
    movie_length_321 = find_time(page_321)
    movie_small_sample_img_321 = find_small_sample_image(lxml_page_321)
    movie_sample_video_poster_321 = find_movie_poster(lxml_page_321)
    movie_sample_video_url_321 = find_sample_movie(lxml_page_321)
    movie_sample_img_321 = find_sample_images(lxml_page_321)
    performer_cover_image_url_321 = star_cover_image(lxml_page_321, find_star(lxml_page_321))
    meta_321['code'] = code_321
    meta_321['series'] = series_321
    meta_321['star_j'] = stars_321
    meta_321['title'] = title_321
    meta_321['company'] = company_321
    meta_321['genres'] = genres_321
    meta_321['released_date'] = released_date_321
    meta_321['movie_length'] = movie_length_321
    meta_321['movie_small_sample_img'] = movie_small_sample_img_321
    meta_321['movie_sample_video_poster'] = movie_sample_video_poster_321
    meta_321['movie_sample_video_url'] = movie_sample_video_url_321
    meta_321['movie_sample_img'] = movie_sample_img_321
    meta_321['performer_cover_image_url'] = performer_cover_image_url_321
    # jav_meta['jav321'] = meta
    # print(meta_321)
    # meta_all.put(meta_321)
    print('\n-----------------search done for jav321-----------------\n')
    # jav_lock.release()
    return_dict['jav321'] = meta_321
    return


if __name__ == '__main__':
    test_dict = {}
    meta_321_test = empty_dict()
    code_test = "ipx-493"
    jav321_search(meta_321_test, code_test, test_dict)
    print(test_dict)

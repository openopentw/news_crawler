# example url: https://udn.com/news/archive/0/0/2018/05/30

import json
import sys
import time
import urllib.request as request

from bs4 import BeautifulSoup

def get_soup (url, debug_mode=0, debug_outfile='./tmp.html'):
    time.sleep(0.5) # sleep a bit to prevent DOS
    if debug_mode == 0 or debug_mode == 1:
        req = request.Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        req = request.urlopen(req)
        html = req.read()
        soup = BeautifulSoup(html, 'lxml')
        soup = BeautifulSoup(soup.prettify(), 'lxml')
        if debug_mode == 1:
            with open(debug_outfile, 'w', encoding='utf8') as f:
                print(soup.prettify(), file=f)
    elif debug_mode == 2:
        with open(debug_outfile, encoding='utf8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'lxml')
    return soup

def get_total_page (soup):
    total_page = soup.select_one('.total').text.replace('共', '').replace('頁', '').strip()
    return total_page

def get_url_list (soup):
    a_list = soup.select_one('#ranking_table').select('a')
    url_list = []
    for a in a_list:
        url_list += [a['href']]
    return url_list

def get_all_pages (url, debug_print=False):
    soup = get_soup(url)

    total_page = int(get_total_page(soup))
    if debug_print:
        print('total page =', total_page)

    url_list = get_url_list(soup)
    for page in range(2, total_page + 1):
        if debug_print:
            print('page =', page)
        soup = get_soup('{}/{}'.format(url, page))
        url_list += get_url_list(soup)

    return url_list

if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Please give me the output file name.'

    base_url = 'https://udn.com/news/archive/0/0'
    year = 2017
    month_days = [
        [6, 5, 30],
        [7, 1, 31],
        [8, 1, 31],
        [9, 1, 30],
        [10, 1, 31],
        [11, 1, 30],
        [12, 1, 31],
    ]

    year_month_days_news_url = {
        year: {},
    }
    for (month, beg_day, end_day) in month_days:
        print(month, end_day)
        year_month_days_news_url[year][month] = {}
        for day in range(beg_day, end_day + 1):
            print(year, month, day)
            url = '{}/{}/{:02}/{:02}'.format(base_url, year, month, day)
            # print(url)
            url_list = get_all_pages(url)
            # print('len of url =', len(url_list))
            print(url_list)
            year_month_days_news_url[year][month][day] = list(url_list)

    # print outside
    print('outfile =', sys.argv[1])
    with open(sys.argv[1], 'w') as outfile:
        json.dump(year_month_days_news_url, outfile)

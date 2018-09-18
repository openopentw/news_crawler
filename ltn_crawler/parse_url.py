""" This module parse all the url to the news.

Example usage:
    python3 parse_url.py

"""

# example url: http://news.ltn.com.tw/list/newspaper/focus/20180501/2

import json
import time
import urllib.request as request
from urllib.error import URLError, HTTPError
from typing import List, Tuple

from bs4 import BeautifulSoup

def get_html(url: str) -> bytes:
    """ Download html from url and return with html string. """
    time.sleep(0.1) # sleep a bit to prevent DOS

    req = request.Request(
        url,
        headers={
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)'
                           'AppleWebKit/537.36 (KHTML, like Gecko)'
                           'Chrome/35.0.1916.47 Safari/537.36')
        }
    )
    req = request.urlopen(req)
    html = req.read()

    return html

def get_url_list_page_topic(date: List[str], topic: str, page: int) -> Tuple[List[str], int]:
    """ Get url list by given date / topic / page. """
    url = 'http://news.ltn.com.tw/list/newspaper/{}/{}/{}'.format(
        topic, '{}{:02}{:02}'.format(date[0], date[1], date[2]), page
    )
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    a_list = soup.select_one('.list').select('.tit')
    url_list = ['http://news.ltn.com.tw/{}'.format(a['href']) for a in a_list]

    max_page = 1
    pagination = soup.select_one('.pagination')
    if pagination:
        max_page = len(pagination.select('a')) - 2

    return url_list, max_page

def get_url_list_topic(date: List[str], topic: str) -> List[str]:
    """ Get url list by given date / topic. """

    url_list, max_page = get_url_list_page_topic(date, topic, 1)
    for page in range(2, max_page + 1):
        new_url_list, _ = get_url_list_page_topic(date, topic, page)
        url_list += new_url_list

    return url_list

def get_url_list(date: List[str]) -> List[str]:
    """ Get url list by given date. """
    topic_list = [
        'focus',
        'politics',
        'society',
        'local',
        'life',
        'opinion',
        'world',
        'business',
        'sports',
        'entertainment',
        'consumer',
        'supplement',
    ]

    url_list = []
    for topic in topic_list:
        url_list += get_url_list_topic(date, topic)

    return url_list

def main():
    """ Main function. """
    years = list(range(2017, 2005 - 1, -1))
    months = list(range(1, 12 + 1))
    days = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }

    for year in years:
        print('Year:', year)
        year_url_list = {}
        for month in months:
            print('Month:', month)
            year_url_list[month] = {}
            for day in range(1, days[month] + 1):
                print('Year, Month, Day:', year, month, day, end='')
                try:
                    year_url_list[month][day] = get_url_list([year, month, day])
                    print(' ', 'len:', len(year_url_list[month][day]))
                except HTTPError as error:
                    print('')
                    print('Error code: ', error.code)
                    with open('./error_msg.txt', 'a') as errfile:
                        print('Year, Month, Day:', year, month, day, file=errfile)
                        print('Error code: ', error.code, file=errfile)
                except URLError as error:
                    print('')
                    print('Reason: ', error.reason)
                    with open('./error_msg.txt', 'a') as errfile:
                        print('Year, Month, Day:', year, month, day, file=errfile)
                        print('Reason: ', error.reason)

        with open('content_{}.json'.format(year), 'w', encoding='utf8') as outfile:
            json.dump(year_url_list, outfile)

if __name__ == '__main__':
    main()

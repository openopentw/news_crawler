""" This module parse all the url to the news.

Example usage:
    python3 parse_url.py

"""

# example url: 'https://news.tvbs.com.tw/realtime/2018-7-1'
# example url: ('https://news.tvbs.com.tw/news/LoadMoreOverview_realtime'
#               '?showdate=2018-07-01&newsoffset=90&ttalkoffset=0&'
#               'liveoffset=0&nowtime=2018-07-02 00:57:00')

import json
import time
import urllib.request as request

from urllib.error import URLError, HTTPError

from bs4 import BeautifulSoup

def get_html(url):
    """ Download html from url and return with html string. """
    time.sleep(0.5) # sleep a bit to prevent DOS

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

def get_nums(soup):
    """ Get counts from given soup and return. """
    total_num = int(soup.select_one('#total_num')['value'])
    news_count = int(soup.select_one('#news_count')['value'])
    ttalk_count = int(soup.select_one('#ttalk_count')['value'])
    live_count = int(soup.select_one('#live_count')['value'])
    return total_num, (news_count, ttalk_count, live_count)

def get_list_soup(year, month, day, news_offset):
    """ Get urls by given offset. """
    url = ('https://news.tvbs.com.tw/news/LoadMoreOverview_realtime'
           '?showdate={}-{}-{}&newsoffset={}&ttalkoffset=0&liveoffset=0&'
           'nowtime=2018-07-02 00:57:00').format(year, month, day, news_offset)
    raw = get_html(url)
    tmp_dic = json.loads(raw)

    news_count = int(tmp_dic['news_count'])
    ttalk_count = int(tmp_dic['ttalk_count'])
    live_count = int(tmp_dic['live_count'])

    html = tmp_dic['add_li']
    soup = BeautifulSoup(html, 'lxml')

    a_list = soup.select('a')
    url_list = [a['href'] for a in a_list]
    return url_list, (news_count, ttalk_count, live_count)

def get_list(year, month, day):
    """ Get url list by given year/month/day. """
    url = ('https://news.tvbs.com.tw/realtime/'
           '{}-{}-{}'.format(year, month, day))
    soup = BeautifulSoup(get_html(url), 'lxml')
    total_num, (news_count, ttalk_count, live_count) = get_nums(soup)

    ul = soup.select_one('#realtime_data') # pylint: disable=invalid-name
    a_list = ul.select('a')
    url_list = [a['href'] for a in a_list]

    curr_cnt = news_count + ttalk_count + live_count
    while total_num > news_count + ttalk_count + live_count:
        new_url_list, (news_count,
                       ttalk_count,
                       live_count) = get_list_soup(year, month, day, curr_cnt)
        url_list += new_url_list
        curr_cnt += news_count + ttalk_count + live_count

    base_url = 'https://news.tvbs.com.tw'
    url_list = [base_url + url for url in url_list]
    return url_list

def main():
    """ main function. """
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
                    year_url_list[month][day] = get_list(year, month, day)
                    print(' ', 'len:', len(year_url_list[month][day]))
                except HTTPError as error:
                    print('')
                    print('Error code: ', error.code)
                except URLError as error:
                    print('')
                    print('Reason: ', error.reason)

        with open('content_{}.json'.format(year), 'w',
                  encoding='utf8') as outfile:
            json.dump(year_url_list, outfile)

if __name__ == '__main__':
    main()

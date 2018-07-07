""" This module parse all the url to the news.

Example usage:

"""

# example url: 'https://news.tvbs.com.tw/entertainment/561333'

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

def get_header(soup):
    """ Get the title string from given soup. """
    header_soup = soup.select_one('div.title')
    title = header_soup.select_one('h1').text.strip()
    author = header_soup.select_one('h4').text.strip()
    date = header_soup.select_one('div.time').text.strip()
    return title, author, date

def get_content(soup):
    """ Get the article content from given soup. """
    article_soup = soup.select_one('#news_detail_div')
    article = article_soup.get_text('\n')
    sections = article.split('\n')
    sections = [s.strip() for s in sections]
    article = '\n'.join(sections)
    while '\n\n' in article:
        article = article.replace('\n\n', '\n')
    return article.strip()

def get_header_url(url):
    """ Get headers (title, author, date) and article from given url. """
    soup = BeautifulSoup(get_html(url), 'lxml')

    if soup:
        title, author, date = get_header(soup)
        article = get_content(soup)
        return (title, author, date), article
    return ('', '', ''), ''

def main():
    """ Main function. """
    years = list(range(2017, 2005 - 1, -1))

    for year in years:
        content = {}
        with open('urls/url_{}.json'.format(year)) as infile:
            url_list = json.load(infile)
        for month in url_list:
            content[month] = {}
            for day in url_list[month]:
                content[month][day] = []

                print(year, month, day, end=' ', flush=True)
                for url in url_list[month][day]:

                    try:
                        (title, author, date), article = get_header_url(url)
                    except HTTPError as error:
                        print('')
                        print('Error code: ', error.code)
                        with open('error_url.txt', 'a') as errfile:
                            print('Error code: ', error.code, file=errfile)
                            print(url, file=errfile)
                    except URLError as error:
                        print('')
                        print('Reason: ', error.reason)
                        with open('error_url.txt', 'a') as errfile:
                            print('Reason: ', error.reason, file=errfile)
                            print(url, file=errfile)
                    except Exception as error:
                        print('')
                        print('Reason: ', error)
                        with open('error_url.txt', 'a') as errfile:
                            print('Reason: ', error, file=errfile)
                            print(url, file=errfile)

                    if article:
                        content[month][day] += [{
                            'title': title,
                            'date': date,
                            'author': author,
                            'content': article,
                            'url': url,
                        }]

                print(len(content[month][day]))

        with open('contents/content_{}.json'.format(year), 'w', encoding='utf8') as outfile:
            json.dump(content, outfile)

if __name__ == '__main__':
    main()

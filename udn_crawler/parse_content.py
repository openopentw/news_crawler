# example url: https://udn.com/news/story/7317/3169825

import json
import sys
import time
import urllib.request as request

from bs4 import BeautifulSoup

def get_soup (url, debug_mode=0, debug_outfile='./debug_whole.html'):
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
        if debug_mode == 1:
            with open(debug_outfile, 'w', encoding='utf8') as f:
                print(str(soup), file=f)
    elif debug_mode == 2:
        with open(debug_outfile, encoding='utf8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'lxml')
    return soup

def get_content (soup, debug_print=False, debug_outfile='./debug_content.html'):
    content = soup.select_one('#story_body_content')

    if debug_print:
        with open(debug_outfile, 'w', encoding='utf8') as f:
            print(content.prettify(), file=f)

    h1 = content.select_one('h1').text.strip()

    time_and_author = content.select_one('.story_bady_info_author')
    date = time_and_author.select_one('span')
    date_str = date.text.strip()
    date.extract()
    author = time_and_author.text.strip()

    ps = content.select('p')
    articles = []
    for p in ps:
        # remove <figure>
        figures = p.select('figure')
        for figure in figures:
            figure.extract()
        # remove <script>
        scripts = p.select('script')
        for script in scripts:
            script.extract()
        # get all the text
        if p.find(text=True, recursive=False):
            if p.find(text=True, recursive=False).strip():
                articles += [p.text.strip()]
    article = '\n'.join(articles)

    return h1, date_str, author, article

if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Please give me the input file name.'
    assert len(sys.argv) > 2, 'Please give me the output file name.'

    with open(sys.argv[1]) as f:
        url_list = json.load(f)

    # stop_cnt = 0
    # stop = 50

    base_url = 'https://udn.com'
    year_month_days_news_content = {
    }

    for year in url_list:
        year_month_days_news_content[year] = {}
        for month in url_list[year]:
            year_month_days_news_content[year][month] = {}
            for day in url_list[year][month]:
                # skip the downloaded part
                if int(month) == 1 and int(day) <= 25:
                    continue

                year_month_days_news_content[year][month][day] = []
                for partial_url in url_list[year][month][day]:
                    url = '{}{}'.format(base_url, partial_url)
                    print(month, day, url)
                    try:
                        soup = get_soup(url)
                        h1, date, author, article = get_content(soup)
                        year_month_days_news_content[year][month][day] += [{
                            'title': h1,
                            'date': date,
                            'author': author,
                            'content': article,
                            'url': url,
                        }]
                    except:
                        try:
                            with open('./err.log', 'a') as err_file:
                                print('url: ', url, file=err_file)
                        except:
                            pass
                        pass
                    # stop_cnt += 1
                    # if stop_cnt >= stop:
                    #     break
                print('len =', len(year_month_days_news_content[year][month][day]))

                # print outside
                with open(sys.argv[2], 'w') as outfile:
                    json.dump(year_month_days_news_content, outfile)

                # if stop_cnt >= stop:
                    # break
            # if stop_cnt >= stop:
                # break
        # if stop_cnt >= stop:
            # break

    # print outside
    print('outfile =', sys.argv[2])
    # with open(sys.argv[2], 'w') as outfile:
    #     json.dump(year_month_days_news_content, outfile)

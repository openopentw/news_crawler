# example url: https://udn.com/news/archive/0/0/2018/05/30

import json
import sys

if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Please give me the input file name.'

    with open(sys.argv[1]) as f:
        url_list = json.load(f)

    urls = []
    for year in url_list:
        for month in url_list[year]:
            for day in url_list[year][month]:
                urls += url_list[year][month][day]
    print(len(urls))
    print(len(set(urls)))

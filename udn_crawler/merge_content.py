import json
import sys

if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Please give me the bigger input file name.'
    assert len(sys.argv) > 2, 'Please give me the smaller input file name.'
    assert len(sys.argv) > 3, 'Please give me the output file name.'

    with open(sys.argv[1]) as f:
        year_month_days_news_content = json.load(f)

    with open(sys.argv[2]) as f:
        more = json.load(f)

    for day in more['2018']['1']:
        print(day)
        year_month_days_news_content['2018']['1'][day] = more['2018']['1'][day]

    with open(sys.argv[3], 'w') as f:
        json.dump(year_month_days_news_content, f)

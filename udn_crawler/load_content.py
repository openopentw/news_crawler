import json
import sys

if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Please give me the input file name.'

    with open(sys.argv[1]) as f:
        year_month_days_news_content = json.load(f)

    all_true_len = 0
    all_len = 0

    for year in year_month_days_news_content:
        for month in year_month_days_news_content[year]:
            for day in year_month_days_news_content[year][month]:
                true_len = 0
                for c in year_month_days_news_content[year][month][day]:
                    if c['content']:
                        true_len += 1
                if (len(year_month_days_news_content[year][month][day]) > 0):
                    print(year, month, day, true_len / len(year_month_days_news_content[year][month][day]))
                else:
                    print(year, month, day, 'no url')
                all_true_len += true_len
                all_len += len(year_month_days_news_content[year][month][day])

    print('all_true_len =', all_true_len)
    print('all_len =', all_len)

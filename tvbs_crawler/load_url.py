""" This module load the urls in the json files in subfolder urls/

Example usage:

"""

import json

def main():
    """ Main function. """
    years = list(range(2017, 2005 - 1, -1))

    tot_len = 0

    for year in years:
        with open('urls/url_{}.json'.format(year)) as infile:
            url_list = json.load(infile)
        year_len = 0
        for month in url_list:
            for day in url_list[month]:
                year_len += len(url_list[month][day])
        print(year, year_len)
        tot_len += year_len

    print('Total length:', tot_len)

if __name__ == '__main__':
    main()

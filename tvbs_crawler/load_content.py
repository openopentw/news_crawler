""" This module load the contents in the json files in subfolder contents/

Example usage:

"""

import json

def main():
    """ Main function. """
    years = list(range(2017, 2013 - 1, -1))

    tot_len = 0

    for year in years:
        with open('contents/content_{}.json'.format(year)) as infile:
            content_list = json.load(infile)
        year_len = 0
        for month in content_list:
            for day in content_list[month]:
                year_len += len(content_list[month][day])
        print(year, year_len)
        tot_len += year_len

    print('Total length:', tot_len)

if __name__ == '__main__':
    main()

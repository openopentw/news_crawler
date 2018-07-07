""" This module load the urls in the json files in subfolder urls/

Example usage:
    python3 save_sample_url.py

"""

import json

def main():
    """ Main function. """
    year = 2017

    with open('urls/url_{}.json'.format(year)) as infile:
        url_list = json.load(infile)

    sample_url = {
        '1': url_list['1'],
        '2': url_list['2'],
    }

    with open('./sample_url.json', 'w', encoding='utf8') as outfile:
        json.dump(sample_url, outfile)

if __name__ == '__main__':
    main()

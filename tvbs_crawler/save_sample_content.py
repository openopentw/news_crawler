""" This module load the contents in the json files in subfolder contents/

Example usage:
    python3 save_sample_content.py

"""

import json

def main():
    """ Main function. """
    year = 2017

    with open('contents/content_{}.json'.format(year)) as infile:
        content_list = json.load(infile)

    sample_content = {
        '1': {
            '1': content_list['1']['1'][:50],
            '2': content_list['1']['2'][:50],
        },
        '2': {
            '1': content_list['2']['1'][:50],
            '2': content_list['2']['2'][:50],
        },
    }

    with open('./sample_content.json', 'w', encoding='utf8') as outfile:
        json.dump(sample_content, outfile)

if __name__ == '__main__':
    main()

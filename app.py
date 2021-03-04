import os

from scrapers import elsevier, sage, springer
from links import LINKS
from common import CSVWriter, CSVRow

# TODO: Error handling

def main():
    if not os.path.exists('out'):
        os.makedirs('out')
    
    csvwriter = CSVWriter()

    for idx, link in enumerate(LINKS):
        print('LINK %d OF %d' % (idx+1, len(LINKS)))

        if 'www.springer.com' in link:
            springer.scrape(link, csvwriter)
        elif 'journals.sagepub.com' in link:
            sage.scrape(link, csvwriter)
        elif 'www.elsevier.com' in link:
            elsevier.scrape(link, csvwriter)
        else:
            print('ERROR: INCORRECT LINK')

    print('DONE')
    csvwriter.teardown()

if __name__ == '__main__':
    main()

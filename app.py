from datetime import datetime
import csv, os

from scrapers import elsevier, sage, springer
from links import LINKS

# TODO: Error handling

def main():
    if not os.path.exists('out'):
        os.makedirs('out')
    
    filename = os.path.join('out/', '%s.csv' % datetime.now().strftime('%Y.%m.%d_%H.%M.%S'))
    csv_columns = ['Name', 'Title', 'Journal Title', 'Search Link']

    csvfile = open(filename, 'w', newline='', encoding='utf-8')
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()

    for idx, link in enumerate(LINKS):
        print('LINK %d OF %d' % (idx+1, len(LINKS)))

        if 'www.springer.com' in link:
            springer.scrape(link, writer)
        elif 'journals.sagepub.com' in link:
            sage.scrape(link, writer)
        elif 'www.elsevier.com' in link:
            elsevier.scrape(link, writer)
        else:
            print('ERROR: INCORRECT LINK')

    print('DONE')
    csvfile.close()

if __name__ == '__main__':
    main()

from datetime import datetime
import csv, os

from scrapers import elsevier, sage, springer
from links import LINKS

# TODO: Error handling
# TODO: Nicer output: https://stackoverflow.com/a/5291044

def main():
    if not os.path.exists('out'):
        os.makedirs('out')
    
    filename = os.path.join('out/', '%s.csv' % datetime.now().strftime('%Y.%m.%d_%H.%M.%S'))
    csv_columns = ['Name', 'E-mail', 'Title', 'Journal Title', 'Search Link']

    csvfile = open(filename, 'w', newline='', encoding='utf-8')
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()

    for link in LINKS:
        if 'www.springer.com' in link:
            springer.scrape(link, writer)
        elif 'journals.sagepub.com' in link:
            sage.scrape(link, writer)
        elif 'www.elsevier.com' in link:
            elsevier.scrape(link, writer)
        else:
            print('>> ERROR: INCORRECT LINK')

    csvfile.close()

if __name__ == '__main__':
    main()

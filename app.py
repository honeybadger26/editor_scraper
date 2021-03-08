import os

from links import LINKS
from scrapers import *
from common import CSVWriter, ErrorWriter

def main():
    if not os.path.exists('out'):
        os.makedirs('out')
    
    csvwriter = CSVWriter()
    errorwriter = ErrorWriter()

    for idx, link in enumerate(LINKS):
        print('LINK %d/%d' % (idx+1, len(LINKS)))

        if 'www.springer.com' in link:
            scraper = SpringerScraper(link, csvwriter, errorwriter)
        elif 'journals.sagepub.com' in link:
            scraper = SageScraper(link, csvwriter, errorwriter)
        elif 'www.elsevier.com' in link:
            scraper = ElsevierScraper(link, csvwriter, errorwriter)
        else:
            errorwriter.addsearchlink(link)
            continue

        scraper.getjournallinks()
        scraper.geteditors()

    csvwriter.teardown()
    print('DONE')

if __name__ == '__main__':
    main()

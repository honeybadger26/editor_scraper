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
        elif 'www.dovepress.com' in link:
            scraper = DovePressScraper(link, csvwriter, errorwriter)
        elif 'www.cambridge.org' in link:
            scraper = CambridgeScraper(link, csvwriter, errorwriter)
        elif 'pubs.rsc.org' in link:
            scraper = RSCScraper(link, csvwriter, errorwriter)
        elif 'direct.mit.edu' in link:
            scraper = MITScraper(link, csvwriter, errorwriter)
        elif 'www.tandfonline.com' in link:
            scraper = TaylorFrancisScraper(link, csvwriter, errorwriter)
        elif 'journals.plos.org' in link:
            scraper = PLOSScraper(link, csvwriter, errorwriter)
            scraper.journallinks = [link + 's/editorial-board']
            scraper.geteditors()
            continue
        else:
            errorwriter.addsearchlink(link)
            continue

        scraper.getjournallinks()
        scraper.geteditors()

    csvwriter.teardown()
    print('DONE')

if __name__ == '__main__':
    main()

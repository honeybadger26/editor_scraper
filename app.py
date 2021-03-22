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
        print('Scraping link %d of %d (%s)' % (idx+1, len(LINKS), link))

        if 'www.springer.com' in link:
            scraper = SpringerScraper(link, csvwriter, errorwriter)
        elif 'journals.sagepub.com' in link:
            scraper = SageScraper(link, csvwriter, errorwriter)
        elif 'www.elsevier.com' in link:
            scraper = ElsevierScraper(link, csvwriter, errorwriter)
        elif 'www.dovepress.com' in link:
            print('DovePress: Need to query each journal link for editorial board, this might take a while')
            scraper = DovePressScraper(link, csvwriter, errorwriter)
        elif 'www.cambridge.org' in link:
            scraper = CambridgeScraper(link, csvwriter, errorwriter)
        elif 'pubs.rsc.org' in link:
            print('RSoC: Need to query each journal link for editorial board, this might take a while')
            scraper = RSCScraper(link, csvwriter, errorwriter)
        elif 'direct.mit.edu' in link:
            scraper = MITScraper(link, csvwriter, errorwriter)
        elif 'www.tandfonline.com' in link:
            scraper = TaylorFrancisScraper(link, csvwriter, errorwriter)
        elif 'brill.com' in link:
            scraper = BrillScraper(link, csvwriter, errorwriter)
        elif 'www.frontiersin.org' in link:
            print('Frontiers: Need to query API, this might take a while')
            scraper = FrontiersScraper(link, csvwriter, errorwriter)
        elif 'journals.plos.org' in link:
            scraper = PLOSScraper(link, csvwriter, errorwriter)
            scraper.journallinks = [link + 's/editorial-board']
            scraper.geteditors()
            continue
        else:
            print('Error: Invalid link')
            errorwriter.addsearchlink(link)
            continue

        scraper.getjournallinks()
        scraper.geteditors()

    csvwriter.teardown()
    print('Done, quitting...')

if __name__ == '__main__':
    main()

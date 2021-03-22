from scrapers.base import BaseScraper
from common import get_soup

JOURNAL_LINK_BASE = 'https://www.tandfonline.com/action/journalInformation?show=editorialBoard&journalCode=%s'

class TaylorFrancisScraper(BaseScraper):

    def buildsearchpageurl(self):
        return '%s&startPage=%d' % (self.searchpagebaseurl, self.searchpagenum-1)

    def getjournalsonpage(self):
        linkelems = self.soup.find('ol', class_='browse-results browse').find_all('a', class_='ref', href=True)
        return [ JOURNAL_LINK_BASE % e['href'].replace('/toc/', '').replace('/current', '') for e in linkelems ]

    def hasnextsearchpage(self):
        return self.soup.find('a', class_='nextPage') is not None

    def getjournaltitle(self):
        return self.soup.find('span', class_='journal-heading').text.strip()

    def geteditorelems(self):
        boardelem = self.soup.find('h1', text='Editorial board').find_next('div')
        lines = boardelem.text.split('  ')
        return [ l.strip() for l in lines if l.strip() != '' ]

    # FIXME: Next methods are repeated code
    def geteditorname(self, elem):
        return elem

    def geteditorrole(self, elem):
        return ''



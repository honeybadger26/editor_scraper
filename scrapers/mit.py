from scrapers.base import BaseScraper

JOURNAL_LINK_BASE = 'https://direct.mit.edu%s/pages/editorial-info'

class MITScraper(BaseScraper):

    def buildsearchpageurl(self):
        return self.searchpagebaseurl

    def getjournalsonpage(self):
        linkelems = self.soup \
            .find('div', class_='widget-SelfServeContent widget-instance-SelfServeContent') \
            .find_all('a', href=True)
        return [ JOURNAL_LINK_BASE % l['href'] for l in linkelems ]

    def hasnextsearchpage(self):
        return False

    def getjournaltitle(self):
        return self.soup.find('a', class_='journal-logo-link').find('img', alt=True)['alt']

    def geteditorelems(self):
        boardelem = self.soup.find('div', class_='widget-SelfServeContent widget-instance-SelfServeContent')
        lines = boardelem.text.splitlines()
        return [ l for l in lines if l != '' ]

    def geteditorname(self, elem):
        return elem

    def geteditorrole(self, elem):
        return ''


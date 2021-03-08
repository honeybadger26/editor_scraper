from scrapers.base import BaseScraper

EDITOR_LINK_BASE = 'https://www.springer.com%s/editors'
JOURNAL_LINK_PREFIX = '/journal/'

class SpringerScraper(BaseScraper):
    def buildsearchpageurl(self):
        return '%s&page=%d' % (self.searchpagebaseurl, self.searchpagenum)

    def scrapejournallinks(self):
        linkelems = self.soup.find_all('a', href=True)
        journalsfound = False

        for e in linkelems:
            if e['href'].startswith(JOURNAL_LINK_PREFIX):
                journalsfound = True
                self.journallinks.add(EDITOR_LINK_BASE % e['href'])

        assert journalsfound, 'No journals found'

    def hasnextsearchpage(self):
        nextpagebtn = self.soup.find('a', class_='next')
        return nextpagebtn is not None

    def getjournaltitle(self):
        return self.soup.find('div', { 'id': 'journalTitle' }).text.strip()

    def geteditorelems(self):
        editorial_board_elem = self.soup.find('div', { 'id': 'editorialboard' })
        lines = editorial_board_elem.text.splitlines()
        return [ l for l in lines if l != '']

    def geteditorrole(self, elem):
        return ''

    def geteditorname(self, elem):
        return elem

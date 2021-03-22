from scrapers.base import BaseScraper

EDITOR_LINK_BASE = 'https://www.springer.com%s/editors'
JOURNAL_LINK_PREFIX = '/journal/'

class SpringerScraper(BaseScraper):

    def buildsearchpageurl(self):
        return '%s&page=%d' % (self.searchpagebaseurl, self.searchpagenum)

    def getjournalsonpage(self):
        linkelems = self.soup.find_all('a', href=True)
        links = []

        for e in linkelems:
            if e['href'].startswith(JOURNAL_LINK_PREFIX):
                links.append(EDITOR_LINK_BASE % e['href'])

        return links

    def hasnextsearchpage(self):
        nextpagebtn = self.soup.find('a', class_='next')
        return nextpagebtn is not None

    def getjournaltitle(self):
        return self.soup.find('div', { 'id': 'journalTitle' }).text.strip()

    def geteditorelems(self):
        editorial_board_elem = self.soup.find('div', { 'id': 'editorialboard' })
        lines = editorial_board_elem.text.splitlines()
        return [ l for l in lines if l != '' ]

    def geteditorname(self, elem):
        return elem

    def geteditorrole(self, elem):
        return ''


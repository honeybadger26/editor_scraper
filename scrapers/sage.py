from scrapers.base import BaseScraper

EDITOR_LINK_BASE = 'https://journals.sagepub.com/editorial-board/%s'

class SageScraper(BaseScraper):
    def buildsearchpageurl(self):
        # return '%s&startPage=%d' % (self.searchpagebaseurl, self.searchpagenum-1)
        return self.searchpagebaseurl

    def scrapejournallinks(self):
        linkelems = self.soup.find('div', class_='results').find('table').find_all('a', href=True)
        assert len(linkelems) != 0, 'No journals jound'
        for e in linkelems:
            self.journallinks.add(EDITOR_LINK_BASE % e['href'].removeprefix('/home/'))

    def hasnextsearchpage(self):
        # nextpagebtn = self.soup.find('a', class_='nextPage')
        # return nextpagebtn is not None
        return False

    def getjournaltitle(self):
        return self.soup.find('a', { 'id': 'headerTitle' }).text.strip()

    def geteditorelems(self):
        return [ e.find('a') for e in self.soup.find_all('td', class_='ed-board-member') ]

    def geteditorname(self, elem):
        return elem.text.strip()

    def geteditorrole(self, elem):
        return elem.find_previous('div', class_='ed-board-name').text.strip()

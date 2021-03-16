from scrapers.base import BaseScraper
from common import get_soup

JOURNAL_LINK_BASE = 'https://pubs.rsc.org%s'

class RSCScraper(BaseScraper):

    def buildsearchpageurl(self):
        return self.searchpagebaseurl

    def scrapejournallinks(self):
        print('\n\tSEARCHING FOR EDITORIAL BOARD LINK. THIS MIGHT TAKE A WHILE')
        linkelems = self.soup.find_all('a', class_='list__item-link', href=True)
        assert len(linkelems) != 0, 'No journals found'

        for l in linkelems:
            link = JOURNAL_LINK_BASE % l['href']
            temp_soup = get_soup(link)

            for infoelem in temp_soup.find_all('a', class_='list__item-link', href=True):
                if infoelem.text.strip() == 'Editorial Board': 
                    self.journallinks.add(infoelem['href'])

    def hasnextsearchpage(self):
        return False

    def getjournaltitle(self):
        return self.soup.find('h1', class_='home-header-with-drop').text.strip()

    def geteditorelems(self):
        return self.soup \
            .find('div', { 'id': 'boards-staff' }) \
            .find('div', class_='block tabsinnerblock') \
            .find_all('strong')

    def geteditorname(self, elem):
        return elem.text.strip()    # TODO: Put this in parent class?

    def geteditorrole(self, elem):
        return elem.find_previous('h4').text.strip()

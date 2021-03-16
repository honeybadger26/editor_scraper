from scrapers.base import BaseScraper

JOURNAL_LINK_BASE = 'https://www.cambridge.org%s/information/editorial-board'

class CambridgeScraper(BaseScraper):

    def buildsearchpageurl(self):
        return self.searchpagebaseurl   # Assumes only one page. TODO: Put this in parent class

    def scrapejournallinks(self):
        linkelems = self.soup.find_all('a', class_='title', href=True)
        for l in linkelems:
            self.journallinks.add(JOURNAL_LINK_BASE % l['href'])

    def hasnextsearchpage(self):
        return False # Assumes only one page

    def getjournaltitle(self):
        return self.soup.find('h1', class_='title white').text.strip()

    def geteditorelems(self):
        return self.soup.find('div', class_='row margin-bottom').find_all('p', class_='paragraph_03')

    def geteditorname(self, elem):
        return elem.find(text=True, recursive=False)

    def geteditorrole(self, elem):
        return elem.find_previous('h6', class_='margin-bottom').text.strip()

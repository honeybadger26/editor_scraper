from scrapers.base import BaseScraper
from common import get_soup

JOURNAL_LINK_BASE = 'https://www.dovepress.com/%s'

class DovePressScraper(BaseScraper):
    def buildsearchpageurl(self):
        return self.searchpagebaseurl   # Assumes only one page

    def getjournalsonpage(self):
        linkelemgroups = self.soup.find_all('div', class_='alpha-content')

        linkelems = []
        for e in linkelemgroups:
            linkelems.extend(e.find_all('a', href=True))

        links = []
        for l in linkelems:
            link = JOURNAL_LINK_BASE % l['href']
            temp_soup = get_soup(link)
            board_link_elem =  temp_soup.find('a', href=True, text='Editors')
            if board_link_elem is not None:
                links.append(JOURNAL_LINK_BASE % board_link_elem['href'])

        return links

    def hasnextsearchpage(self):
        return False        # Assumes only one page

    def getjournaltitle(self):
        return self.soup.find('div', class_='tabs-padding group').find('h1').text.strip()

    def geteditorelems(self):
        elems = []
        elems.extend(self.soup.find('div', class_='journals').find_all('h2'))
        elems.extend(self.soup.find('div', class_='categories-bg group').find_all('h5'))
        return elems

    def geteditorname(self, elem):
        return elem.text.strip()

    def geteditorrole(self, elem):
        return ''

from scrapers.base import BaseScraper

JOURNAL_DOMAIN = 'journals.elsevier.com'
EDITOR_LINK_BASE = '%s/editorial-board'

class ElsevierScraper(BaseScraper):
    def buildsearchpageurl(self):
        return '%s&page=%d' % (self.searchpagebaseurl, self.searchpagenum)

    def scrapejournallinks(self):
        linkelems = self.soup.find_all('a', href=True)
        journalsfound = False

        for e in linkelems:
            if JOURNAL_DOMAIN in e['href']:
                journalsfound = True
                self.journallinks.add(EDITOR_LINK_BASE % e['href'])

        assert journalsfound, 'No journals found'

    def hasnextsearchpage(self):
        nextpagebtn = self.soup.find('a', class_='pagination-btn pagination-btn--next')
        return nextpagebtn is not None and \
            'is-disabled' not in nextpagebtn['class']

    def getjournaltitle(self):
        pagetitleelem = self.soup.find('div', class_='publication-title')
        return pagetitleelem.text.strip().replace(' - Editorial Board', '')

    def geteditorelems(self):
        return [ _ for _ in self.soup.find_all('div', class_='publication-editor-name') ]

    def geteditorrole(self, elem):
        return elem.find_previous('div', class_='publication-editor-type').text.strip()

    def geteditorname(self, elem):
        return elem.text.strip()

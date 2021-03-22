from scrapers.base import BaseScraper

JOURNAL_LINK_BASE = 'https://brill.com%s'

class BrillScraper(BaseScraper):

    def buildsearchpageurl(self):
        return '%s&page=%d' % (self.searchpagebaseurl, self.searchpagenum)

    def getjournalsonpage(self):
        linkwrapperelems = self.soup.find_all('div', class_='typography-body text-headline color-primary')
        linkelems = [ e.find('a', class_='c-Button--link', href=True) for e in linkwrapperelems ]
        return [ JOURNAL_LINK_BASE % e['href'] for e in linkelems]

    def hasnextsearchpage(self):
        pageswrapperelem = self.soup.find('div', class_='t-data-grid-pager')
        pageselem = list(pageswrapperelem.children)
        lastelem = pageselem[-1]
        return not (lastelem.name == 'span' and 'current' in lastelem['class'])

    def getjournaltitle(self):
        return self.soup.find('h1', class_='title text-headline mb-3').text.strip()

    def geteditorelems(self):
        editorialheader = self.soup.find('span', class_='typography-body')
        boardelem = editorialheader.find_next('div', class_='component component-content-item component-editorial-content')
        lines = boardelem.text.splitlines()
        return [ l.strip() for l in lines if l.strip() != '' ]

    def geteditorname(self, elem):
        return elem

    def geteditorrole(self, elem):
        return ''

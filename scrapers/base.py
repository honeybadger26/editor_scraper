from common import get_soup, CSVRow, passedfilter

SEARCHING_JOURNALS_MSG = '\r\033[K\tSEARCHING FOR JOURNALS [PAGE %d] - FOUND: %d'
JOURNALS_FOUND_MSG = '\r\033[K\tJOURNALS FOUND: %d'
SEARCHING_EDITORS_MSG = '\r\033[K\tSEARCHING FOR EDITORS [PAGE %d/%d] - FOUND: %d'
EDITORS_FOUND_MSG = '\r\033[K\tEDITORS FOUND: %d'

class BaseScraper():
    def __init__(self, baselink, csvwriter, errorwriter):
        self.writer = csvwriter
        self.errorwriter = errorwriter

        self.searchpagebaseurl = baselink
        self.searchpagenum = 1

        self.journallinks = set()
        self.numeditorsfound = 0

    def buildsearchpageurl(self):
        pass

    def scrapejournallinks(self):
        pass

    def hasnextsearchpage(self):
        pass

    def getjournallinks(self):
        done = False

        while not done:
            searchpageurl = self.buildsearchpageurl()
            self.soup = get_soup(searchpageurl)

            try:
                self.scrapejournallinks()
            except:
                self.errorwriter.addsearchlink(searchpageurl)

            print(SEARCHING_JOURNALS_MSG % (self.searchpagenum, len(self.journallinks)), end='')

            done = not self.hasnextsearchpage()
            self.searchpagenum += 1

        print(JOURNALS_FOUND_MSG % len(self.journallinks))

    def getjournaltitle(self):
        pass

    def geteditorelems(self):
        pass

    def geteditorrole(self, elem):
        pass

    def geteditorname(self, elem):
        pass

    def geteditorsonpage(self, link):
        self.soup = get_soup(link)
        journaltitle = self.getjournaltitle()

        row = CSVRow()
        row.journal_title = journaltitle
        row.source_link = link

        editorelems = self.geteditorelems()

        for e in editorelems:
            row.editor_name = self.geteditorname(e)
            row.editor_title = self.geteditorrole(e)

            if not passedfilter(row.editor_name, row.editor_title):
                continue

            self.writer.writerow(row)
            self.numeditorsfound += 1

    def geteditors(self):
        for idx, journallink in enumerate(self.journallinks):
            try:
                self.geteditorsonpage(journallink)
            except:
                self.errorwriter.addjournallink(journallink)

            print(SEARCHING_EDITORS_MSG % (idx+1, len(self.journallinks), self.numeditorsfound), end='')

        print(EDITORS_FOUND_MSG % self.numeditorsfound)

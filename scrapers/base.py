from common import get_soup, passedfilter, printthisline

SEARCHING_EDITORS_MSG = '\r\033[K\tSEARCHING FOR EDITORS [PAGE %d/%d] - FOUND: %d'
EDITORS_FOUND_MSG = '\r\033[K\tEDITORS FOUND: %d'
GOOGLE_LINK_BASE = 'http://www.google.com/search?q=%s+"%s"'

class BaseScraper():

    def __init__(self, baselink, csvwriter, errorwriter):
        self.writer = csvwriter
        self.errorwriter = errorwriter

        self.searchpagebaseurl = baselink
        self.searchpagenum = 1

        self.journallinks = set()
        self.editors = []

    # Returns the URL of the next page to scrape for journal links
    def buildsearchpageurl(self):
        pass

    # Return an array of journal links scraped from current page
    def getjournalsonpage(self):
        pass

    # Returns whether there are more search pages to scrape journal links from
    def hasnextsearchpage(self):
        pass

    # Scrape journal links from all search pages
    def getjournallinks(self):
        done = False

        while not done:
            searchpageurl = self.buildsearchpageurl()
            self.soup = get_soup(searchpageurl)

            try:
                journals = self.getjournalsonpage()
                for j in journals:
                    self.journallinks.add(j)
                printthisline('Scraping journals [Page: %d - Found on page: %d - Total found: %d]'
                    % (self.searchpagenum, len(journals), len(self.journallinks)))
            except Exception as e:
                print('\nError: %s' % str(e))
                self.errorwriter.addsearchlink(searchpageurl)

            done = not self.hasnextsearchpage()
            self.searchpagenum += 1

        print('')

    def getjournaltitle(self):
        pass

    def geteditorelems(self):
        pass

    def geteditorname(self, elem):
        pass

    def geteditorrole(self, elem):
        pass

    def geteditorsonpage(self, link):
        self.soup = get_soup(link)
        journaltitle = self.getjournaltitle()

        editorelems = self.geteditorelems()
        editors = []

        for e in editorelems:
            editor_name = self.geteditorname(e)
            editor_title = self.geteditorrole(e)

            if not passedfilter(editor_name, editor_title):
                continue

            editors.append({
                'Name': editor_name,
                'Title': editor_title,
                'Journal Title': journaltitle,
                'Source URL': link,
                'Search Link': GOOGLE_LINK_BASE % (
                        editor_name.replace(' ', '+'), 
                        journaltitle.replace(' ', '+')
                    )
            })

        return editors

    def geteditors(self):
        totaleditors = 0

        for idx, journallink in enumerate(self.journallinks):
            self.currentjournalpage = journallink

            try:
                editors = self.geteditorsonpage(journallink)

                for e in editors:
                    self.writer.writerow(e)
                    totaleditors += 1
                
                printthisline('Scraping editors [Page: %d/%d - Found on page: %d - Total found: %d]' 
                    % (idx+1, len(self.journallinks), len(editors), totaleditors))
            except Exception as e:
                print('\nError: %s' % str(e))
                self.errorwriter.addjournallink(journallink)

        print('')
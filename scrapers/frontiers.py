import re, requests, json

from scrapers.base import BaseScraper

API_BASE_URL = 'https://www.frontiersin.org/api/journals/%d/editors/filters?index=%d'
API_PAYLOAD = 'JournalId=%d&RoleCode=All&SortType=Ascending&KeyWord=+'
API_HEADERS = { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }

class FrontiersScraper(BaseScraper):

    def buildsearchpageurl(self):
        return self.searchpagebaseurl

    def scrapejournallinks(self):
        wrapperelems = self.soup.findAll('h5', class_='clearfix pull-left')
        linkelems = [ e.find('a', href=True) for e in wrapperelems ]

        assert len(linkelems) != 0, 'No journals found'

        for l in linkelems:
            self.journallinks.add(l['href'])

    def hasnextsearchpage(self):
        return False

    def getjournaltitle(self):
        return self.soup.find('title').text.strip()

    def geteditorelems(self):
        pagenum = 0
        journalid = int(re.search(r'\d+$', self.currentjournalpage).group())

        url = API_BASE_URL % (journalid, pagenum)
        payload = API_PAYLOAD % journalid

        print('\tFETCHING ALL EDITORS. THIS MIGHT TAKE A WHILE')
        r = requests.post(url, data=payload, headers=API_HEADERS)
        response = r.json()

        editorelems = []
        while 'Editors' in response and response['Editors'] is not None:
            for editor in response['Editors']:
                editorelems.append({                  
                    'Name': editor['FullName'],
                    'Role': editor['Role']['Name']
                })

            pagenum += 1
            url = API_BASE_URL % (journalid, pagenum)
            r = requests.post(url, data=payload, headers=API_HEADERS)
            response = r.json()

        return editorelems

    def geteditorrole(self, elem):
        return elem['Role']

    def geteditorname(self, elem):
        return elem['Name']
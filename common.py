import requests
from bs4 import BeautifulSoup

from exclusions import EXCLUSIONS

GOOGLE_LINK_BASE = 'http://www.google.com/search?q=%s+"%s"'
TIMEOUT = 5

SEARCHING_JOURNALS_MSG = '\r\033[K\tSEARCHING PAGE FOR JOURNALS [%d/%s] - JOURNALS FOUND: %d '

def get_soup(link):
    r = requests.get(link)
    return BeautifulSoup(r.content, 'html.parser')

def isallowedrole(role):
    for e in EXCLUSIONS:
        if e.lower() in role.lower():
            return False
    return True

class CSVRow():
    editor_name = ''
    editor_title = ''
    journal_title = ''
    source_link = ''
    search_link = ''

    def getObj(self):
        return {
            'Name': self.editor_name,
            'Title': self.editor_title,
            'Journal Title': self.journal_title,
            'Source URL': self.source_link,
            'Search Link': self.search_link
        }
from datetime import datetime
import csv, os
import requests
from bs4 import BeautifulSoup

from exclusions import EXCLUSIONS

GOOGLE_LINK_BASE = 'http://www.google.com/search?q=%s+"%s"'
TIMEOUT = 5
FILE_ROW_LIMIT = 1000

SEARCHING_JOURNALS_MSG = '\r\033[K\tSEARCHING PAGE FOR JOURNALS [%d/%s] - JOURNALS FOUND: %d '

def get_soup(link):
    r = requests.get(link)
    return BeautifulSoup(r.content, 'html.parser')

def isallowedrole(role):
    for e in EXCLUSIONS:
        if e.lower() in role.lower():
            return False
    return True

class CSVWriter():
    numrows = 0
    csvfile = None
    writer = None

    def __init__(self):
        self.setup()

    def setup(self):
        filename = os.path.join('out/', '%s.csv' % datetime.now().strftime('%Y.%m.%d_%H.%M.%S'))
        self.csvfile = open(filename, 'w', newline='', encoding='utf-8')
        csv_columns = list(CSVRow().getObj().keys())
        self.writer = csv.DictWriter(self.csvfile, fieldnames=csv_columns)
        self.writer.writeheader()

    def teardown(self):
        self.csvfile.close()
        self.numrows = 0

    def writerow(self, row):
        self.writer.writerow(row.getObj())
        self.numrows += 1

        if self.numrows >= FILE_ROW_LIMIT:
            self.teardown()
            self.setup()

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
from time import sleep
from datetime import datetime
import csv, os
import requests
from bs4 import BeautifulSoup

from exclusions import EXCLUSIONS

GOOGLE_LINK_BASE = 'http://www.google.com/search?q=%s+"%s"'
TIMEOUT = 0
FILE_ROW_LIMIT = 1000

def get_soup(link):
    r = requests.get(link)
    sleep(TIMEOUT)
    return BeautifulSoup(r.content, 'html.parser')

def passedfilter(name, role):
    if name == '' or name.isspace():
        return False

    for e in EXCLUSIONS:
        if e.lower() in role.lower():
            return False

    return True

class ErrorWriter():
    def addsearchlink(self, link):
        filename = os.path.join('out/', 'FailedSearchPages.csv')
        with open(filename, 'w') as f:
            f.write(link + '\n')

    def addjournallink(self, link):
        filename = os.path.join('out/', 'FailedEditorialBoardPages.csv')
        with open(filename, 'w') as f:
            f.write(link + '\n')

class CSVWriter():
    def __init__(self):
        self.setup()

    def setup(self):
        filename = os.path.join('out/', '%s.csv' % datetime.now().strftime('%Y.%m.%d_%H.%M.%S'))
        csv_columns = list(CSVRow().getObj().keys())

        self.csvfile = open(filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.csvfile, fieldnames=csv_columns)
        self.numrows = 0

        self.writer.writeheader()

    def teardown(self):
        self.csvfile.close()

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

    def getObj(self):
        search_link = GOOGLE_LINK_BASE % (
            self.editor_name.replace(' ', '+'), 
            self.journal_title.replace(' ', '+')
        )
        return {
            'Name': self.editor_name,
            'Title': self.editor_title,
            'Journal Title': self.journal_title,
            'Source URL': self.source_link,
            'Search Link': search_link
        }

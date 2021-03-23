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
    r = requests.get(link, allow_redirects=True, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
    })
    sleep(TIMEOUT)
    return BeautifulSoup(r.content, 'html.parser')

def passedfilter(name, role):
    if name == '' or name.isspace():
        return False

    for e in EXCLUSIONS:
        if e.lower() in role.lower():
            return False

    return True

def printthisline(msg):
    print('\r%s' % msg, end=' '*20)

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
        csv_columns = ['Name', 'Title', 'Journal Title', 'Source URL', 'Search Link' ]

        self.csvfile = open(filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.csvfile, fieldnames=csv_columns)
        self.numrows = 0

        self.writer.writeheader()

    def teardown(self):
        self.csvfile.close()

    def writerow(self, row):
        self.writer.writerow(row)
        self.numrows += 1

        if self.numrows >= FILE_ROW_LIMIT:
            self.teardown()
            self.setup()
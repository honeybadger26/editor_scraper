import re
from time import sleep

import common

EDITORS_LINK_BASE = 'https://www.springer.com%s/editors'
JOURNAL_LINK_PREFIX = '/journal/'


def getjournallinks(base_link):
    editors_links = set()
    done = False
    page_num = 1
    total_pages = None

    while not done:
        result_page_link = '%s&page=%d' % (base_link, page_num)

        soup = common.get_soup(result_page_link)
        sleep(common.TIMEOUT)

        if total_pages is None:
            total_pages = int(soup.find('span', class_='number-of-pages').text.strip())

        link_elems = soup.find_all('a', href=True)
        for e in link_elems:
            if e['href'].startswith(JOURNAL_LINK_PREFIX):
                editors_links.add(EDITORS_LINK_BASE % e['href'])

        print(common.SEARCHING_JOURNALS_MSG % (page_num, str(total_pages), len(editors_links)), end='')

        page_num += 1
        done = page_num > total_pages
    
    return editors_links


def scrape(base_link, csvwriter):
    total_lines = 0
    num_skipped = 0

    editors_links = getjournallinks(base_link)
    print('')

    for idx, editors_link in enumerate(editors_links):
        print('\r\tSEARCHING JOURNALS [%d/%d] - ' % (idx+1, len(editors_links)), end='')

        soup = common.get_soup(editors_link)

        editorial_board_elem = soup.find('div', { 'id': 'editorialboard' })

        if editorial_board_elem is None:
            num_skipped += 1
            continue

        row = common.CSVRow()
        journal_title = soup.find('div', { 'id': 'journalTitle' }).text.strip()
        row.journal_title = journal_title
        row.source_link = editors_links

        lines = editorial_board_elem.text.splitlines()
        lines = [ l for l in lines if l != '']

        for line in lines:
            row.editor_name = line
            row.search_link = common.GOOGLE_LINK_BASE % (line.replace(' ', '+'), journal_title.replace(' ', '+'))

            csvwriter.writerow(row.getObj())
            total_lines += 1

        print('TOTAL LINES FOUND: %d - JOURNALS SKIPPED: %d \033[K' % (total_lines, num_skipped), end='')

    print('')
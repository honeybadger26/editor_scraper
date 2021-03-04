import re
from time import sleep

import common

JOURNAL_DOMAIN = 'journals.elsevier.com'
EDITOR_LINK_BASE = '%s/editorial-board'

def getjournallinks(base_link):
    journal_links = set() 
    done = False
    page_num = 1
    total_pages = None

    while not done:
        search_page_link = '%s&page=%d' % (base_link, page_num)

        soup = common.get_soup(search_page_link)
        sleep(common.TIMEOUT)

        if total_pages is None:
            page_status = soup.find('div', class_='pagination-status').text.strip()
            total_pages = int(re.search('(\d+)$', page_status).group())

        link_elems = soup.find_all('a', href=True)
        for e in link_elems:
            if JOURNAL_DOMAIN in e['href']:
                journal_links.add(EDITOR_LINK_BASE % e['href'])

        print(common.SEARCHING_JOURNALS_MSG % (page_num, str(total_pages), len(journal_links)), end='')

        page_num += 1
        done = page_num > total_pages

    return journal_links


def scrape(base_link, csvwriter):
    total_editors = 0
    num_skipped = 0

    journal_links = getjournallinks(base_link)

    print('')

    for idx, journal_link in enumerate(journal_links):
        print('\r\tSEARCHING JOURNALS [%d/%d] - ' % (idx+1, len(journal_links)), end='')
        soup = common.get_soup(journal_link)

        page_title = soup.find('div', class_='publication-title')
        if page_title is None:
            num_skipped += 1
            continue

        row = common.CSVRow()
        journal_title = page_title.text.strip().replace(' - Editorial Board', '')
        row.journal_title = journal_title
        row.source_link = journal_link

        editor_elems = [ _ for _ in soup.find_all('div', class_='publication-editor-name') ]
        editor_title = None

        for editor_elem in editor_elems:
            new_editor_title = editor_elem.find_previous('div', class_='publication-editor-type').text.strip()
            if new_editor_title != editor_title:
                editor_title = new_editor_title

            if not common.isallowedrole(editor_title):
                continue

            editor_name = editor_elem.text.strip()
            row.editor_name = editor_name
            row.editor_title = editor_title
            row.search_link = common.GOOGLE_LINK_BASE % (editor_name.replace(' ', '+'), journal_title.replace(' ', '+'))

            csvwriter.writerow(row)
            total_editors += 1

        print('TOTAL EDITORS FOUND: %d - JOURNALS SKIPPED: %d \033[K' % (total_editors, num_skipped), end='')

    print('')

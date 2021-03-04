from time import sleep

import common

EDITOR_LINK_BASE = 'https://journals.sagepub.com/editorial-board/%s'

def scrape(base_link, csvwriter):
    editors_links = set()
    done = False

    page_num = 0
    total_editors = 0

    while not done:
        search_page_link = '%s&startPage=%d' % (base_link, page_num)

        soup = common.get_soup(search_page_link)
        sleep(common.TIMEOUT)

        link_elems = soup.find('div', class_='results').find('table').find_all('a', href=True)
        for e in link_elems:
            editors_links.add(EDITOR_LINK_BASE % e['href'].removeprefix('/home/'))

        print(common.SEARCHING_JOURNALS_MSG % (page_num+1, 'unknown', len(editors_links)), end='')

        page_num += 1
        if soup.find('a', class_='nextPage') is None:
            done = True

    print('')

    for idx, editors_link in enumerate(editors_links):
        print('\r\tSEARCHING JOURNAL [%d/%d] - ' % (idx+1, len(editors_links)), end='')
        soup = common.get_soup(editors_link)

        row = common.CSVRow()
        journal_title = soup.find('a', { 'id': 'headerTitle' }).text.strip()
        row.journal_title = journal_title
        row.source_link = editors_link

        # Get editors
        editor_elems = [ e.find('a') for e in soup.find_all('td', class_='ed-board-member') ]
        editor_title = None

        for editor_elem in editor_elems:
            new_editor_title = editor_elem.find_previous('div', class_='ed-board-name').text.strip()
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

        print('TOTAL EDITORS FOUND: %d \033[K' % total_editors, end='')

    print('')

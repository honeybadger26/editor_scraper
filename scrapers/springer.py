import re
from time import sleep

from common import get_soup, GOOGLE_LINK_BASE, TIMEOUT

EDITORS_LINK_BASE = 'https://www.springer.com%s/editors'
JOURNAL_LINK_PREFIX = '/journal/'

def scrape(base_link, csvwriter):
    editors_links = set()
    done = False

    page_num = 1
    total_pages = None
    total_lines = 0
    num_skipped = 0

    while not done:
        result_page_link = '%s&page=%d' % (base_link, page_num)

        soup = get_soup(result_page_link)
        sleep(TIMEOUT)

        if total_pages is None:
            total_pages = int(soup.find('span', class_='number-of-pages').text.strip())

        link_elems = soup.find_all('a', href=True)
        for e in link_elems:
            if e['href'].startswith(JOURNAL_LINK_PREFIX):
                editors_links.add(EDITORS_LINK_BASE % e['href'])

        print('\r\033[K\tSEARCHING FOR JOURNALS [%d/%d] - FOUND: %d ' 
            % (page_num, total_pages, len(editors_links)), end='')

        page_num += 1
        done = page_num > total_pages

    print('')

    for idx, editors_link in enumerate(editors_links):
        print('\r\tSEARCHING JOURNALS [%d/%d] - ' % (idx+1, len(editors_links)), end='')

        soup = get_soup(editors_link)

        editorial_board_elem = soup.find('div', { 'id': 'editorialboard' })

        if editorial_board_elem is None:
            num_skipped += 1
            continue

        data = { 'Title': '' }

        data['Journal Title'] = soup.find('div', { 'id': 'journalTitle' }).text.strip()

        lines = editorial_board_elem.text.splitlines()
        lines = [ l for l in lines if l != '']

        for line in lines:
            data['Name'] = line
            data['Search Link'] = GOOGLE_LINK_BASE + line.replace(' ', '+')

            csvwriter.writerow(data)
            total_lines += 1

        print('TOTAL LINES FOUND: %d - JOURNALS SKIPPED: %d \033[K' % (total_lines, num_skipped), end='')

    print('')
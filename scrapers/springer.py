import re
from time import sleep

from common import get_soup, GOOGLE_LINK_BASE, TIMEOUT

EDITORS_LINK_BASE = 'https://www.springer.com%s/editors'
EMAIL_REGEX = '(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
JOURNAL_LINK_PREFIX = '/journal/'

def scrape(base_link):
    editors_links = set()
    done = False
    page_num = 1
    total_pages = None

    while not done:
        result_page_link = '%s&page=%d' % (base_link, page_num)

        soup = get_soup(result_page_link)
        sleep(TIMEOUT)

        if total_pages is None:
            total_pages = int(soup.find('span', class_='number-of-pages').text.strip())

        print('SEARCHING PAGE %d OF %d' % (page_num, total_pages))

        link_elems = soup.find_all('a', href=True)
        for e in link_elems:
            if e['href'].startswith(JOURNAL_LINK_PREFIX):
                editors_links.add(EDITORS_LINK_BASE % e['href'])

        print('TOTAL JOURNALS FOUND: %d' % len(editors_links))
        page_num += 1
        done = page_num > total_pages

    for editors_link in editors_links:
        print('QUERYING: %s' % editors_link)
        soup = get_soup(editors_link)

        editorial_board_elem = soup.find('div', { 'id': 'editorialboard' })

        if editorial_board_elem is None:
            continue

        journal_title = soup.find('div', { 'id': 'journalTitle' }).text.strip()
        print(journal_title)

        emails = set(re.findall(EMAIL_REGEX, editorial_board_elem.text))

        for email in emails:
            print('\t%s' % email)

        print('')

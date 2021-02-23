import re
from time import sleep

from common import get_soup, GOOGLE_LINK_BASE, TIMEOUT

JOURNAL_DOMAIN = 'journals.elsevier.com'
EDITOR_LINK_BASE = '%s/editorial-board'

def scrape(base_link, csvwriter):
    journal_links = set() 
    done = False
    page_num = 1
    total_pages = None

    while not done:
        search_page_link = '%s&page=%d' % (base_link, page_num)

        soup = get_soup(search_page_link)
        sleep(TIMEOUT)

        if total_pages is None:
            last_page_link = soup.find('a', class_='pagination-btn--last', href=True)['href']
            total_pages = int(re.search('(?!page=)\d+', last_page_link).group())

        print('SEARCHING PAGE [%d/%d]' % (page_num, total_pages))

        link_elems = soup.find_all('a', href=True)
        for e in link_elems:
            if JOURNAL_DOMAIN in e['href']:
                journal_links.add(EDITOR_LINK_BASE % e['href'])

        print('\tTOTAL JOURNALS FOUND: %d' % len(journal_links))
        page_num += 1
        done = page_num > total_pages

    for idx, journal_link in enumerate(journal_links):
        print('QUERYING [%d/%d] (%s)' % (idx, len(journal_links), journal_link))
        soup = get_soup(journal_link)

        page_title = soup.find('div', class_='publication-title')
        if page_title is None:
            print('\tINVALID PAGE. SKIPPING')
            continue

        data = {
            'Journal Title': page_title.text.strip().replace(' - Editorial Board', ''),
            'E-mail': ''
        }

        editor_elems = [ _ for _ in soup.find_all('div', class_='publication-editor-name') ]
        print('\tEDITORS FOUND: %d' % len(editor_elems))

        editor_title = None

        for editor_elem in editor_elems:
            new_editor_title = editor_elem.find_previous('div', class_='publication-editor-type').text.strip()
            if new_editor_title != editor_title:
                editor_title = new_editor_title

            data['Title'] = editor_title

            editor_name = editor_elem.text.strip()
            data['Name'] = editor_name

            google_link = GOOGLE_LINK_BASE + editor_name.replace(' ', '+')
            data['Search Link'] = google_link

            csvwriter.writerow(data)

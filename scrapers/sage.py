from common import get_soup, GOOGLE_LINK_BASE

EDITOR_LINK_BASE = 'https://journals.sagepub.com/editorial-board/%s'

def scrape(link, csvwriter):
    soup = get_soup(link)

    total_editors = 0

    # Find links for each journal
    journal_links = soup.find('div', class_='results').find('table').find_all('a', href=True)

    print('\tJOURNALS FOUND: %d' % len(journal_links))

    for idx, journal_link_elem in enumerate(journal_links):
        # Make link to editorial board page
        editorial_board_link = EDITOR_LINK_BASE % journal_link_elem['href'].removeprefix('/home/')

        print('\r\tSEARCHING JOURNAL [%d/%d] - ' % (idx+1, len(journal_links)), end='')
        soup = get_soup(editorial_board_link)

        data = {
            'Journal Title': soup.find('a', { 'id': 'headerTitle' }).text.strip()
        }

        # Get editors
        editor_elems = [ e.find('a') for e in soup.find_all('td', class_='ed-board-member') ]
        editor_title = None

        for editor_elem in editor_elems:
            new_editor_title = editor_elem.find_previous('div', class_='ed-board-name').text.strip()
            if new_editor_title != editor_title:
                editor_title = new_editor_title

            data['Title'] = editor_title

            editor_name = editor_elem.text.strip()
            data['Name'] = editor_name

            google_link = GOOGLE_LINK_BASE + editor_name.replace(' ', '+')
            data['Search Link'] = google_link

            csvwriter.writerow(data)
            total_editors += 1

        print('TOTAL EDITORS FOUND: %d \033[K' % total_editors, end='')

    print('')

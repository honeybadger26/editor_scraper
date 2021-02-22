from common import get_soup, GOOGLE_LINK_BASE

EDITOR_LINK_BASE = 'https://journals.sagepub.com/editorial-board/%s'

def scrape(link):
    soup = get_soup(link)

    # Find links for each journal
    journal_links = soup.find('div', class_='results').find('table').find_all('a', href=True)

    print('JOURNALS FOUND: %d' % len(journal_links))

    for journal_link_elem in journal_links:
        # Make link to editorial board page
        editorial_board_link = EDITOR_LINK_BASE % journal_link_elem['href'].removeprefix('/home/')

        print('QUERYING: %s' % editorial_board_link)
        soup = get_soup(editorial_board_link)

        # Get editors
        editor_elems = [ e.find('a') for e in soup.find_all('td', class_='ed-board-member') ]
        print('\tEDITORS FOUND: %d' % len(editor_elems))

        editor_title = None

        for editor_elem in editor_elems:
            new_editor_title = editor_elem.find_previous('div', class_='ed-board-name').text.strip()
            if new_editor_title != editor_title:
                editor_title = new_editor_title
                print('\t%s' % editor_title)

            editor_name = editor_elem.text.strip()
            google_link = GOOGLE_LINK_BASE + editor_name.replace(' ', '+')
            print('\t\t%-60s%s' % (editor_name, google_link))

        print('')



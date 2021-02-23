import requests
from bs4 import BeautifulSoup

GOOGLE_LINK_BASE = 'http://www.google.com/search?q='
TIMEOUT = 5

def get_soup(link):
    # TODO: Multiple attempts
    r = requests.get(link)
    return BeautifulSoup(r.content, 'html.parser')

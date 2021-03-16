from scrapers.base import BaseScraper
class PLOSScraper(BaseScraper):

    def getjournaltitle(self):
        return self.soup.find('h1', class_='logo').text.strip()        

    def geteditorelems(self):
        return self.soup.find('article').find_all('h4')

    def geteditorname(self, elem):
        return elem.text.strip()

    def geteditorrole(self, elem):
        role_elem = elem.find_previous_sibling('h3')
        if role_elem is None:
            role_elem = elem.find_previous_sibling('h2')
        return role_elem.text.strip()

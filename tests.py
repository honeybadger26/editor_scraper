import unittest
import unittest.mock as mock

# import app
from scrapers import *

csvwriter = mock.Mock()
errorwriter = mock.Mock()
INVALID_LINK = 'http://blank.org/'

class TestBase():
    def setUp(self):
        csvwriter.reset_mock()
        errorwriter.reset_mock()

    def test_scrapejournallinkssuccess(self):
        scraper = self.SCRAPER(self.SEARCH_RESULT_LINK, csvwriter, errorwriter)
        scraper.getjournallinks()
        errorwriter.addsearchlink.assert_not_called()

    def test_scrapejournalslinksfailed(self):
        scraper = self.SCRAPER(INVALID_LINK, csvwriter, errorwriter)
        scraper.getjournallinks()
        errorwriter.addsearchlink.assert_called()

    def test_scrapeeditorssuccess(self):
        scraper = self.SCRAPER('', csvwriter, errorwriter)
        scraper.journallinks = [self.JOURNAL_LINK]
        scraper.geteditors()
        csvwriter.writerow.assert_called()
        errorwriter.addjournallink.assert_not_called()

    def test_scrapeeditorsfailed(self):
        scraper = self.SCRAPER('', csvwriter, errorwriter)
        scraper.journallinks = [INVALID_LINK]
        scraper.geteditors()
        csvwriter.writerow.assert_not_called()
        errorwriter.addjournallink.assert_called()

class TestElsevier(TestBase, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SEARCH_RESULT_LINK = 'https://www.elsevier.com/en-au/search-results?labels=journals&subject-0=27380&subject-1=28004'
        cls.JOURNAL_LINK = 'https://www.journals.elsevier.com/studies-in-history-and-philosophy-of-science/editorial-board'
        cls.SCRAPER = ElsevierScraper

class TestSage(TestBase, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SEARCH_RESULT_LINK = 'https://journals.sagepub.com/action/showPublications?category=10.1177/life-and-biomedical-sciences-cell-biology'
        cls.JOURNAL_LINK = 'https://journals.sagepub.com/editorial-board/stia'
        cls.SCRAPER = SageScraper

class TestSpringer(TestBase, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SEARCH_RESULT_LINK = 'https://www.springer.com/gp/search?dnc=true&facet-subj=subj__111000&facet-type=type__journal&query=energy+test&submit=Submit+Query'
        cls.JOURNAL_LINK = 'https://www.springer.com/journal/43937/editors'
        cls.SCRAPER = SpringerScraper

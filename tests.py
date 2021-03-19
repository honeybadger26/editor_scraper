import unittest
import unittest.mock as mock

from scrapers import *

csvwriter = mock.Mock()
errorwriter = mock.Mock()

class TestBase():
    def setUp(self):
        csvwriter.reset_mock()
        errorwriter.reset_mock()

    def test_scrapejournallinks(self):
        scraper = self.SCRAPER(self.SEARCH_RESULT_LINK, csvwriter, errorwriter)
        scraper.getjournallinks()

        assert len(scraper.journallinks) != 0, 'Expected journals to be found'
        errorwriter.addsearchlink.assert_not_called()

    def test_scrapeeditors(self):
        scraper = self.SCRAPER('', csvwriter, errorwriter)
        scraper.journallinks = [self.JOURNAL_LINK]
        scraper.geteditors()

        assert scraper.numeditorsfound != 0, 'Expected editors to be found'
        csvwriter.writerow.assert_called()
        errorwriter.addjournallink.assert_not_called()

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

class TestPLOS(TestBase, unittest.TestCase):
    test_scrapejournallinks = property(doc='(!) Disallowed inherited')

    @classmethod
    def setUpClass(cls):
        cls.JOURNAL_LINK = 'https://journals.plos.org/plosgenetics/s/editorial-board'
        cls.SCRAPER = PLOSScraper

class TestDovePress(TestBase, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SEARCH_RESULT_LINK = 'https://www.dovepress.com/browse_journals.php'
        cls.JOURNAL_LINK = 'https://www.dovepress.com/journal-editor-hypoxia-eic149'
        cls.SCRAPER = DovePressScraper

class TestCambridge(TestBase, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SEARCH_RESULT_LINK = 'https://www.cambridge.org/core/what-we-publish/journals'
        cls.JOURNAL_LINK = 'https://www.cambridge.org/core/journals/animal-health-research-reviews/information/editorial-board'
        cls.SCRAPER = CambridgeScraper

class TestRSC(TestBase, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SEARCH_RESULT_LINK = 'https://pubs.rsc.org/en/journals'
        cls.JOURNAL_LINK = 'https://www.rsc.org/publishing/journals/dt/staff.asp'
        cls.SCRAPER = RSCScraper

class TestMIT(TestBase, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SEARCH_RESULT_LINK = 'https://direct.mit.edu/journals/pages/browse-by-title'
        cls.JOURNAL_LINK = 'https://direct.mit.edu/lmj/pages/editorial-info'
        cls.SCRAPER = MITScraper

class TestTaylorFrancis(TestBase, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SEARCH_RESULT_LINK = 'https://www.tandfonline.com/action/showPublications?pubType=journal'
        cls.JOURNAL_LINK = 'https://www.tandfonline.com/action/journalInformation?show=editorialBoard&journalCode=raie20'
        cls.SCRAPER = TaylorFrancisScraper

class TestBrill(TestBase, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SEARCH_RESULT_LINK = 'https://brill.com/browse?et=j&level=parent&pageSize=10&pubschedule_1=upcoming&pubschedule_2=new&pubschedule_3=published&sort=datedescending'
        cls.JOURNAL_LINK = 'https://brill.com/view/journals/rpal/rpal-overview.xml?rskey=cNbNpb&result=1'
        cls.SCRAPER = BrillScraper

class TestFrontiers(TestBase, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SEARCH_RESULT_LINK = 'https://www.frontiersin.org/about/journals-a-z'
        cls.JOURNAL_LINK = 'https://www.frontiersin.org/journals/1723'
        cls.SCRAPER = FrontiersScraper
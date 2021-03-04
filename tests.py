import unittest
import unittest.mock as mock

import app

TEST_LINKS = [
    'https://www.elsevier.com/en-au/search-results?labels=journals&subject-0=27380&subject-1=28004',
    'https://journals.sagepub.com/action/showPublications?category=10.1177/life-and-biomedical-sciences-cell-biology',
    'https://www.springer.com/gp/search?dnc=true&facet-subj=subj__111000&facet-type=type__journal&query=energy+test&submit=Submit+Query'
]

class Test_App(unittest.TestCase):
    @mock.patch('app.LINKS', TEST_LINKS)
    def test_app(self):
        app.main()
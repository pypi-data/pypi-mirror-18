import os
import unittest
import zope.testrunner
from zope import component
from sparc.testing.fixture import test_suite_mixin
from sparc.git.testing import SPARC_GIT_INTEGRATION_LAYER


class SparcGitUrlTestCase(unittest.TestCase):
    layer = SPARC_GIT_INTEGRATION_LAYER
    sm = component.getSiteManager()
    
    def test_url(self):
        from sparc.git import IRepoUrl
        url = component.createObject(u'sparc.git.url', 'dummy url')
        self.assertEquals(url, 'dummy url')
        self.assertTrue(IRepoUrl.providedBy(url))

class test_suite(test_suite_mixin):
    layer = SPARC_GIT_INTEGRATION_LAYER
    package = 'sparc.git'
    module = 'url'
    
    def __new__(cls):
        suite = super(test_suite, cls).__new__(cls)
        suite.addTest(unittest.makeSuite(SparcGitUrlTestCase))
        return suite

if __name__ == '__main__':
    zope.testrunner.run([
                         '--path', os.path.dirname(__file__),
                         '--tests-pattern', os.path.splitext(
                                                os.path.basename(__file__))[0]
                         ])
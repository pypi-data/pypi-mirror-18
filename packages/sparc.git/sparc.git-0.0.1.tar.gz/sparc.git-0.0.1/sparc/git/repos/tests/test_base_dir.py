import os
import unittest
import zope.testrunner
from zope import component
from sparc.testing.fixture import test_suite_mixin
from sparc.git.repos.testing import SPARC_GIT_REPOS_DIR_INTEGRATION_LAYER

import git
import tempfile

class SparcGitUrlTestCase(unittest.TestCase):
    layer = SPARC_GIT_REPOS_DIR_INTEGRATION_LAYER
    sm = component.getSiteManager()
    wd = [] # a list of working directories created within a test
    
    def tearDown(self):
        super(SparcGitUrlTestCase, self).tearDown()
        while self.wd:
            self.layer.remove_working_dir(self.wd.pop())
            
    
    def create_repo(self):
        wd = tempfile.mkdtemp(dir=self.layer.working_dir)
        self.wd.append(wd)
        return git.Repo.init(wd)
    
    def test_base_dir(self):
        repo1 = self.create_repo()
        repo2 = self.create_repo()
        iterator = component.createObject(u"sparc.git.repos.repos_from_recursive_dir", self.layer.working_dir)
        iter_repos = list(iterator)
        self.assertEqual(set([repo1,repo2]), set(iter_repos))

class test_suite(test_suite_mixin):
    layer = SPARC_GIT_REPOS_DIR_INTEGRATION_LAYER
    package = 'sparc.git.repos'
    module = 'base_dir'
    
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
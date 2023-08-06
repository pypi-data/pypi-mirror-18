import os
import shutil
import unittest
import zope.testrunner
from zope import component
from sparc.testing.fixture import test_suite_mixin
from sparc.git.testing import SPARC_GIT_INTEGRATION_LAYER

import tempfile
from ..testing import yaml_StashConnection

class SparcGitStashRepoTestCase(unittest.TestCase):
    level = 2
    layer = SPARC_GIT_INTEGRATION_LAYER
    sm = component.getSiteManager()

    def setUp(self):
        self.working_dir = tempfile.mkdtemp()
        self.yaml_StashProjectRepos = {'StashConnection': yaml_StashConnection,
                                       'GitReposBaseDir': {
                                                'directory': self.working_dir
                                                             }
                                       }
        self.working_dir_repo_iterator = \
                        component.createObject(\
                                u'sparc.git.repos.repos_from_recursive_dir',
                                self.working_dir)
        
    def tearDown(self):
        if len(self.working_dir) < 3:
            print('ERROR: working directory less than 3 chars long, unable to clean up: %s' % str(self.working_dir))
            return
        shutil.rmtree(self.working_dir)
    
    def test_repos_iterator(self):
        yaml = self.yaml_StashProjectRepos
        yaml['include'] = {'PSO': ['testing_repo']}
        
        # some basic tests
        repo_iter = component.createObject(\
                        u'sparc.git.repos.stash.repos_iterator', yaml)
        repo_list = list(repo_iter)
        self.assertEquals(len(repo_list), 1)
        self.assertEquals(repo_list, 
                          list(self.working_dir_repo_iterator))
        
        # make sure a pre-init'd repo dir acts appropriately
        repo_list = list(repo_iter)
        self.assertEquals(len(repo_list), 1)
        self.assertEquals(repo_list, 
                          list(self.working_dir_repo_iterator))

class test_suite(test_suite_mixin):
    level = 2
    layer = SPARC_GIT_INTEGRATION_LAYER
    package = 'sparc.git'
    module = 'url'
    
    def __new__(cls):
        suite = super(test_suite, cls).__new__(cls)
        suite.addTest(unittest.makeSuite(SparcGitStashRepoTestCase))
        return suite

if __name__ == '__main__':
    zope.testrunner.run([
                         '--path', os.path.dirname(__file__),
                         '--tests-pattern', os.path.splitext(
                                                os.path.basename(__file__))[0]
                         ])
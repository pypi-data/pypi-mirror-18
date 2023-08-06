import os
import git
from zope import interface
from zope.component.factory import Factory
from sparc.git import repos

@interface.implementer(repos.IReposIterator)
class ReposIteratorForRecurisiveDir(object):
    def __init__(self, repos_base_dir):
        self.repos_base_dir = repos_base_dir

    def __iter__(self):
        for path, dirs, files in os.walk(self.repos_base_dir):
            try:
                repo = git.Repo(path)
                # since repo can be created from working dir path or .git sub-path,
                # we need to make sure we don't return the same repo twice
                l_char_trim_len = len(repo.working_dir) - len(path)
                if repo.working_dir[l_char_trim_len:] == path:
                    yield repo
                
            except git.InvalidGitRepositoryError:
                pass
            
        
reposIteratorForRecurisiveDirFactory = Factory(ReposIteratorForRecurisiveDir)
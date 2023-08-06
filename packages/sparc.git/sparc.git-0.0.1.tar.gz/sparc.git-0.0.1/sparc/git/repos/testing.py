import os
import tempfile
import git
import shutil
import sparc.git
from sparc.testing.testlayer import SparcZCMLFileLayer

class SparcGitReposDirZCMLFileLayer(SparcZCMLFileLayer):
    """
    In this layer, we need to stage and tear down sample git repos based
    on a directory layout
    """
    working_dir = tempfile.mkdtemp()
    git_dirs = []
    
    def remove_git_files(self, git_dir):
        # remove all git-related files
        pass
    
    def create_repo(self, git_dir):
        if os.path.exists(git_dir):
            raise EnvironmentError("did not expect path to exist: %s" % git_dir)
        return git.Repo.init(git_dir, bare=True)
    
    def create_repo_tracked_temp_file(self, repo):
        if not len(repo.working_tree_dir) > 1:
            raise ValueError("expected git working tree dir length > 1, got: %s" % str(repo.working_tree_dir))
        tfile = tempfile.NamedTemporaryFile(dir=repo.working_tree_dir)
        self.commit_tracked_file(repo, tfile, message="initial commit")
        return tfile
    
    def commit_tracked_file(self, repo, tfile, message="file commited"):
        repo.index.add([tfile.name])
        repo.index.commit(message)
    
    def replace_file_contents(self, tfile, contents):
        tfile.seek(0)
        tfile.write(contents)
        tfile.truncate()
        tfile.flush()

    def remove_working_dir(self, dir_=None):
        wd = self.working_dir if not dir_ else dir_
        if not wd:
            print('ERROR: working directory not set, unable to clean up')
            return
        if len(wd) < 3:
            print('ERROR: working directory less than 3 chars long, unable to clean up: %s' % str(wd))
            return
        shutil.rmtree(wd)

    def setUp(self):
        super(SparcGitReposDirZCMLFileLayer, self).setUp()

    def tearDown(self):
        super(SparcGitReposDirZCMLFileLayer, self).tearDown()
        self.remove_working_dir()
            
        
SPARC_GIT_REPOS_DIR_INTEGRATION_LAYER = SparcGitReposDirZCMLFileLayer(sparc.git)
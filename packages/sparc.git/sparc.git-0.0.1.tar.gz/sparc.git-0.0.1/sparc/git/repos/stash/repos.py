import git
import os
import requests
from stashy import Stash
from zope import component
from zope.component.factory import Factory
from zope import interface
from sparc.git import repos
from sparc.git.repos import stash

from sparc.configuration import container

# see http://docs.python-requests.org/en/master/user/advanced/
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.exceptions import SSLError
class Ssl3HttpAdapter(HTTPAdapter):
    """"Transport adapter" that allows us to use SSLv3."""

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_SSLv3)

def get_cloned_repo(base_dir, url, **kwargs):
    """Return a git.Repo within base_dir who is cloned from url
    
    This will search base_dir for git repos, each available repo will be 
    checked to see if it is a clone of url and the first match will be 
    returned.  If a match is not found, then url will be cloned into base_dir
    and returned.
    """
    local_repos = component.createObject(\
                                u'sparc.git.repos.repos_from_recursive_dir', 
                                base_dir)
    for repo in local_repos:
        for remote in repo.remotes:
            if remote.name != u'origin':
                continue
            if remote.url == url:
                return repo
    repo_dir_name = url.split('/').pop()
    return git.Repo.clone_from(\
                        url, os.path.join(base_dir, repo_dir_name) , **kwargs)

@interface.implementer(repos.IReposIterator)
class ReposIteratorFromYamlStashProjects(object):
    
    def __init__(self, yaml_config):
        """Init
        
        Args:
            yaml_config: a valid Python data structure from yaml.load().  Expects
                         to have either a StashProjectRepos entry, or assumes
                         a valid StashProjectRepos substructure.
        """
        self.yaml_config = yaml_config if 'StashProjectRepos' in yaml_config else {'StashProjectRepos': yaml_config}
    
    def __iter__(self):
        # iter through config entries
        v_iter = component.getUtility(container.ISparcPyDictValueIterator)
        for d in v_iter.values(self.yaml_config, 'StashProjectRepos'): #d is dict of StashProjects keys
            s = requests.Session()
            args = [d['StashConnection']['url']]
            kwargs = {'username': d['StashConnection']['username'],
                      'password': d['StashConnection']['password'],
                      'verify': d['StashConnection']['requests']['verify'],
                      'session': s}
            try:
                stash = Stash(*args, **kwargs)
            except SSLError:
                # small hack to see if a diff ssl version might fix the conn issue
                s.mount(d['StashConnection']['url'], Ssl3HttpAdapter())
                stash = Stash(*args, **kwargs)
            include_p = d['include'] if 'include' in d else []
            exclude_p = d['exclude'] if 'exclude' in d else []
            
            # iter through projects
            for prj_desc in stash.projects.list(): # returns dicts
                proj_key = prj_desc['key']
                include_r = include_p[proj_key] if proj_key in include_p else []
                exclude_r = exclude_p[proj_key] if proj_key in exclude_p else []
                
                if exclude_p:
                    if (proj_key in exclude_p) and not exclude_r:
                        continue
                if include_p:
                    if proj_key not in include_p:
                        continue
                    
                
                # iter through repos
                for repo_desc in stash.projects[proj_key].repos.list():
                    repo_name = repo_desc['name']
                    
                    if exclude_r and (repo_name in exclude_r):
                        continue
                    if include_r and (repo_name not in include_r):
                        continue
                    yield get_cloned_repo(\
                                d['GitReposBaseDir']['directory'], 
                                repo_desc['cloneUrl'])
                    
reposIteratorFromYamlStashProjectsFactory = Factory(ReposIteratorFromYamlStashProjects)


    
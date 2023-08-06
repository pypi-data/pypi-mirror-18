from zope import interface
from zope.component.factory import Factory
from .interfaces import IRepoUrl

@interface.implementer(IRepoUrl)
class RepoUrl(str):
    pass

repoUrlFactory = Factory(RepoUrl)
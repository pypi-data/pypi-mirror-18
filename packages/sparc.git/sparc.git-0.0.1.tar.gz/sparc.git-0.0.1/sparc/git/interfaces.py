from zope.interface import Interface

class IRepoUrl(Interface):
    """String-like object containing url reference to a git repo"""

class IRepo(Interface):
    """Marker for a git.Repo object"""

class ICommit(Interface):
    """Marker for git.Commit object"""

class IBlob(Interface):
    """Marker for git.Blob object"""
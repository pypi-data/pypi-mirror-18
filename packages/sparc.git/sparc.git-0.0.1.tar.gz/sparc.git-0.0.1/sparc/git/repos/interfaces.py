from zope.interface import Interface

class IReposIterator(Interface):
    """Iterator for IRepo objects"""
    def __iter__():
        """Iterator of objects providing IRepo"""


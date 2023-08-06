from zope import interface
from zope import proxy

from . import IZopeInterfaceProviderProxy

@interface.implementer(IZopeInterfaceProviderProxy)
class ZopeInterfaceProviderProxy(proxy.ProxyBase):
    """Proxy to allow interface assignment to types that won't allow attribute assignment
    """
    __slots__ = ('__provides__')
from zope import interface

class ISparcProxyProvider(interface.Interface):
    """Implements zope.proxy.AbstractPyProxyBase"""

class IZopeInterfaceProviderProxy(ISparcProxyProvider):
    """Proxy that allows object interface assignment"""
    __slots__ = interface.Attribute('__provides__')
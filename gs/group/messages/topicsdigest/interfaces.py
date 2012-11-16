# coding=utf-8
from zope.viewlet.interfaces import IViewletManager
from zope.interface import Interface
from gs.auth.token import AuthToken

class IDailyTopicsDigestHtmlVM(IViewletManager):
    ''' Viewlet manager for daily topics digests '''

class IDailyTopicsDigestTxtVM(IViewletManager):
    ''' Viewlet manager for daily topics digests '''

class IWeeklyTopicsDigestHtmlVM(IViewletManager):
    ''' Viewlet manager for weekly topics digests '''

class IWeeklyTopicsDigestTxtVM(IViewletManager):
    ''' Viewlet manager for weekly topics digests '''

class ISendAllDigests(Interface):
    '''Declares the form that will be used to send digests for all of the groups on the site. '''
    
    token = AuthToken(title=u'Token',
                      description=u'The authentication token',
                      required=True)

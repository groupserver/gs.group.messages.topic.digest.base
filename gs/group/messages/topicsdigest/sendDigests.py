# coding=utf-8
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form.form import SiteForm
from gs.auth.token import log_auth_error
from interfaces import ISendAllDigests
from notifiers import DynamicTopicsDigestNotifier

from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest.sendDigests')
FOLDER_TYPES = ['Folder', 'Folder (Ordered)']


class SendAllDigests(SiteForm):
    label = u'Send Digests for All Groups on the Site'
    pageTemplateFileName = 'browser/templates/send_all_digests.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(ISendAllDigests, render_context=False)

    def setUpWidgets(self, ignore_request=False):
        data = {'name': self.siteInfo.name, }
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context,
            self.request, form=self, data=data,
            ignore_request=ignore_request)

    @property
    def sites(self):
        '''All sites in a GroupServer instance'''
        # The digest sender sends digests for all groups the share the same
        # GroupServer *INSTANCE* as the site we currently on. This itterator
        # gets all the sites.
        # TODO: Put in a generic place (gs.site.base?)
        site_root = self.context.site_root()
        content = getattr(site_root, 'Content')
        sIds = content.objectIds(FOLDER_TYPES)
        for sId in sIds:
            s = getattr(content, sId)
            if s.getProperty('is_division', False) and hasattr(s, 'groups'):
                yield s

    def groups_for_site(self, site):
        '''An itterator for all groups on a site.'''
        # --=mpj17=-- I am using an itterator so we do not load all the group
        # instances into RAM in one hit. ('groupserver.GroupsInfo' needs to
        # be fixed so it treads lightly on RAM.)
        groups = getattr(site, 'groups')
        gIds = groups.objectIds(FOLDER_TYPES)
        for gId in gIds:
            g = getattr(groups, gId)
            if g.getProperty('is_group', False):
                yield g

    @form.action(label=u'Send', failure='handle_send_all_digests_failure')
    def handle_send_all_digests(self, action, data):
        log.info('Processing the digests')

        for site in self.sites:
            for group in self.groups_for_site(site):
                tdn = DynamicTopicsDigestNotifier(group, self.request)
                tdn.notify()

        log.info('All digests sent')
        self.status = u'<p>All digests sent.</p>'

    def handle_send_all_digests_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'

        assert type(self.status) == unicode

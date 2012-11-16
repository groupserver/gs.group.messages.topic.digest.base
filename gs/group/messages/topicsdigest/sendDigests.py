# coding=utf-8
from zope.formlib import form
from zope.component import createObject
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form.form import SiteForm
from gs.auth.token import log_auth_error
from interfaces import ISendAllDigests
from notifiers import DailyTopicsDigestNotifier

from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest.sendDigests')

class SendAllDigests(SiteForm):
    label = u'Send Digests for All Groups on the Site'
    pageTemplateFileName = 'browser/templates/send_all_digests.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(ISendAllDigests, render_context=False)

    def setUpWidgets(self, ignore_request=False):
        data = {'name': self.siteInfo.name,}
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context,
            self.request, form=self, data=data,
            ignore_request=ignore_request)

    @form.action(label=u'Send All Digests', failure='handle_send_all_digests_failure')
    def handle_send_all_digests(self, action, data):
        #Get A list of all groups, then loop through and call TopicsDigestNotifer for each
        #try:
            groupsInfo = createObject('groupserver.GroupsInfo', self.context)
            groups = groupsInfo.get_all_groups()
            for group in groups:
                tdn = DailyTopicsDigestNotifier(group, self.request)
                tdn.notify()
            self.status = u'<p>All Digests Sent</p>'
        except StandardError as e:
            #TODO set the error status for this form
            # How do I do this?
            log.exception(e)
            self.status = u'<p>An error occurred while sending digests. This error has been logged.</p>'

    def handle_send_all_digests_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        if len(errors) ==1:
            self.status = u'<p>There is an error:</p>'

        assert type(self.status) == unicode

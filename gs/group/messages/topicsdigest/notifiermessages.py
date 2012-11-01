# coding=utf-8
from gs.group.base.page import GroupPage

from logging import getLogger
log = getLogger('gs.group.messages.topicsdigest.notifiermessages')

# Classes used with page templates

class TopicsDigestMessage(GroupPage):
    pass

class TopicsDigestMessageText(TopicsDigestMessage):
    def __init__(self, context, request):
        TopicsDigestMessage.__init__(self, context, request)
        response = request.response
        response.setHeader("Content-Type", "text/plain; charset=UTF-8")

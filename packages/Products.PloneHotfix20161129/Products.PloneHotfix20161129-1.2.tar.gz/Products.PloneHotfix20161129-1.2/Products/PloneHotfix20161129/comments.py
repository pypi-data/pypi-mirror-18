from AccessControl import Unauthorized
from Acquisition import aq_parent
from plone.app.discussion.interfaces import IComment
from plone.indexer import indexer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import allowedRolesAndUsers
from Products.Five import BrowserView
from zope.component import getMultiAdapter

import logging

logger = logging.getLogger('Products.PloneHotfix20161129')


@indexer(IComment)
def comment_allowedRolesAndUsers(obj):
    portal_workflow = getToolByName(obj, 'portal_workflow')
    chain = portal_workflow.getChainForPortalType(obj.portal_type)
    if 'one_state_workflow' in chain:
        # In this case, we need to use parent roles.
        # Note that the acquisition chain is:
        # context / conversation / comment object
        # So we need the grandparent.
        parent = aq_parent(aq_parent(obj))
        return allowedRolesAndUsers(parent)()
    return allowedRolesAndUsers(obj)()


class ApplyHotfix(BrowserView):
    applied = False

    def upgrade(self):
        workflow_tool = getToolByName(self.context, "portal_workflow")
        catalog = getToolByName(self.context, 'portal_catalog')
        if 'comment_review_workflow' in workflow_tool:
            wf = workflow_tool['comment_review_workflow']
            if 'published' in wf.states:
                # Give View permission to no one.  This automatically turns on
                # 'Acquire permission settings'.
                wf.states['published'].permission_roles['View'] = []

        for brain in catalog.unrestrictedSearchResults(
                portal_type='Discussion Item'):
            try:
                comment = brain.getObject()
                comment.reindexObjectSecurity()
            except (AttributeError, KeyError):
                logger.info('Could not reindex comment %s' % brain.getURL())

    def __call__(self):
        if self.request.REQUEST_METHOD == 'POST':
            # do not assume they have latest plone.protect installed
            authenticator = getMultiAdapter((self.context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized

            self.upgrade()
            self.applied = True
        return self.index()


logger.info('You should call /@@apply-hotfix20161129 on all Plone Sites '
            'that have comments enabled.')

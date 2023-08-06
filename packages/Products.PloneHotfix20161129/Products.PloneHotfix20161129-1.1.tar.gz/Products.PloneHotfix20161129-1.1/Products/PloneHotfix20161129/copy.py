# Copysupport hotfix
#
# - Robert Niederreiter
# - Phil Auersperg
#
from AccessControl import getSecurityManager
from Acquisition import aq_base
from OFS.CopySupport import CopyError
from OFS.CopySupport import CopySource

import tempfile
import transaction


def CopySource_getCopy(self, container):
    transaction.savepoint(optimistic=True)
    if self._p_jar is None:
        raise CopyError(
            'Object "%s" needs to be in the database to be copied' % repr(
                self))
    if container._p_jar is None:
        raise CopyError(
            'Container "%s" needs to be in the database' % repr(container))
    f = tempfile.TemporaryFile()
    self._p_jar.exportFile(self._p_oid, f)
    f.seek(0)
    ob = container._p_jar.importFile(f)
    f.close()
    return self._cleanupCopy(ob)


def CopySource_cleanupCopy(self, cp):
    sm = getSecurityManager()
    ob = aq_base(self)
    if hasattr(ob, 'objectIds'):
        for k in self.objectIds():
            v = self._getOb(k)
            if not sm.checkPermission('View', v):
                # If we use cp._delOb, it is slightly faster, but fails on
                cp._delOb(k)
                # On Plone 3, we need to cleanup the internal objects list,
                # On Plone 4 or higher this is always an empty tuple.
                cp._objects = tuple([
                    i for i in cp._objects if i['id'] != k])
            else:
                # recursively check
                v._cleanupCopy(cp._getOb(k))
    return cp


CopySource._getCopy = CopySource_getCopy
CopySource._cleanupCopy = CopySource_cleanupCopy

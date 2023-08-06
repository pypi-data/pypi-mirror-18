import logging
import pkg_resources

logger = logging.getLogger('Products.PloneHotfix20161129')

# First import any current CMFPlone patches.
try:
    from Products.CMFPlone import patches  # noqa
except:
    pass

# General hotfixes for all.
hotfixes = [
    'publishing',
    'copy',
]

try:
    pkg_resources.get_distribution('plone.app.discussion')
except pkg_resources.DistributionNotFound:
    pass
else:
    # Not technically a hotfix, but this will print a line with extra
    # instructions.
    hotfixes.append('comments')

# Apply the fixes
for hotfix in hotfixes:
    try:
        __import__('Products.PloneHotfix20161129.%s' % hotfix)
        logger.info('Applied %s patch' % hotfix)
    except:
        logger.warn('Could not apply %s' % hotfix)
if not hotfixes:
    logger.info('No hotfixes were needed.')
else:
    logger.info('Hotfix installed')

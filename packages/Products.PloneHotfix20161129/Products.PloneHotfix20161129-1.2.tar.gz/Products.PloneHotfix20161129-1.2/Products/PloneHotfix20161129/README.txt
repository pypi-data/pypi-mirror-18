Plone hotfix, 2016-11-29
========================

This hotfix fixes several security issues:

- A user could copy a public folder containing a private document and be able to see the document in the copy.

- An anonymous user could see some settings of the site by accessing widgets directly.
  This is for z3c.form widgets, which are widely used in Plone.

- A comment on a private document would be partly visible in the live search.
  Access to the search result page would be denied if the results contained such a comment.
  This is for the plone.app.discussion commenting system introduced in Plone 4.1.
  See the required manual step below for further instructions.


Extra fixes
===========

- Related: a vulnerability in DTML was discovered that could allow Cross Site Scripting attacks (XSS).
  This vulnerability is *not* fixed by this hotfix, because this was not possible.
  An exploit is hard: an attacker would need to enter a character that cannot normally be entered on a keyboard.
  On Plone 4.1 and higher, you should use DocumentTemplate 2.13.3, which was released today.
  On Plone 4.0 and lower, DocumentTemplate was included in the Zope2 code, which will not get an updated release.

- The Zope Security Team fixed an issue where quoting of an SQL string could fail.
  The ZSQLMethods product is available in all Plone sites, but no core code uses it.
  An exploit is hard: an attacker would need to enter a character that cannot normally be entered on a keyboard.
  On Plone 4.0 and higher, you should use Products.ZSQLMethods 2.13.5, which was released a few weeks ago.
  On Plone 3.3 and lower, Products.ZSQLMethods was included in the Zope2 code, which will not get an updated release.


Required manual step
====================

The security issue about comments on private documents needs a change in the Plone configuration.
You need to login as Manager and call `/@@apply-hotfix20161129` on the root of the Plone Site.
This will display a form.
Click the button on the form and Plone will make a change in the workflow of comments, and reindex the security settings of comments.


Warning about 'Update security settings' limitation
===================================================

As a Plone administrator you may already know that you can change the settings of an existing workflow.
In the Zope Management Interface you can go to ``portal_workflow``, and change lots of permission settings for various states.
When you are done, you click the 'Update security settings' button, and Plone goes through the database and applies the changes to individual content items.
Mostly this means: update the information in the catalog, so that items only show up on the search results page or other listings when the user is allowed to see them.

For comments this does not work: they are not found by this procedure.
So if you have made a change in the workflow that makes comments invisible for everybody, they may still show up in a search.

This will likely get fixed in a future release of Plone.
As a workaround, once you have saved the workflow changes, you can use the form on `/@@apply-hotfix20161129`.

Note that in the Plone UI you can choose a different workflow for a type in the Content Settings controlpanel (or Types in earlier Plone versions).
This works fine for comments too, including updating the security settings.


Compatibility
=============

This hotfix should be applied to the following versions of Plone:

* Plone 5.0.6 and any earlier 5.x version
* Plone 4.3.11 and any earlier 4.x version
* Any older version of Plone

The hotfix is officially supported by the Plone security team on the
following versions of Plone in accordance with the Plone
`version support policy`_: 4.0.10, 4.1.6, 4.2.7, 4.3.11 and 5.0.6.
However it has also received some testing on older versions of Plone.
The fixes included here will be incorporated into subsequent releases of Plone,
so Plone 4.3.12, 5.0.7 and greater should not require this hotfix.


Installation
============

Installation instructions can be found at
https://plone.org/security/hotfix/20161129


Automated testing
=================

If you have automated tests for your code and you want to run them in combination with this hotfix, to see if there any regressions, you should make sure the hotfix is included in your test setup.
With plone.app.testing it should look something like this in your test layer fixture::


    def setUpZope(self, app, configurationContext):
        from plone.testing import z2
        z2.installProduct(app, 'Products.PloneHotfix20161129')

With the old-style Products.PloneTestCase it should be like this::

    from Testing import ZopeTestCase
    ZopeTestCase.installProduct('PloneHotfix20161129', quiet=1)


Q&A
===

Q: How can I confirm that the hotfix is installed correctly and my site is protected?
  A: On startup, the hotfix will log a number of messages to the Zope event log
  that look like this::

      2016-11-29 08:42:11 INFO Products.PloneHotfix20161129 Applied publishing patch
      2016-11-29 08:42:11 INFO Products.PloneHotfix20161129 Applied copy patch
      2016-11-29 08:42:11 INFO Products.PloneHotfix20161129 Applied comments patch
      2016-11-29 08:42:11 INFO Products.PloneHotfix20161129 You should call /@@apply-hotfix20161129 on all Plone Sites that have comments enabled.
      2016-11-29 08:42:11 INFO Products.PloneHotfix20161129 Hotfix installed

  The exact number of patches applied, will differ depending on what packages you are using.
  If a patch is attempted but fails, it will be logged as a warning that says
  "Could not apply". This may indicate that you have a non-standard Plone
  installation.

Q: How can I report problems installing the patch?
  A: Contact the Plone security team at security@plone.org, or visit the
  #plone channel on freenode IRC.

Q: How can I report other potential security vulnerabilities?
  A: Please email the security team at security@plone.org rather than discussing
  potential security issues publicly.

.. _`version support policy`: http://plone.org/support/version-support-policy

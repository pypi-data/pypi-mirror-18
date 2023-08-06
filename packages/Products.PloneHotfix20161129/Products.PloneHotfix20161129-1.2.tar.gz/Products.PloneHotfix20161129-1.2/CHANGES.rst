Changelog
=========

1.2 (2016-11-29)
----------------

- Handle issue where not all comments on multilingual sites were reindexed.
  [maurits]


1.1 (2016-11-29)
----------------

- handle issue where the comment upgrade would fail if a comment was in the
  catalog but removed from the site. You only need to upgrade to this version
  of the patch if you get an AttributeError running the commenting patch
  on the site.
  [vangheem]

1.0 (2016-11-29)
----------------

- Initial release

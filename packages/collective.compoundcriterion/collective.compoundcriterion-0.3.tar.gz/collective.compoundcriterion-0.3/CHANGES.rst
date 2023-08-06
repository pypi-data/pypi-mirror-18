Changelog
=========


0.3 (2016-12-08)
----------------

- Return clear message when a query format is not plone.app.querystring compliant.
  [gbastien]


0.2 (2015-09-04)
----------------

- Raise a KeyError if the format of the query returned by the named adapter
  is not compliant with what is returned by
  plone.app.querystring.queryparser.parseFormquery, this way it behaves
  correctly with collective.eeafaceted.collectionwidget.
  [gbastien]


0.1 (2015-06-02)
----------------

- Initial release.
  [IMIO]

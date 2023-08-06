# encoding: utf-8

from collective.compoundcriterion.interfaces import ICompoundCriterionFilter
from zope.component import queryAdapter


def _filter_is(context, row):
    named_adapter = queryAdapter(context,
                                 ICompoundCriterionFilter,
                                 name=row.values)
    if named_adapter:
        # check that query is plone.app.querystring compliant
        # the value needs to be defined with a 'query' dict like :
        # {
        #  'portal_type':
        #  {'query': ['portal_type1', 'portal_type2']},
        #  'created':
        #  {'query': DateTime('2015/05/05'),
        #   'range': 'min'},
        # }
        for term in named_adapter.query.values():
            if not isinstance(term, dict) or \
               'query' not in term:
                raise ValueError(
                    "The query format returned by '{0}' named adapter "
                    "is not plone.app.querystring compliant !".format(row.values))
        return named_adapter.query
    return {}

.. image:: https://travis-ci.org/IMIO/collective.compoundcriterion.svg?branch=master
   :target: https://travis-ci.org/IMIO/collective.compoundcriterion

.. image:: https://coveralls.io/repos/IMIO/collective.compoundcriterion/badge.png?branch=master
  :target: https://coveralls.io/r/IMIO/collective.compoundcriterion?branch=master



====================
collective.compoundcriterion
====================

This package add a new kind of criterion available for plone.app.collection.

Motivation
----------

Sometimes, some index are composed of different elements with a certain logic or you need to query particular elements of the site like groups of the current user or anything else.
This is not achievable using default indexes and Collection UI, you need to write python code.

How to use
----------

When adding/editing a Collection, a new criterion filed under the 'Other' category of available indexes called 'Filter' is available.

When selecting a 'Filter', a selection box will show you named adapter that provide the collective.compoundcriterion.interfaces.ICoumpondCriterionFilter interface.

You will be able to select among available ones.  This can still be used together with other criteria.

To register this complex query builder named adapter, you will have to add this kind of code :

.. code:: xml

   <adapter for="*"
            factory="collective.compoundcriterion.tests.adapter.CompoundCrietrionFilterAdapter"
            provides="collective.compoundcriterion.interfaces.ICompoundCriterionFilter"
            name="testing-compound-adapter" />
 
How to test
-----------

Add the adapter registration zcml here above to a configure.zcml file (like the one in collective.compoundcriterion), it will make the 'testing-compound-adapter' available in the Collection 'Filter' index.

This testing adapter will query elements of the site having string 'special_text_to_find' in the title.  So create a document with such title and it should work.

A second adapter can be used to test :

.. code:: xml

    <adapter for="*"
             factory="collective.compoundcriterion.tests.adapter.SampleCompoundCrietrionFilterAdapter"
             provides="collective.compoundcriterion.interfaces.ICompoundCriterionFilter"
             name="sample-compound-adapter" />

This one will query elements having 'title_with_sample_text' in the title.

ftw.referencewidget
===================

This Widget provides a Referencebrowser and a searchfield, which allows users to select references.

The basequery is all types which are not in the types_not_searched property all modification to the allowed types are relative to this query.

Traversal or Selectability can be changed for all widgets with the IReferenceSettings registry interface or per widget with the widget parameters.

The widget takes the following parameters:
 - allow_traversal: These Types are traversable
 - block_traversal: These Types are not traversable
 - selectable: These Types are selectable
 - nonselectable: These Types are not selectable
 - start: The path first opened. Can either be a callable or a path. Additionaly the strings "parent", "navroot", "ploneroot" can be used.
 - allow_nonsearched_types: If this is set to true all the types will be traversable and selectable.
 - override: drops all global config and the base query if a list is passed to the widget. All types need to be added to be selectable.


**IMPORTANT NOTE:**
Currently this widget drops the SourceBinder concept, which has huge impact on the usability.

The following combinations are supported.
- RelationList with value_type Relation --> Stores a List of RelationValues
- RelationList with value_type RelationChoice --> Stores a List of RelationValues
- Relation --> Stores a RelationValue
- List of RelationChoice --> Stores a list of absolute paths, without the portal root part
- TextLine --> Stores a absolute path as string, without the portal root part



TODO
----

- The SourceBinder concept needs to be implemented for better compatibility with everything/everyone else.
- Proper Integration Tests using test behaviors with several configurations.


Screenshots
-----------
The general Listing:
![Listing](https://github.com/4teamwork/ftw.referencewidget/raw/master/docs/static/list.png)
The Search Listing:
![Search Listing](https://github.com/4teamwork/ftw.referencewidget/raw/master/docs/static/search.png)
The Selected Items
![Selected](https://github.com/4teamwork/ftw.referencewidget/raw/master/docs/static/selected.png)

Links
-----

- Github: https://github.com/4teamwork/ftw.referencewidget
- Issues: https://github.com/4teamwork/ftw.referencewidget/issues
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.referencewidget


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.referencewidget`` is licensed under GNU General Public License, version 2.

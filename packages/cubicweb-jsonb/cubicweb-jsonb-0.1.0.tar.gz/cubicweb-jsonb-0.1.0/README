Summary
-------

Add a new attribue type to CubicWeb: ``Jsonb``. This type is mapped to the
`jsonb PostgreSQL data type`_.

Declaration
~~~~~~~~~~~

In your schemas, you can use the new type as follow::

    >>> class MyEntityType(EntityType):
    ...     json_attribute = Jsonb(required=True)
    ...

Get/Set
~~~~~~~

To provide a value for a Jsonb attribute, you can use either:

* a dict,
* a JSON string.

For example, you can write the following code::

    >>> my_entity.cw_set(json_attribute={'a': [1, 2, 3]})

The code below wil have exactly the same effect::

   >>> my_entity.cw_set(json_attribute=u'{"a": [1, 2, 3]}')

Please note that, whatever way you set the value (string or dict), you will
always get back a dict when asking for it::

   >>> my_entity.json_attribute
   {u'a': [1, 2, 3]}


Querying
~~~~~~~~

In RQL, you can query a Jsonb attribute in multiple ways. For example, you can
ask for attributes containing a specific key/value pair::

    >>> import json
    >>> rql('Any X WHERE X json_attribute J HAVING JSONB_CONTAINS(J, %(json_value)s)=True',
            {'json_value': json.dumps({u'a': 1})})

You can ask for existence of a specific key::

    >>> rql('Any X WHERE X json_attribute J HAVING JSONB_EXISTS(J, %(key)s)=True',
            {'key': u'b'})

You can get the value for a key::

    >>> rql('Any JSONB_GET(J, %(key)s) WHERE X json_attribute J, X eid %(eid)s',
            {'key': u'a', 'eid': 1234})

Note: ``JSONB_GET()`` will *always* return a string. If the value is a JSON
object (or a JSON array), you may want to use ``json.loads()`` afterwards to
have a dict (or a list).

One final remark: as the PostgreSQL documentation suggests, you should use the
same structure for your JSON data in the same column. This makes querying much
easier.

.. _jsonb PostgreSQL data type: https://www.postgresql.org/docs/9.4/static/datatype-json.html

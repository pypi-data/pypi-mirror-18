# -*- coding: utf-8 -*-
# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""Register the new type."""

from six import string_types
import json

from logilab.database import FunctionDescr, get_db_helper
from logilab.database.sqlgen import SQLExpression
from rql.utils import register_function
from yams import register_base_type


#
# Jsonb type
#

def convert_jsonb(x):
    if isinstance(x, SQLExpression):
        return x
    elif isinstance(x, string_types):
        try:
            json.loads(x)
        except (ValueError, TypeError):
            raise ValueError(u'Invalid JSON value: {0}'.format(x))
        return SQLExpression('%(json_obj)s::jsonb', json_obj=x)
    return SQLExpression('%(json_obj)s::jsonb', json_obj=json.dumps(x))


# Register the new type
register_base_type('Jsonb')

# Map the new type with PostgreSQL
pghelper = get_db_helper('postgres')
pghelper.TYPE_MAPPING['Jsonb'] = 'jsonb'
pghelper.TYPE_CONVERTERS['Jsonb'] = convert_jsonb

# Map the new type with SQLite3
sqlitehelper = get_db_helper('sqlite')
sqlitehelper.TYPE_MAPPING['Jsonb'] = 'text'
sqlitehelper.TYPE_CONVERTERS['Jsonb'] = json.dumps


#
# Querying jsonb
#

class JSONB_ARRAY_ELEMENTS(FunctionDescr):
    minargs = 1
    maxargs = 1
    supported_backends = ('postgres',)
    rtype = 'Jsonb'


class JSONB_CONTAINS(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Bool'

    def as_sql_postgres(self, args):
        return u'{0}::jsonb @> {1}::jsonb'.format(*args)


class JSONB_EXISTS(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'Bool'

    def as_sql_postgres(self, args):
        return u'{0}::jsonb ? {1}'.format(*args)


class JSONB_GET(FunctionDescr):
    minargs = 2
    maxargs = 2
    supported_backends = ('postgres',)
    rtype = 'String'

    def as_sql_postgres(self, args):
        return u'{0}->>{1}'.format(*args)


register_function(JSONB_ARRAY_ELEMENTS)
register_function(JSONB_CONTAINS)
register_function(JSONB_EXISTS)
register_function(JSONB_GET)

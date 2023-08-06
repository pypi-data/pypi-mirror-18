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
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-jsonb postcreate script, executed at instance creation time or when
the cube is added to an existing instance.

You could setup site properties or a workflow here for example.
"""

# Create indexes for all Jsonb attributes in schema

def json_rdefs():
    for rschema in schema.relations():
        for subj_etype, obj_etype in rschema.rdefs:
            if obj_etype == 'Jsonb':
                yield rschema.rdef(subj_etype, obj_etype)


dbdriver = config.system_source_config['db-driver']
if dbdriver == 'postgres':  # These indexes only exists in Postgres
    for rdef in json_rdefs():
        etype, attr = rdef.subject.type, rdef.rtype.type
        table, col = 'cw_{0}'.format(etype.lower()), 'cw_{0}'.format(attr)
        idxname = '{0}_{1}_idx'.format(table, attr)
        query = 'DROP INDEX IF EXISTS {0}'.format(idxname)
        sql(query)
        query = 'CREATE INDEX {0} ON {1} USING gin({2})'.format(idxname, table, col)
        sql(query)

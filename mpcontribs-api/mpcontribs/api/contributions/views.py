import re
import os
import flask_mongorest
from flask import Blueprint
from flask_mongorest.resources import Resource
from flask_mongorest import operators as ops
from flask_mongorest.methods import List, Fetch, Create, Delete, Update, BulkUpdate
from mpcontribs.api.core import SwaggerView
from mpcontribs.api.contributions.document import Contributions
from mpcontribs.api.structures.document import Structures
from mpcontribs.api.tables.document import Tables

templates = os.path.join(
    os.path.dirname(flask_mongorest.__file__), 'templates'
)
contributions = Blueprint("contributions", __name__, template_folder=templates)


class ContributionsResource(Resource):
    document = Contributions
    filters = {
        'project': [ops.In, ops.Exact],
        'identifier': [ops.In, ops.Contains, ops.Exact],
        'is_public': [ops.Boolean],
        re.compile(r'^(data__)((?!__).)*$'): [ops.Contains]
    }
    fields = ['id', 'project', 'identifier', 'is_public']
    allowed_ordering = ['project', 'identifier', 'is_public']
    paginate = True
    default_limit = 20
    max_limit = 200
    bulk_update_limit = 100

    @staticmethod
    def get_optional_fields():
        return ['data', 'structures', 'tables']

    def value_for_field(self, obj, field):
        # add structures and tables info to response if requested
        if field == 'structures':
            structures = Structures.objects.only('id', 'name').filter(project=obj.project, contribution=obj.id)
            return [{'id': s.id, 'name': s.name} for s in structures]
        elif field == 'tables':
            tables = Tables.objects.only('id', 'name').filter(project=obj.project, contribution=obj.id)
            return [{'id': t.id, 'name': t.name} for t in tables]
        else:
            raise UnknownFieldError

class ContributionsView(SwaggerView):
    resource = ContributionsResource
    methods = [List, Fetch, Create, Delete, Update, BulkUpdate]

    # TODO unpack display from dict
    # https://github.com/tschaume/flask-mongorest/blob/9a04099daf9a93eefd6fd2ee906c29ffbb87789f/flask_mongorest/resources.py#L401
    # unflatten(dict(
    #     (k, v) for k, v in get_cleaned_data(<serialize_dict_field>).items()
    # ))

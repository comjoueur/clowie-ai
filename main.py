from flask import Flask, redirect

from resources.api.entity import create_entity_resource, get_all_entities_resource, delete_entity_resource
from resources.api.entity_entry import create_entity_entry_resource, delete_entity_entry_resource, get_all_entries_resource
from resources.api.source import create_source_resource, get_all_sources_resource, delete_source_resource
from resources.api.restaurant import create_restaurant_resource, get_all_restaurants_resource, delete_restaurant_resource
from resources.api.mixed import delete_all_indices_docs

from resources.api.app.restaurant_filtering import restaurant_filtering
from resources.api.app.playground import playground_resource
from resources.api.app.playground_v2 import playground_resource_v2
from resources.api.app.playground_v3 import playground_resource_v3

from resources.pages.source import create_source_page, delete_source_page
from resources.pages.entity import create_entity_page, delete_entity_page
from resources.pages.entity_entry import create_entity_entry_page, delete_entry_page
from resources.pages.mixed import list_resources_page, delete_all_indices_docs_page
from resources.pages.app.playground import playground_page
from resources.pages.app.playground_v2 import playground_page_v2
from resources.pages.app.playground_v3 import playground_page_v3
from resources.pages.restaurant import create_restaurant_page, delete_restaurant_page

app = Flask(__name__)

app.add_url_rule('/api/entity',
                 view_func=create_entity_resource,
                 methods=['POST'])
app.add_url_rule('/api/entity/<entity_id>/entry',
                 view_func=create_entity_entry_resource,
                 methods=['POST'])
app.add_url_rule('/api/source',
                 view_func=create_source_resource,
                 methods=['POST'])
app.add_url_rule('/api/sources/list',
                 view_func=get_all_sources_resource,
                 methods=['GET'])
app.add_url_rule('/api/entity/list',
                 view_func=get_all_entities_resource,
                 methods=['GET'])
app.add_url_rule('/api/delete_all_indices_docs',
                 view_func=delete_all_indices_docs,
                 methods=['DELETE'])
app.add_url_rule('/api/entity/<entity_id>',
                 view_func=delete_entity_resource,
                 methods=['DELETE'])
app.add_url_rule('/api/source/<source_id>',
                 view_func=delete_source_resource,
                 methods=['DELETE'])
app.add_url_rule('/api/entity/entry/list',
                 view_func=get_all_entries_resource,
                 methods=['GET'])
app.add_url_rule('/api/entity/entry/<entry_id>',
                 view_func=delete_entity_entry_resource,
                 methods=['DELETE'])
app.add_url_rule('/api/restaurant',
                 view_func=create_restaurant_resource,
                 methods=['POST'])
app.add_url_rule('/api/restaurant/list',
                 view_func=get_all_restaurants_resource,
                 methods=['GET'])
app.add_url_rule('/api/restaurant/<restaurant_id>',
                 view_func=delete_restaurant_resource,
                 methods=['DELETE'])
"""

App Resources

"""
app.add_url_rule('/api/app/restaurant_filtering',
                 view_func=restaurant_filtering,
                 methods=['GET'])
app.add_url_rule('/api/app/playground',
                 view_func=playground_resource,
                 methods=['POST'])
app.add_url_rule('/api/app/playground_v2',
                 view_func=playground_resource_v2,
                 methods=['POST'])
app.add_url_rule('/api/app/playground_v3',
                 view_func=playground_resource_v3,
                 methods=['POST'])
"""

Pages Resources

"""

app.add_url_rule('/pages/create-source',
                 view_func=create_source_page,
                 methods=['GET'])
app.add_url_rule('/pages/create-entity',
                 view_func=create_entity_page,
                 methods=['GET'])
app.add_url_rule('/pages/create-entity-entry',
                 view_func=create_entity_entry_page,
                 methods=['GET'])
app.add_url_rule('/pages', view_func=list_resources_page, methods=['GET'])
app.add_url_rule('/pages/delete-all-indices-docs',
                 view_func=delete_all_indices_docs_page,
                 methods=['GET'])
app.add_url_rule('/pages/delete-source',
                 view_func=delete_source_page,
                 methods=['GET'])
app.add_url_rule('/pages/delete-entity',
                 view_func=delete_entity_page,
                 methods=['GET'])
app.add_url_rule('/pages/delete-entity-entry',
                 view_func=delete_entry_page,
                 methods=['GET'])
app.add_url_rule('/pages/create-restaurant',
                 view_func=create_restaurant_page,
                 methods=['GET'])
app.add_url_rule('/pages/delete-restaurant',
                 view_func=delete_restaurant_page,
                 methods=['GET'])
app.add_url_rule('/pages/playground',
                 view_func=playground_page,
                 methods=['GET'])
app.add_url_rule('/pages/playground_v2',
                 view_func=playground_page_v2,
                 methods=['GET'])
app.add_url_rule('/pages/playground_v3',
                 view_func=playground_page_v3,
                 methods=['GET'])

app.add_url_rule('/', view_func=lambda: redirect('/pages'), methods=['GET'])

app.run(host='0.0.0.0', port=81)

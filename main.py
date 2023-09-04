from flask import Flask
import resources

app = Flask(__name__)

app.add_url_rule('/api/entity',
                 view_func=resources.api.entry.create_entity_resource,
                 methods=['POST'])
app.add_url_rule(
  '/api/entity-entry',
  view_func=resources.api.entity_entry.create_entity_entry_resource,
  methods=['POST'])

app.run(host='0.0.0.0', port=81)

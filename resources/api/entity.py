from flask import request, jsonify
from schemas.entity import CreateEntitySchema
from models.entity import EntityModel


def create_entity_resource():
  entity_data = CreateEntitySchema().load(request.get_json())
  es_response = EntityModel.create(entity_data)
  return jsonify(es_response)

def get_entity_resource(entity_id):
  entity = EntityModel.get_by_id(entity_id)
  return jsonify(entity)

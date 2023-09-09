from flask import request, jsonify
from schemas.entity import CreateEntitySchema
from models.entity import EntityModel


def create_entity_resource():
  try:
    entity_data = CreateEntitySchema().load(request.get_json())
  except Exception as e:
    return jsonify({"error": str(e)}), 400
  es_response = EntityModel.create(entity_data)
  return jsonify(es_response)


def get_entity_resource(entity_id):
  entity = EntityModel.get_by_id(entity_id)
  return jsonify(entity)


def get_all_entities_resource():
  entities = EntityModel.get_all()
  return jsonify(entities)


def delete_entity_resource(entity_id):
  EntityModel.delete_by_id(entity_id)
  return jsonify({"message": "Entity deleted"})

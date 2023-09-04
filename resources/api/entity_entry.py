from flask import request, jsonify
from schemas.entity import CreateEntityEntrySchema
from models.entity_entry import EntityEntryModel
from models.entity import EntityModel


def create_entity_entry_resource(entity_id):
  entry_data = CreateEntityEntrySchema().load(request.get_json())
  entity = EntityModel.get_by_id(entry_data['entity_id'])
  print(entity)
  return jsonify(entity)

  summary = "\n".join([
    "description: " + entry_data.get("description"),
    "address: " + entry_data.get("address"),
    "typeOfFood: " + entry_data.get("typeOfFood"),
    "rating: " + str(entry_data.get("rating"))
  ])
  entry_data["summary"] = summary
  entry_data["entity_id"] = entity_id
  es_response = EntityEntryModel.create(entry_data)
  return jsonify(es_response)

def get_entity_entry_resource(entity_id, entry_id):
  entry = EntityEntryModel.get_by_id(entity_id, entry_id)
  return jsonify(entry)

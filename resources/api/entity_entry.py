from flask import request, jsonify
from schemas.entity_entry import CreateEntityEntrySchema
from models.entity_entry import EntityEntryModel
from models.entity import EntityModel
from models.source import SourceModel


def create_entity_entry_resource(entity_id):
  try:
    entry_data = CreateEntityEntrySchema().load(request.get_json())
  except Exception as e:
    return jsonify({"error": str(e)}), 400

  entity = EntityModel.get_by_id(entity_id)
  source = SourceModel.get_by_id(entry_data['source_id'])

  summary = "\n\n".join([
    "name: " + entity['_source']['name'],
    "price_range" + str(entity['_source']['minPrice']) + ' - ' +
    str(entity['_source']['maxPrice']),
    "description: " + entry_data.get("description", ""),
    "address: " + entry_data.get("address", ""),
    "typeOfFood: " + entry_data.get("typeOfFood", ""),
    "rating: " + str(entry_data.get("rating", "")),
    "typeOfPlace: " + entry_data.get("typeOfPlace", ""),
  ])
  entry_data["summary"] = summary
  entry_data["entity_id"] = entity_id
  entry_data["entityName"] = entity["_source"]["name"]
  entry_data["sourceName"] = source["_source"]["name"]
  entry_data["minPrice"] = entity["_source"]["minPrice"]
  entry_data["maxPrice"] = entity["_source"]["maxPrice"]
  es_response = EntityEntryModel.create(entry_data)
  return jsonify(es_response)


def delete_entity_entry_resource(entry_id):
  EntityEntryModel.delete_by_id(entry_id)
  return jsonify({"message": "Entry deleted"})


def get_all_entries_resource():
  entries = EntityEntryModel.get_all()
  for entry in entries:
    entity = EntityModel.get_by_id(entry["_source"]["entity_id"])
    entry["entity"] = entity["_source"]["name"]
    source = SourceModel.get_by_id(entry["_source"]["source_id"])
    entry["source"] = source["_source"]["name"]
  return jsonify(entries)

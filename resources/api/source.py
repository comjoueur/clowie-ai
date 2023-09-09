from flask import request, jsonify
from schemas.source import SourceSchema
from models.source import SourceModel


def create_source_resource():
  try:
    source_data = SourceSchema().load(request.get_json())
  except Exception as e:
    return jsonify({"error": str(e)}), 400
  es_response = SourceModel.create(source_data)
  return jsonify(es_response)


def get_entity_resource(source_id):
  entity = SourceModel.get_by_id(source_id)
  return jsonify(entity)


def get_all_sources_resource():
  entities = SourceModel.get_all()
  return jsonify(entities)


def delete_source_resource(source_id):
  SourceModel.delete_by_id(source_id)
  return jsonify({"message": "Source deleted"})

from flask import request, jsonify
from models.entity_entry import EntityEntryModel


def restaurant_filtering():
  budget_per_dinner = request.args.get('budget_per_dinner')
  preferred_type = request.args.get('preferred_type')
  preferred_cuisine = request.args.get('preferred_cuisine')
  user_suggestion = request.args.get('user_suggestion')

  entries = EntityEntryModel.search_by_type_id_and_suggestion(budget_per_dinner, preferred_type, preferred_cuisine, user_suggestion)

  return jsonify(entries)

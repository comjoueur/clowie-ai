from flask import request, jsonify
from models.restaurant import RestaurantModel
from schemas.restaurant import CreateRestaurantSchema


def get_all_restaurants_resource():
  restaurants = RestaurantModel.get_all()
  return jsonify(restaurants)


def get_restaurant_resource(restaurant_id):
  restaurant = RestaurantModel.get_by_id(restaurant_id)
  return jsonify(restaurant)


def create_restaurant_resource():
  try:
    restaurant_data = CreateRestaurantSchema().load(request.get_json())
  except Exception as e:
    return jsonify({"error": str(e)}), 400
  # format restaurant data in a key: value and join by \n
  summary = "\n".join([
    f"{key}: {value}" for key, value in restaurant_data.items()
    if value is not None
  ])
  meals_list = ",".join(restaurant_data.get("meals"))
  weekdays_list = ",".join(restaurant_data.get("weekdays"))

  restaurant_payload = {
    **restaurant_data,
    "summary": summary,
    "meals_list": meals_list,
    "weekdays_list": weekdays_list,
  }
  es_response = RestaurantModel.create(restaurant_payload)
  return jsonify(es_response)


def delete_restaurant_resource(restaurant_id):
  RestaurantModel.delete_by_id(restaurant_id)
  return jsonify({"message": "Restaurant deleted successfully"})

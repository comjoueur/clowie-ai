from flask import request, jsonify
from schemas.app.playground_v3 import PlaygroundSchemaV3
from models.restaurant import RestaurantModel
import openai
import settings

openai.api_key = settings.OPENAI_API_KEY


def playground_resource_v3():
  try:
    input_data = PlaygroundSchemaV3().load(request.get_json())
  except Exception as e:
    return jsonify({"error": str(e)}), 400

  preOpenAIresponseES = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[{
      "role":
      "user",
      "content":
      "You are a helpful assistant that divides the user prompt into individual commands. Instead of listing them, separate each command after the other separated by a comma: \n\n"
      + input_data["userSuggestion"]
    }],
    temperature=1,
    max_tokens=512,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
  )
  user_key_words = [
    key_word.strip() for key_word in preOpenAIresponseES['choices'][0]
    ['message']['content'].split(',')
  ]

  restaurants = RestaurantModel.search_by_type_suggestion_day_meal_v3(
    input_data["budgetPerDinner"],
    user_key_words,
    input_data["startTime"],
    input_data["numberOfDays"],
    input_data["meals"],
  )

  return jsonify({"restaurants": restaurants, "key_words": user_key_words})

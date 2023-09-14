from flask import request, jsonify
from schemas.app.playground_v2 import PlaygroundSchemaV2
from models.restaurant import RestaurantModel
from resources.api.app.utils import generate_meals_schedule
import openai
import settings
import tiktoken

WEEK_DAYS = [
  "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]
openai.api_key = settings.OPENAI_API_KEY


def num_tokens_from_string(string: str, encoding_name: str) -> int:
  encoding = tiktoken.encoding_for_model(encoding_name)
  num_tokens = len(encoding.encode(string))
  return num_tokens


def playground_resource_v2():
  try:
    input_data = PlaygroundSchemaV2().load(request.get_json())
  except Exception as e:
    return jsonify({"error": str(e)}), 400

  meals_schedule = generate_meals_schedule(
    input_data["numberOfDays"],
    input_data["startTime"],
    input_data["meals"],
  )

  preOpenAIresponseES = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
      {
        "role":
        "system",
        "content":
        "You are a helpful assistant whose job is to extract key words (split by commas) from long texts to inject into Elastic Search to use text_expansion",
      },
      {
        "role":
        "user",
        "content":
        "Please read the following requirements from a user that wants restaurant recommendations and extract the most important key words (split by commas) that we can the use to filter out restaurants:\n\n"
        + input_data["userSuggestion"] + "\n\n",
      },
    ],
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

  restaurants = RestaurantModel.search_by_type_suggestion_day_meal(
    input_data["budgetPerDinner"],
    user_key_words,
    input_data["startTime"],
    input_data["numberOfDays"],
    input_data["meals"],
  )

  list_of_entries = "\n\n".join(
    [entry["_source"]["summary"] for entry in restaurants])

  system_message = input_data["openaiSystemMessage"]
  system_message = system_message.replace("{user_selected_days}",
                                          meals_schedule)
  system_message = system_message.replace("{user_suggestion}",
                                          input_data["userSuggestion"])
  system_message = system_message.replace("{list_of_entries}", list_of_entries)

  user_prompt = input_data["openaiPrompt"]
  user_prompt = user_prompt.replace("{user_selected_days}", meals_schedule)
  user_prompt = user_prompt.replace("{user_suggestion}",
                                    input_data["userSuggestion"])
  user_prompt = user_prompt.replace("{list_of_entries}", list_of_entries)

  print(
    "openaiinput",
    num_tokens_from_string(system_message + user_prompt, "gpt-3.5-turbo-16k"))

  openAIresponse = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
      {
        "role": "system",
        "content": system_message,
      },
      {
        "role": "user",
        "content": user_prompt,
      },
    ],
    temperature=1,
    max_tokens=2500,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
  )
  response = openAIresponse['choices'][0]['message']['content']
  print("openaioutput", num_tokens_from_string(response, "gpt-3.5-turbo-16k"))

  print([
    {
      "role": "system",
      "content": system_message,
    },
    {
      "role": "user",
      "content": user_prompt,
    },
  ])

  return jsonify({
    "response":
    response,
    "entries":
    "<br><br>".join([
      "week_day: " + restaurant["week_day"] + "<br>" + "meal: " +
      restaurant["meal"] + "<br>" + "key_word:" + restaurant["key_word"] +
      "<br>" + restaurant["_source"]["summary"] for restaurant in restaurants
    ]),
    "messages": [
      {
        "role": "system",
        "content": system_message,
      },
      {
        "role": "user",
        "content": user_prompt,
      },
    ]
  })

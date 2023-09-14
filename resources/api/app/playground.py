from flask import request, jsonify
from schemas.app.playground import PlaygroundSchema
from resources.api.app.utils import generate_meals_schedule
from models.entity_entry import EntityEntryModel
import openai
import settings
import tiktoken

openai.api_key = settings.OPENAI_API_KEY


def num_tokens_from_string(string: str, encoding_name: str) -> int:
  encoding = tiktoken.encoding_for_model(encoding_name)
  num_tokens = len(encoding.encode(string))
  return num_tokens


def playground_resource():
  try:
    input_data = PlaygroundSchema().load(request.get_json())
  except Exception as e:
    return jsonify({"error": str(e)}), 400

  meals_schedule = generate_meals_schedule(
    input_data["numberOfDays"],
    input_data["startTime"],
    input_data["meals"],
  )

  print(meals_schedule)
  preferred_type = ", ".join(input_data["preferredType"])

  entries = EntityEntryModel.search_by_type_id_and_suggestion(
    input_data["budgetPerDinner"],
    preferred_type,
    input_data["userSuggestion"],
    input_data["esPrompt"],
  )

  list_of_entries = "\n".join(
    [entry["_source"]["summary"] for entry in entries])

  system_message = input_data["openaiSystemMessage"]
  system_message = system_message.replace("{user_selected_days}",
                                          meals_schedule)
  system_message = system_message.replace("{preferred_type}", preferred_type)
  system_message = system_message.replace("{user_suggestion}",
                                          input_data["userSuggestion"])
  system_message = system_message.replace("{list_of_entries}", list_of_entries)

  user_prompt = input_data["openaiPrompt"]
  user_prompt = user_prompt.replace("{user_selected_days}", meals_schedule)
  user_prompt = user_prompt.replace("{preferred_type}", preferred_type)
  user_prompt = user_prompt.replace("{user_suggestion}",
                                    input_data["userSuggestion"])
  user_prompt = user_prompt.replace("{list_of_entries}", list_of_entries)

  print(
    "openaiinput",
    num_tokens_from_string(system_message + user_prompt, "gpt-3.5-turbo-16k"))

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

  return jsonify({
    "response":
    response,
    "entries":
    "<br><br>".join([entry["_source"]["summary"] for entry in entries])
  })

from flask import request, jsonify
from models.entity_entry import EntityEntryModel
import openai
import settings
import datetime

PROMPT = """
Recommend one place to dine in Mexico City for each of the following meals:
{user_selected_days}

Given the next list of restaurant information:
{list_of_entries}

Consider the following preferences:
- {preferred_type}
- {user_suggestion}
For each of them provide:
- name
- price per person
- a description in 100 words
- it's location (neighborhood)
- type of restaurant (e.g. traditional cuisine, top in rankings, fine dining, local classics, street food)
- Cuisine (e.g. sushi, Italian, Mexican)
"""


def restaurant_filtering():
  budget_per_dinner = request.args.get('budget_per_dinner')
  preferred_type = request.args.get('preferred_type')
  user_suggestion = request.args.get('user_suggestion')
  start_time = datetime.datetime.fromisoformat(request.args.get('start_time'))
  number_of_days = request.args.get('number_of_days')
  meals = request.args.get('meals').split(",")

  week_days = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
    "Sunday"
  ]

  user_selected_days = ""
  for day in range(int(number_of_days)):
    for meal in meals:
      meal_day = start_time + datetime.timedelta(days=day)
      week_day = week_days[meal_day.weekday()]
      user_selected_days += week_day + " " + meal
    user_selected_days += '\n'

  entries = EntityEntryModel.search_by_type_id_and_suggestion(
    budget_per_dinner, preferred_type, user_suggestion)

  openai_prompt = PROMPT.format(user_selected_days=user_selected_days,
                                preferred_type=preferred_type,
                                user_suggestion=user_suggestion,
                                list_of_entries="\n".join([
                                  entry["_source"]["summary"]
                                  for entry in entries
                                ]))

  openai.api_key = settings.OPENAI_API_KEY

  response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                          messages=[
                                            {
                                              "role": "user",
                                              "content": openai_prompt,
                                            },
                                          ],
                                          temperature=1,
                                          max_tokens=1024,
                                          top_p=1,
                                          frequency_penalty=0,
                                          presence_penalty=0)
  response_json = response['choices'][0]['message']['content']

  return jsonify(response_json)

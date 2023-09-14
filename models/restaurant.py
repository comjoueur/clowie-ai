from models.base import ESIndexModel
import requests
import json
import datetime

WEEK_DAYS = [
  "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]

DOCUMENTS_PER_QUERY = 1


class RestaurantModel(ESIndexModel):
  ES_INDEX = 'search-clowie-restaurant'
  INGEST_PIPELINE = 'ml-inference-clowie-restaurant-summary'

  @classmethod
  def search_by_type_suggestion_day_meal(cls, price, user_key_words,
                                         start_time, number_of_days, meals):
    url = "{deployment_url}/{index}/_search".format(
      deployment_url=cls.es_deployment_url,
      index=cls.ES_INDEX,
    )
    restaurants = []
    key_word_idx = 0
    ignore_restaurants_ids = []

    for day in range(int(number_of_days)):
      for meal in meals:
        meal_day = start_time + datetime.timedelta(days=day)
        week_day = WEEK_DAYS[meal_day.weekday()]

        query = {
          "size": DOCUMENTS_PER_QUERY,
          "query": {
            "bool": {
              "must": [
                {
                  "text_expansion": {
                    "ml.inference.summary_expanded.predicted_value": {
                      "model_id": ".elser_model_1",
                      "model_text": user_key_words[key_word_idx]
                    }
                  },
                },
                {
                  "query_string": {
                    "default_field": "meals_list",
                    "query": "*{}*".format(meal),
                  }
                },
                {
                  "query_string": {
                    "default_field": "weekdays_list",
                    "query": "*{}*".format(week_day),
                  }
                },
              ],
              "must_not": [{
                "terms": {
                  "_id": ignore_restaurants_ids
                }
              }]
            }
          }
        }
        response = requests.post(url,
                                 data=json.dumps(query),
                                 headers=cls.es_headers)
        if response.status_code != 200:
          raise Exception(
            "Error in Elasticsearch search request: {} {}".format(
              response.status_code, response.text))
        es_restaurants = response.json()['hits']['hits']
        restaurants += [{
          **es_restaurant, "key_word":
          user_key_words[key_word_idx],
          "week_day":
          week_day,
          "meal":
          meal
        } for es_restaurant in es_restaurants]

        key_word_idx = (key_word_idx + 1) % len(user_key_words)
        ignore_restaurants_ids += [
          restaurant['_id'] for restaurant in es_restaurants
        ]
        print(ignore_restaurants_ids)
    print("total " + str(len(restaurants)))
    return restaurants

  @classmethod
  def search_by_type_suggestion_day_meal_v3(cls, price, user_key_words,
                                            start_time, number_of_days, meals):
    url = "{deployment_url}/{index}/_search".format(
      deployment_url=cls.es_deployment_url,
      index=cls.ES_INDEX,
    )
    restaurants = []
    ignore_restaurants_ids = []
    consumable_key_words = [key_word for key_word in user_key_words]
    print("before" * 100)

    for day in range(int(number_of_days)):
      for meal in meals:
        meal_day = start_time + datetime.timedelta(days=day)
        week_day = WEEK_DAYS[meal_day.weekday()]

        best_restaurant = None
        best_score = 0
        best_key_word = None

        if len(consumable_key_words) > 0:
          for key_word in consumable_key_words:
            query = {
              "size": 1,
              "query": {
                "bool": {
                  "must": [
                    {
                      "text_expansion": {
                        "ml.inference.summary_expanded.predicted_value": {
                          "model_id": ".elser_model_1",
                          "model_text": key_word
                        }
                      },
                    },
                    {
                      "query_string": {
                        "default_field": "meals_list",
                        "query": "*{}*".format(meal),
                      }
                    },
                    {
                      "query_string": {
                        "default_field": "weekdays_list",
                        "query": "*{}*".format(week_day),
                      }
                    },
                  ],
                  "must_not": [{
                    "terms": {
                      "_id": ignore_restaurants_ids
                    }
                  }]
                }
              }
            }

            response = requests.post(
              url,
              data=json.dumps(query),
              headers=cls.es_headers,
            )

            es_restaurant = response.json()['hits']['hits'][0]
            if es_restaurant is None or best_score < es_restaurant['_score']:
              best_restaurant = es_restaurant
              best_score = es_restaurant['_score']
              best_key_word = key_word
          consumable_key_words.remove(best_key_word)
        else:
          for key_word in user_key_words:
            query = {
              "size": 1,
              "query": {
                "bool": {
                  "must": [
                    {
                      "text_expansion": {
                        "ml.inference.summary_expanded.predicted_value": {
                          "model_id": ".elser_model_1",
                          "model_text": key_word
                        }
                      },
                    },
                    {
                      "query_string": {
                        "default_field": "meals_list",
                        "query": "*{}*".format(meal),
                      }
                    },
                    {
                      "query_string": {
                        "default_field": "weekdays_list",
                        "query": "*{}*".format(week_day),
                      }
                    },
                  ],
                  "must_not": [{
                    "terms": {
                      "_id": ignore_restaurants_ids
                    }
                  }]
                }
              }
            }

            response = requests.post(
              url,
              data=json.dumps(query),
              headers=cls.es_headers,
            )

            response_json = response.json()

            if not response_json['hits']['hits']:
              print(query)
              return []
              continue

            es_restaurant = response_json['hits']['hits'][0]
            if es_restaurant is None or best_score < es_restaurant['_score']:
              best_restaurant = es_restaurant
              best_score = es_restaurant['_score']
              best_key_word = key_word

        restaurants.append({
          **best_restaurant,
          "meal": meal,
          "week_day": week_day,
          "key_word": best_key_word,
          "best_score": best_score,
        })
        ignore_restaurants_ids.append(best_restaurant['_id'])
        print("ignored", ignore_restaurants_ids)
    return restaurants

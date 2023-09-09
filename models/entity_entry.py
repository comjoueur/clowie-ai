from models.base import ESIndexModel
import json
import requests


class EntityEntryModel(ESIndexModel):
  ES_INDEX = 'search-clowie-entity-entry'
  INGEST_PIPELINE = 'ml-inference-entry-summary'

  @classmethod
  def search_by_type_id_and_suggestion(cls, price, type_restaurant,
                                       preferred_cuisine, suggestion):
    url = "{deployment_url}/{index}/_search".format(
      deployment_url=cls.es_deployment_url,
      index=cls.ES_INDEX,
    )

    semantic_search_prompt = """
Select the documents that include restaurants of the following type {type_of_restaurant} and the following considerations: {user_suggestion}.
""".format(
      type_of_restaurant=type_restaurant,
      user_suggestion=suggestion,
    )

    query = {
      "query": {
        "bool": {
          "must": [{
            "range": {
              "maxPrice": {
                "gte": int(price),
              },
            }
          }, {
            "range": {
              "minPrice": {
                "lte": int(price)
              }
            }
          }, {
            "text_expansion": {
              "ml.inference.summary_expanded.predicted_value": {
                "model_id": ".elser_model_1",
                "model_text": semantic_search_prompt
              }
            },
          }]
        }
      }
    }

    response = requests.post(url,
                             headers=cls.es_headers,
                             data=json.dumps(query))
    if response.status_code >= 300:
      raise Exception("Entry was not created with status code {}\n{}".format(
        response.status_code, response.text))
    responseJson = response.json()

    return responseJson['hits']['hits']

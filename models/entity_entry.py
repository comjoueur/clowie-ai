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
    query = {
      "query": {
        "text_expansion": {
          "ml.inference.summary_expanded": {
            "model_id": ".elser_model_1",
            "model_text": "How is the cooking styles?"
          }
        },
        #"bool": {
        #  "must": [{
        #    "range": {
        #      "maxPrice": {
        #        "gte": int(price),
        #      },
        #    }
        #  }, {
        #    "range": {
        #      "minPrice": {
        #        "lte": int(price)
        #      }
        #    }
        #  }]
        # }
      }
    }

    response = requests.post(url,
                             headers=cls.es_headers,
                             data=json.dumps(query))
    if response.status_code >= 300:
      raise Exception("Entry was not created with status code {}\n{}".format(
        response.status_code, response.text))
    responseJson = response.json()
    print(responseJson)
    print(responseJson['hits']['hits'])

    return responseJson['hits']['hits']

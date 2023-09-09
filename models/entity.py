from models.base import ESIndexModel
import requests
import json


class EntityModel(ESIndexModel):
  ES_INDEX = 'search-clowie-entity'

  @classmethod
  def search_by_price(cls, price):
    url = "{deployment_url}/{index}/_search".format(
      deployment_url=cls.es_deployment_url,
      index=cls.ES_INDEX,
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
    return response.json()['hits']['hits']
  
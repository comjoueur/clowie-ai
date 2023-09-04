import json
import settings
import requests

ES_DEPLOYMENT_URL = 'https://cf406e5a2f0d4a54a257a3c968d6614b.us-central1.gcp.cloud.es.io:443'
ES_HEADERS = {
  'Authorization': 'ApiKey {api_key}'.format(api_key=settings.ES_API_KEY),
  'Content-Type': 'application/json'
}


class ESIndexModel:
  ES_INDEX = ''
  INGEST_PIPELINE = 'ent-search-generic-ingestion'

  @classmethod
  def create(cls, entity_data):
    url = "{deployment_url}/{index}/_doc?pipeline={pipeline}".format(
      deployment_url=ES_DEPLOYMENT_URL,
      index=cls.ES_INDEX,
      pipeline=cls.INGEST_PIPELINE,
    )

    data = json.dumps(entity_data)
    response = requests.post(url, headers=ES_HEADERS, data=data)
    if response.status_code >= 300:
      error_message = "{} was not created with status code {}\n{}"
      raise Exception(
        error_message.format(cls.ES_INDEX, response.status_code,
                             response.text))
    return response.json()

  @classmethod
  def get_by_id(cls, entity_id):
    url = "{deployment_url}/{index}/_doc/{id}".format(
      deployment_url=ES_DEPLOYMENT_URL,
      index=cls.ES_INDEX,
      id=entity_id,
    )
    response = requests.get(url, headers=ES_HEADERS)
    if response.status_code >= 300:
      raise Exception("Entry was not created with status code {}\n{}".format(
        response.status_code, response.text))

    return response.json()

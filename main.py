from flask import Flask, request, render_template, abort
import requests
from pymongo import MongoClient
import os
import openai
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
client = MongoClient(os.environ['MONGO_DB_URI'])
db = client[os.environ['MONGO_DB_NAME']]
openai.api_key = os.environ['OPENAI_API_KEY']
elastic_search_headers = {
  'Authorization': 'ApiKey {}'.format(os.environ["ELASTIC_SEARCH_INDEX_SAVE"]),
  'Content-Type': 'application/json'
}
es_url = "https://cf406e5a2f0d4a54a257a3c968d6614b.us-central1.gcp.cloud.es.io:443"

#
# CLOWIE HELPERS
#


def clear_text(text):
  cleared_text = text.replace("\n", " ").replace("\r",
                                                 " ").replace("\t",
                                                              " ").strip()
  cleared_text = ' '.join(cleared_text.split())
  return cleared_text


def split_by_chunks(text):
  CHUNK_SIZE = 4000
  chunks = []
  accum_chunk = ""
  for semantic_chunk in text.split("."):
    if len(accum_chunk + semantic_chunk) > CHUNK_SIZE:
      chunks.append(accum_chunk)
      accum_chunk = semantic_chunk
    else:
      accum_chunk += semantic_chunk
  if accum_chunk:
    chunks.append(accum_chunk)
  return chunks


def upload_chunks_to_elastic_search(chunks):
  url = "{}/search-clowie/_doc?pipeline=ml-inference-clowie".format(es_url)
  for chunk in chunks:
    response = requests.post(url,
                             headers=elastic_search_headers,
                             data=json.dumps({"chunkInfo": chunk}))
    if response.status_code >= 300:
      abort(response.status_code, response.text)


def search_info_on_es(text):
  url = "{}/search-clowie/_search".format(es_url)
  data = json.dumps({
    "query": {
      "text_expansion": {
        "ml.inference.chunkInfo_expanded.predicted_value": {
          "model_id": ".elser_model_1",
          "model_text": text
        }
      }
    }
  })

  response = requests.post(url, headers=elastic_search_headers, data=data)
  if response.status_code >= 300:
    print(response.text)
    abort(response.status_code, response.text)
  jsonResponse = response.json()
  return jsonResponse.get('hits', {}).get('hits', [])


#
# CLOWIE FUNCTIONAL ENDPOINTS
#


@app.route('/process/url', methods=['POST'])
def process_url():
  url = request.form.get('url')

  response = requests.get(url)
  html = response.text

  soup = BeautifulSoup(html, 'html.parser')
  text = soup.get_text()
  cleared_text = clear_text(text)

  chunks = split_by_chunks(cleared_text)

  upload_chunks_to_elastic_search(chunks)
  return "Created {} chunks".format(len(chunks))


@app.route('/process/text', methods=['POST'])
def process_text():
  text = request.form.get('text')
  cleared_text = clear_text(text)

  chunks = split_by_chunks(cleared_text)
  upload_chunks_to_elastic_search(chunks)
  return "Created {} chunks".format(len(chunks))


@app.route('/es/document/<document_id>', methods=['DELETE'])
def delete_es_document(document_id):
  url = "{}/search-clowie/_doc/{}".format(es_url, document_id)
  response = requests.delete(url, headers=elastic_search_headers)
  if response.status_code >= 300:
    abort(response.status_code, response.text)
  return "Deleted successfully"


@app.route('/es/search', methods=['GET'])
def search_es():
  query = request.args.get('query')
  return search_info_on_es(query)


@app.route('/overall-query', methods=['GET'])
def overall_query():
  query = request.args.get('query')
  fragments = search_info_on_es(query)
  fragments.sort(key=lambda x: x['_score'], reverse=True)
  fragments = '\n'.join(
    [fragment['_source']['chunkInfo'] for fragment in fragments])
  prompt = "Given the next prompt from a user (\"{}\"), answer the prompt based on the datasource fragments data (order by relevance) and your knowledge, paraphrase if it's needed\n\n[start of datasource fragments data]\n{}\n\n[end of datasource fragments data]".format(
    query, fragments)

  openaiResponse = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                                messages=[{
                                                  "role": "user",
                                                  "content": prompt
                                                }],
                                                max_tokens=7000)

  # Invoke OpenAI API here and get the generated text
  generated_text = openaiResponse.get('choices')[0].get('message').get(
    'content')
  return generated_text


@app.route('/process/doc', methods=['POST'])
def process_doc():
  text = request.form.get('text')
  cleared_text = clear_text(text)

  chunks = split_by_chunks(cleared_text)
  upload_chunks_to_elastic_search(chunks)
  return "Created {} chunks".format(len(chunks))


#
# CLOWIE RENDER ENDPOINTS
#


@app.route('/view/process-url', methods=['GET'])
def view_process_url():
  return render_template('process_url.html')


@app.route('/view/process-text', methods=['GET'])
def view_process_text():
  return render_template('process_text.html')


@app.route('/view/es/query-ranker', methods=['GET'])
def view_query_ranker():
  return render_template('query_ranker.html')


@app.route('/view/overall-query', methods=['GET'])
def view_overall_query():
  return render_template('overall_query.html')


@app.route('/view/es/delete', methods=['GET'])
def view_delete_es_doc():
  return render_template('delete_es_doc.html')


@app.route('/main', methods=['GET'])
def main_page():
  return render_template('main_page.html')


@app.route('/entry_doc_row', methods=['GET'])
def entry_doc():
  return render_template('entry_doc_form.html')


@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')


app.run(host='0.0.0.0', port=81)

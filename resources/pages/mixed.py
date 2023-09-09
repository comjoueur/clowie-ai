from flask import render_template

def list_resources_page():
  return render_template('list_resources.html')

def delete_all_indices_docs_page():
  return render_template('delete_all_docs.html')

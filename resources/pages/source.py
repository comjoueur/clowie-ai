from flask import render_template

def create_source_page():
  return render_template('create_source_form.html')

def delete_source_page():
  return render_template('delete_source_form.html')

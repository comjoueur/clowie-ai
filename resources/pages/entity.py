from flask import render_template


def create_entity_page():
  return render_template('create_entity_form.html')


def delete_entity_page():
  return render_template('delete_entity_form.html')

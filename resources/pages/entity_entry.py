from flask import render_template


def create_entity_entry_page():
  return render_template('create_entry_form.html')


def delete_entry_page():
  return render_template('delete_entry_form.html')

from flask import render_template


def create_restaurant_page():
  return render_template('create_restaurant_form.html')


def delete_restaurant_page():
  return render_template('delete_restaurant_form.html')

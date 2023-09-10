import datetime

WEEK_DAYS = [
  "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]


def generate_meals_schedule(number_of_days, start_time, meals):
  user_selected_days = ""
  for day in range(int(number_of_days)):
    for meal in meals:
      meal_day = start_time + datetime.timedelta(days=day)
      week_day = WEEK_DAYS[meal_day.weekday()]
      user_selected_days += week_day + " " + meal + '\n'
  return user_selected_days

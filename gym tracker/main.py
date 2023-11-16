import requests
import datetime as dt
import os

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
calorie_estimate_url = "https://trackapi.nutritionix.com/v2/natural/exercise"
TOKEN = os.environ["TOKEN"]
sheety_post_url = os.environ["SHEET_ENDPOINT"]

# Getting today's date

date_now = dt.date.today()
day = str(date_now.day)
month = str(date_now.month)
year = str(date_now.year)
date = f"{day}/{month}/{year}"
hour_now = int(dt.datetime.now().hour) + 2
hour_now = str(hour_now)
minute_now = int(dt.datetime.now().minute)
if minute_now < 10:
    minute_now = str(minute_now)
    minute_now = f"0{minute_now}"
minute_now = str(minute_now)
hour_in_day = f"{hour_now}:{minute_now}"


#setting up the api call

headers = {
    "x-app-id":APP_ID,
    "x-app-key":API_KEY,

}
headers_auth = {
    "Authorization": TOKEN
}

user_input = input("What exercise did you did and for how long/what was the distance you ran/cycled etc?")

post_body = {
 "query":user_input,
 "gender":"male",
 "weight_kg":99,
 "height_cm":185,
 "age":21
}
#AI processed our input, now we can get the exact info we want

response = requests.post(url=calorie_estimate_url, json=post_body, headers=headers)
response.raise_for_status()
fitness_data = response.json()

exercises_list = fitness_data["exercises"]


#sending the info back to sheety, which updates our google sheet,
# which has 5 columns: Date, Time, Exercise, Duration, Calories

for exercise in exercises_list:
    date = date
    hour_in_day = hour_in_day
    exercise_type = str(exercise["name"])
    exercise_type = exercise_type.title()
    duration = exercise["duration_min"]
    calories_burned = exercise["nf_calories"]
    sheety_body = {
        "workout": {
            "date": date,
            "time": hour_in_day,
            "exercise": exercise_type,
            "duration": duration,
            "calories": calories_burned


        }


    }
    response_post_sheety = requests.post(url=sheety_post_url, json=sheety_body, headers=headers_auth)

    response_post_sheety.raise_for_status()

print(response_post_sheety.text)

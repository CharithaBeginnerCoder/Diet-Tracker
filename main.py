import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app_id = os.getenv("APP_ID")
api_key = os.getenv("API_KEY")
nutrient_endpoint = os.getenv("NUT_ENDPOINT")
sheet_endpoint = os.getenv("SHEET_ENDPOINT")
YOUR_SHEET_TOKEN = os.getenv("YOUR_TOKEN")

headers = {
    "x-app-id": app_id,
    "x-app-key": api_key,
}

breakfast_text = input("What did you have for Breakfast: ")
breakfast_parameters = {
    "query": breakfast_text
}
breakfast_response = requests.post(nutrient_endpoint, json=breakfast_parameters, headers=headers)

lunch_text = input("What did you have for Lunch: ")
lunch_parameters = {
    "query": lunch_text
}
lunch_response = requests.post(nutrient_endpoint, json=lunch_parameters, headers=headers)

dinner_text = input("What did you have for Dinner: ")
dinner_parameters = {
    "query": dinner_text
}
dinner_response = requests.post(nutrient_endpoint, json=dinner_parameters, headers=headers)

snacks_text = input("What did you have as Snacks: ")
snacks_parameters = {
    "query": snacks_text
}
snacks_response = requests.post(nutrient_endpoint, json=snacks_parameters, headers=headers)

water_text = input("Did you drink something: ")
water_parameters = {
    "query": water_text
}
water_response = requests.post(nutrient_endpoint, json=water_parameters, headers=headers)

breakfast_result = breakfast_response.json()
lunch_result = lunch_response.json()
dinner_result = dinner_response.json()
snacks_result = snacks_response.json()
water_result = water_response.json()

result = [breakfast_result, lunch_result, dinner_result, snacks_result, water_result]

today_date = datetime.now().strftime("%d/%m/%y")

complete_list = []
calories = 0
for item in range(0, len(result)):
    list_1 = ""
    for i in range(0, len(result[item]["foods"])):
        item_name = result[item]["foods"][i]["food_name"].title()
        item_unit = result[item]["foods"][i]["serving_unit"]
        item_qty = str(result[item]["foods"][i]["serving_qty"])
        calories = calories + float(result[item]["foods"][i]["nf_calories"])
        list_item = item_name + ", " + item_qty + ", " + item_unit
        list_1 = list_1 + list_item + "\n"
    complete_list.append(list_1)

calories = str(round(calories, 3))

sheet_inputs = {
    "sheet1": {
        "date": today_date,
        "breakfast": complete_list[0],
        "lunch": complete_list[1],
        "dinner": complete_list[2],
        "snacks": complete_list[3],
        "drinks": complete_list[4],
        "calories": calories
    }
}

bearer_headers = {
    "Authorization": f"Bearer {YOUR_SHEET_TOKEN}"
}
sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=bearer_headers)




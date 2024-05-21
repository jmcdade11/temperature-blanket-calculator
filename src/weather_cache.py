from blanket_node import BlanketNode
from calendar import monthrange
from datetime import date, timedelta
import json
import os
from pathlib import Path
from urllib.request import urlopen

class WeatherCache:
    def __init__(self):
        self.cache_path = None
        self.api_key = None
        self.blanket_nodes_dict = {}
        self.ip = None

    def load_from_cache(self):
        cache_file = Path(self.cache_path)
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        converted_blanket_nodes_dict = {}
        if not cache_file.is_file():
            return {}
        try:
            with open(cache_file, 'r') as f:
                blanket_nodes_dict = json.loads(f.read())
            for month in blanket_nodes_dict:
                blanket_nodes = []
                days_json = blanket_nodes_dict[month]
                for day in days_json:
                    blanket_node = json.loads(day, object_hook=BlanketNode.from_json)
                    blanket_nodes.append(blanket_node)
                converted_blanket_nodes_dict[int(month)] = blanket_nodes
            return converted_blanket_nodes_dict
        except Exception as e:
            print("Unable to load cache file: ", e)

    def cache_is_empty(self):
        return not self.blanket_nodes_dict
    
    def fill_yearly_cache(self):
        for month in self.get_total_months():
            self.fill_monthly_cache(month)
        
    def fill_monthly_cache(self, month_num):
        yesterday = self.get_yesterday()
        yesterday_month = yesterday.month
        yesterday_year = yesterday.year
        yesterday_day = yesterday.day
        month_blanket_nodes = []
        beginning_date = date(yesterday_year, month_num, 1)
        if month_num == yesterday_month:
            month_last_day = yesterday_day
            end_date = yesterday
        else:
            month_last_day = monthrange(yesterday_year, month_num)[1]
            end_date = date(yesterday_year, month_num, month_last_day)

        weather_json = self.call_weather_api(self.ip, beginning_date, end_date, self.api_key)
        for i in range(month_last_day):
            weather_date = weather_json["data"]["weather"][i]["date"]
            min_c = weather_json["data"]["weather"][i]["mintempC"]
            max_c = weather_json["data"]["weather"][i]["maxtempC"]
            if (abs(int(min_c)) > abs(int(max_c))):
                selected_temp = min_c
            else:
                selected_temp = max_c
            month_blanket_nodes.append(BlanketNode(weather_date, max_c, min_c, selected_temp).to_json())
        self.blanket_nodes_dict[month_num] = month_blanket_nodes
    
    def write_to_cache(self):
        try:
            cache_file = Path(self.cache_path)
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.blanket_nodes_dict, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Unable to write out to cache file: ", e)
        self.blanket_nodes_dict = self.load_from_cache()

    def fill_weekly_cache(self):
        pass

    def get_ip(self):
        try:
            with urlopen("https://ident.me") as public_ip_response:
                my_ip = public_ip_response.read().decode('utf8')
            return my_ip
        except Exception as e:
            print("Could not fetch our public IP for weather api usage: ", e)
            exit()

    def get_api_key(self):
        api_key = os.environ.get("WEATHER_BLANKET_API_KEY")
        if api_key is None:
            raise ValueError("Could not find weather api key in WEATHER_BLANKET_API_KEY environment variable")
        return api_key
    
    def call_weather_api(self, ip, beginning_date, end_date, api_key):
        url = f"https://api.worldweatheronline.com/premium/v1/past-weather.ashx?q={ip}&date={beginning_date}&enddate={end_date}&key={api_key}&format=json"

        try:
            with urlopen(url) as response:
                body = response.read()
                
            weather_json = json.loads(body)
        except Exception as e:
            print("Error when calling weather api: ", e)
        return weather_json

    def get_yesterday(self):
        today = date.today()
        yesterday = today - timedelta(days = 1)
        return yesterday
    
    def get_total_months(self):
        yesterday = self.get_yesterday()
        yesterday_month = yesterday.month
        return list(range(1, yesterday_month + 1))
    
    def get_missing_months(self, starting_month_num):
        yesterday = self.get_yesterday()
        yesterday_month = yesterday.month
        return list(range(starting_month_num, yesterday_month + 1))

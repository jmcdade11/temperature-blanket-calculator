from blanket_node import BlanketNode
from calendar import monthrange
from datetime import date, timedelta
import json
import os
from pathlib import Path
from urllib.request import urlopen

class WeatherCache:
    def __init__(self):
        self.cache_path = "cache/weather_cache.json"
        self.api_key = None
        self.blanket_nodes_dict = {}
        self.ip = None

    def load_from_cache(self):
        cache_file = Path(self.cache_path)
        if not cache_file.is_file():
            return {}
        blanket_nodes_dict = {}
        contents = cache_file.read_text()
        cache_json = json.loads(contents)
        for cache_node in cache_json:
            blanket_node = BlanketNode(cache_node["date"], cache_node["high"], cache_node["low"], cache_node["selected_temp"])
            blanket_nodes_dict["blah"] = blanket_node
        return blanket_nodes_dict
    
    def cache_is_empty(self):
        return not self.blanket_nodes_dict
    
    def fill_yearly_cache(self):
        blanket_nodes_dict = {}
        today = date.today()
        yesterday = today - timedelta(days = 1)
        yesterday_month = yesterday.month
        yesterday_year = yesterday.year
        yesterday_day = yesterday.day

        for month in range(1, yesterday_month + 1):
            month_blanket_nodes = []
            beginning_date = date(yesterday_year, month, 1)
            if month == yesterday_month:
                month_last_day = yesterday_day
                end_date = yesterday
            else:
                month_last_day = monthrange(yesterday_year, month)[1]
                end_date = date(yesterday_year, month, month_last_day)

            weather_json = self.call_weather_api(self.ip, beginning_date, end_date, self.api_key)
            for i in range(month_last_day):
                weather_date = weather_json["data"]["weather"][i]["date"]
                min_c = weather_json["data"]["weather"][i]["mintempC"]
                max_c = weather_json["data"]["weather"][i]["maxtempC"]
                if (abs(int(min_c)) > abs(int(max_c))):
                    selected_temp = min_c
                else:
                    selected_temp = max_c
                month_blanket_nodes.append(BlanketNode(weather_date, max_c, min_c, selected_temp))
            blanket_nodes_dict[month] = month_blanket_nodes
        self.blanket_nodes_dict = blanket_nodes_dict

    def fill_monthly_cache(self):
        pass

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
        with urlopen(url) as response:
            body = response.read()
            
        weather_json = json.loads(body)
        return weather_json
     

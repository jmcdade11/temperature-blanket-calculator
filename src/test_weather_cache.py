from blanket_node import BlanketNode
from colour_index import ColourIndex
from datetime import date, datetime, timedelta
from pathlib import Path
import shutil
import unittest
import uuid
from weather_cache import WeatherCache

class TestWeatherCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clear_cache()
    
    @classmethod
    def tearDownClass(cls):
        cls.clear_cache()

    def clear_cache():
        dirpath = Path("cache")
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)

    def get_yesterday(self):
        today = date.today()
        yesterday = today - timedelta(days = 1)
        return yesterday
    
    def get_total_months(self):
        yesterday = self.get_yesterday()
        yesterday_month = yesterday.month
        return list(range(1, yesterday_month + 1))
    
    def get_date_from_string(self, date_str):
        date_format = '%Y-%m-%d'
        return datetime.strptime(date_str, date_format).date()
    
    def get_cache_path(self):
        return f"cache/{str(uuid.uuid4())}.json"
    
    def get_colour_index_path(self):
        return "colour_index.csv"
    
    def test_write_to_cache(self):
        colour_index = ColourIndex(self.get_colour_index_path())
        cache = WeatherCache(colour_index)
        cache.cache_path = self.get_cache_path()
        test_dict_json = {1: [BlanketNode("2024-01-01", 10, 1, 10, "Green")]}
        cache.blanket_nodes_dict = test_dict_json
        cache.write_to_cache()
        test_dict = {1: [BlanketNode("2024-01-01", 10, 1, 10, "Green")]}
        self.assertEqual(cache.blanket_nodes_dict, test_dict)
        
    def test_fill_yearly_cache(self):
        total_months = self.get_total_months()
        yesterday = self.get_yesterday()

        colour_index = ColourIndex(self.get_colour_index_path())
        cache = WeatherCache(colour_index)
        cache.cache_path = self.get_cache_path()
        cache.api_key = cache.get_api_key()
        cache.blanket_nodes_dict = {}

        self.assertTrue(cache.cache_is_empty(), "The weather cache is not empty")
        cache.fill_yearly_cache()
        cache.write_to_cache()
        self.assertCountEqual(cache.blanket_nodes_dict, total_months)
        jan_days = cache.blanket_nodes_dict[1]
        blanket_node = jan_days[0]
        self.assertEqual(blanket_node.date, f"{yesterday.year}-01-01")
        if (abs(int(blanket_node.low)) > abs(int(blanket_node.high))):
            self.assertEqual(blanket_node.selected_temp, blanket_node.low)
        else:
            self.assertEqual(blanket_node.selected_temp, blanket_node.high)
    
    def test_fill_yearly_cache_to_yesterday(self):
        yesterday = self.get_yesterday()
        total_months = self.get_total_months()
        
        colour_index = ColourIndex(self.get_colour_index_path())
        cache = WeatherCache(colour_index)
        cache.cache_path = self.get_cache_path()
        cache.api_key = cache.get_api_key()
        cache.blanket_nodes_dict = {}
       
        cache.fill_yearly_cache()
        cache.write_to_cache()
        last_month_blanket_nodes = cache.blanket_nodes_dict[total_months[-1]]
        yesterday_blanket_node = last_month_blanket_nodes[-1]

        self.assertEqual(yesterday, self.get_date_from_string(yesterday_blanket_node.date))
    
    def test_fill_monthly_cache(self):
        jan_days = 31
 
        colour_index = ColourIndex(self.get_colour_index_path())
        cache = WeatherCache(colour_index)
        cache.cache_path = self.get_cache_path()
        cache.api_key = cache.get_api_key()
        cache.blanket_nodes_dict = {}
       
        cache.fill_monthly_cache(1)
        cache.write_to_cache()

        self.assertEqual(1, len(cache.blanket_nodes_dict))
        self.assertEqual(jan_days, len(cache.blanket_nodes_dict[1]))

    def test_fill_monthly_cache_this_month(self):
        yesterday = self.get_yesterday()
 
        colour_index = ColourIndex(self.get_colour_index_path())
        cache = WeatherCache(colour_index)
        cache.cache_path = self.get_cache_path()
        cache.api_key = cache.get_api_key()
        cache.blanket_nodes_dict = {}
       
        cache.fill_monthly_cache(yesterday.month)
        cache.write_to_cache()

        self.assertEqual(1, len(cache.blanket_nodes_dict))
        self.assertEqual(yesterday.day, len(cache.blanket_nodes_dict[yesterday.month]))

    def test_fill_missing_months_cache(self):
        yesterday = self.get_yesterday()
 
        colour_index = ColourIndex(self.get_colour_index_path())
        cache = WeatherCache(colour_index)
        cache.cache_path = self.get_cache_path()
        cache.api_key = cache.get_api_key()
        cache.blanket_nodes_dict = {}
       
        cache.fill_monthly_cache(1)
        cache.write_to_cache()
        cache.fill_missing_months_cache()
        cache.write_to_cache()

        self.assertEqual(yesterday.month, len(cache.blanket_nodes_dict))
        self.assertEqual(yesterday.day, len(cache.blanket_nodes_dict[yesterday.month]))

        
if __name__ == '__main__':
    unittest.main()
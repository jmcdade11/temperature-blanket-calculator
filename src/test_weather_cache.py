
from blanket_node import BlanketNode
from datetime import date, timedelta
import unittest
from weather_cache import WeatherCache

class TestWeatherCache(unittest.TestCase):
    def test_fill_yearly_cache(self):
        jan_day_count = 31
        cache = WeatherCache()
        cache.api_key = cache.get_api_key()
        cache.blanket_nodes_dict = {}
        today = date.today()
        yesterday = today - timedelta(days = 1)
        yesterday_month = yesterday.month
        yesterday_year = yesterday.year
        self.assertTrue(cache.cache_is_empty(), "The weather cache is not empty")
        cache.fill_yearly_cache()
        total_months = list(range(1, yesterday_month + 1))
        self.assertCountEqual(cache.blanket_nodes_dict, total_months)
        jan_days = cache.blanket_nodes_dict[1]
        self.assertEqual(jan_day_count, len(jan_days))
        blanketNode = jan_days[0]
        self.assertEqual(blanketNode.date, f"{yesterday_year}-01-01")
        if (abs(int(blanketNode.low)) > abs(int(blanketNode.high))):
            self.assertEqual(blanketNode.selected_temp, blanketNode.low)
        else:
            self.assertEqual(blanketNode.selected_temp, blanketNode.high)
     

if __name__ == '__main__':
    unittest.main()
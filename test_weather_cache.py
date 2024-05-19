
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
        self.assertTrue(cache.cache_is_empty(), "The weather cache is not empty")
        cache.fill_yearly_cache()
        total_months = list(range(1, yesterday_month + 1))
        self.assertCountEqual(cache.blanket_nodes_dict, total_months)
        self.assertEqual(jan_day_count, len(cache.blanket_nodes_dict[1]))
    

if __name__ == '__main__':
    unittest.main()
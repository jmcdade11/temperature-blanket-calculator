from weather_cache import WeatherCache

def main():
    cache = WeatherCache()
    cache.cache_path = "cache/weather_cache.json"
    cache.api_key = cache.get_api_key()
    cache.blanket_nodes_dict = cache.load_from_cache()
    if cache.cache_is_empty():
        cache.fill_yearly_cache()
        cache.write_to_cache()
        print(cache.blanket_nodes_dict[1])
    else:
        last_cached_month = list(cache.blanket_nodes_dict.keys())[-1]
        yesterday = cache.get_yesterday()
        if yesterday.month != last_cached_month:
            months = cache.get_missing_months(last_cached_month + 1)
            for month in months:
                print(f"filling in month: {month}")
                cache.fill_monthly_cache(month)
            cache.write_to_cache()

if __name__ == '__main__':
    main()
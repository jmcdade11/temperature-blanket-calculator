from weather_cache import WeatherCache

def main():
    cache = WeatherCache()
    cache.api_key = cache.get_api_key()
    cache.blanket_nodes_dict = cache.load_from_cache()
    if cache.cache_is_empty():
        cache.fill_yearly_cache()
        print(cache.blanket_nodes_dict[1])
    else:
        print("lol")

if __name__ == '__main__':
    main()
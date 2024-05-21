from pathlib import Path
import sys
from weather_cache import WeatherCache
from colour_index import ColourIndex

def main():
    try:
        if len(sys.argv) > 1:
            index = sys.argv[1]
            index_path = Path(index)
            if not index_path.exists() or not index_path.is_file():
                raise ValueError("Invalid colour index csv provided")
        else:
            index = "colour_index.csv"
        colour_index = ColourIndex(index)
    except Exception as e:
        print("broken: ", e)
        sys.exit()
    cache = WeatherCache(colour_index)
    cache.cache_path = "cache/weather_cache.json"
    cache.api_key = cache.get_api_key()
    cache.blanket_nodes_dict = cache.load_from_cache()
    cache.colour_index = colour_index
    if cache.cache_is_empty():
        cache.fill_yearly_cache()
        cache.write_to_cache()
    else:
        cache.fill_missing_months_cache()
        cache.write_to_cache()

if __name__ == '__main__':
    main()
import calendar
from datetime import datetime
import os
from pathlib import Path
import sys
from weather_cache import WeatherCache
from colour_index import ColourIndex

def generate_report(template_path, dest_path, cache):
    if not os.path.exists(template_path):
        raise ValueError(f"Path {template_path} does not exist")
    report_str = ""
    new_line = '\n'
    blanket_nodes_dict = cache.blanket_nodes_dict
    for month in blanket_nodes_dict.keys():
        monthly_colour_count = {}
        month_name = calendar.month_name[month]
        report_str += f'<button type="button" class="collapsible">{month_name}</button>{new_line}'
        report_str += f'<div class="content">'
        report_str += f"""
<table>
    <tr>
        <th>Day</th>
        <th>High</th>
        <th>Low</th>
        <th>Selected Temp</th>
        <th>Colour</th>
    </tr>
"""
        for month_day in blanket_nodes_dict[month]:
            converted_date = datetime.strptime(month_day.date, '%Y-%m-%d')
            day_number = converted_date.day
            content_node = f"""
<tr>
    <td>{day_number}</td>
    <td>{month_day.high}</td>
    <td>{month_day.low}</td>
    <td>{month_day.selected_temp}</td>
    <td>{month_day.colour}</td>
</tr>
"""
            report_str += content_node
            if month_day.colour not in monthly_colour_count:
                monthly_colour_count[month_day.colour] = 1
            else:
                monthly_colour_count[month_day.colour] += 1
        report_str += f'</table>{new_line}'
        report_str += f'<h3>Monthly colour report</h3>'
        report_str += f"""
<table>
    <tr>
        <th>Colour</th>
        <th>Count</th>
    </tr>
"""
        for colour in monthly_colour_count.keys():
            report_str += f"""
<tr>
    <td>{colour}</td>
    <td>{monthly_colour_count[colour]}</td>
</tr>
"""
        report_str += f'</table>{new_line}'
        report_str += f'</div>{new_line}'
  
    with open(template_path) as template_file:
        template_content = template_file.read()

    template_content = template_content.replace("{{ Content }}", report_str)
    
    dest_file = Path(dest_path)
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_file, "w") as dest_file_writer:
        dest_file_writer.write(template_content)

def main():
    #TODO: some sort of structure for storing monthly colour counts, aggregate up to yearly counts
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
        print("Could not load colour index: ", e)
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
    generate_report("template.html", "temperature_blanket.html", cache)

if __name__ == '__main__':
    main()
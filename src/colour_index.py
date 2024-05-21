import csv
from colour_range import ColourRange

class ColourIndex:
    def __init__(self, index_path):
        self.index_path = index_path
        self.colour_ranges = self.load_colour_ranges()
    
    def load_colour_ranges(self):
        colour_range_list = []
        with open(self.index_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                colour_range = ColourRange(int(row["low"]), int(row["high"]), row["colour"])
                colour_range_list.append(colour_range)
        return colour_range_list
    
    
        
        
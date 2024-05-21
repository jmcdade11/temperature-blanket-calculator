from colour_index import ColourIndex
from colour_range import ColourRange
import csv
from pathlib import Path
import shutil
import unittest
import uuid

class TestColourIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clear_temp()
    
    @classmethod
    def tearDownClass(cls):
        cls.clear_temp()

    def clear_temp():
        dirpath = Path("temp")
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)

    def get_temp_path(self):
        return f"temp/{str(uuid.uuid4())}.csv"
    
    def test_load_colour_ranges(self):
        index = self.get_temp_path()
        index_path = Path(index)
        index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(index_path, 'w', newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['low','high','colour'])
            writer.writerow(["1","10","Green"])
            writer.writerow(["11","20","Yellow"])
        colour_index = ColourIndex(index)
        colour_index.load_colour_ranges()
        self.assertEqual(2, len(colour_index.colour_ranges))
        colour_range = colour_index.colour_ranges[0]
        self.assertEqual(ColourRange(1,10,"Green"), colour_range)
        colour_range = colour_index.colour_ranges[1]
        self.assertEqual(ColourRange(11,20,"Yellow"), colour_range)

    
if __name__ == "__main__":
    unittest.main()
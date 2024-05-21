import json

class BlanketNode:
    def __init__(self, date, high, low, selected_temp):
        self.date = date
        self.high = high
        self.low = low
        self.selected_temp = selected_temp

    def __eq__(self, other):
        return self.date == other.date and self.high == other.high and self.low == other.low and self.selected_temp == other.selected_temp
    
    def __repr__(self):
        return f"BlanketNode(date: {self.date}, high: {self.high}, low: {self.low}, selected_temp: {self.selected_temp})"
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
    def from_json(json_dict):
        return BlanketNode(json_dict["date"], json_dict["high"], json_dict["low"], json_dict["selected_temp"])

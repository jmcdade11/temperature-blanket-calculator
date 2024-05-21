import json

class BlanketNode:
    def __init__(self, date, high, low, selected_temp, colour):
        self.date = date
        self.high = high
        self.low = low
        self.selected_temp = selected_temp
        self.colour = colour

    def __eq__(self, other):
        return self.date == other.date and self.high == other.high and self.low == other.low and self.selected_temp == other.selected_temp and self.colour == other.colour
    
    def __repr__(self):
        return f"BlanketNode(date: {self.date}, high: {self.high}, low: {self.low}, selected_temp: {self.selected_temp}, colour: {self.colour})"
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
    def from_json(json_dict):
        return BlanketNode(json_dict["date"], int(json_dict["high"]), int(json_dict["low"]), int(json_dict["selected_temp"]), json_dict["colour"])

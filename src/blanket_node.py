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
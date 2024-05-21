class ColourRange:
    def __init__(self, low, high, colour):
        self.low = low
        self.high = high
        self.colour = colour
    
    def __eq__(self, other):
        return self.low == other.low and self.high == other.high and self.colour == other.colour
    
    def __repr__(self):
        return f"ColourRange(low: {self.low}, high: {self.high}, colour: {self.colour})"
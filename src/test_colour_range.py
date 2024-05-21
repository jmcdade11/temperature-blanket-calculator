import unittest

from colour_range import ColourRange

class TestColourRange(unittest.TestCase):
    def test_eq(self):
        node = ColourRange(1, 10, "Green")
        node2 = ColourRange(1, 10, "Green")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = ColourRange(1, 10, "Green")
        node2 = ColourRange(-1, -0, "Green")
        self.assertNotEqual(node, node2)
    
    def test_eq_false2(self):
        node = ColourRange(1, 10, "Green")
        node2 = ColourRange(1, 10, "Yellow")
        self.assertNotEqual(node, node2)
     
    def test_repr(self):
        node = ColourRange(1, 10, "Green")
        self.assertEqual(
            "ColourRange(low: 1, high: 10, colour: Green)", repr(node)
        )
    
if __name__ == "__main__":
    unittest.main()
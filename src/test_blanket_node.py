import unittest

from blanket_node import BlanketNode


class TestBlanketNode(unittest.TestCase):
    def test_eq(self):
        node = BlanketNode("2024-01-01", 10, 1, 10, "Green")
        node2 = BlanketNode("2024-01-01", 10, 1, 10, "Green")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = BlanketNode("2024-01-01", 10, 1, 10, "Green") 
        node2 = BlanketNode("2024-01-01", 1, 10, 1, "Green")
        self.assertNotEqual(node, node2)
    
    def test_eq_false2(self):
        node = BlanketNode("2024-01-01", 10, 1, 10, "Green")
        node2 = BlanketNode("2024-02-01", 10, 1, 10, "Yellow")
        self.assertNotEqual(node, node2)
     
    def test_repr(self):
        node = BlanketNode("2024-01-01", 10, 1, 10, "Green")
        self.assertEqual(
            "BlanketNode(date: 2024-01-01, high: 10, low: 1, selected_temp: 10, colour: Green)", repr(node)
        )
    
if __name__ == "__main__":
    unittest.main()
import unittest

from blanket_node import BlanketNode


class TestBlanketNode(unittest.TestCase):
    def test_eq(self):
        node = BlanketNode("2024-01-01", "10", "1", "10")
        node2 = BlanketNode("2024-01-01", "10", "1", "10")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = BlanketNode("2024-01-01", "10", "1", "10") 
        node2 = BlanketNode("2024-01-01", "1", "10", "1")
        self.assertNotEqual(node, node2)
    
    def test_eq_false2(self):
        node = BlanketNode("2024-01-01", "10", "1", "10")
        node2 = BlanketNode("2024-02-01", "10", "1", "10")
        self.assertNotEqual(node, node2)
     
    def test_repr(self):
        node = BlanketNode("2024-01-01", "10", "1", "10")
        self.assertEqual(
            "BlanketNode(date: 2024-01-01, high: 10, low: 1, selected_temp: 10)", repr(node)
        )
    
if __name__ == "__main__":
    unittest.main()
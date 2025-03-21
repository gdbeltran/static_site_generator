import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("<a>", "Test", None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("<a>", "Test", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node, node2)
        
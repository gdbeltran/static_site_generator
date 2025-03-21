import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_text(self):
        node = TextNode("Test", TextType.BOLD)
        node2 = TextNode("Testing", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_texttype(self):
        node = TextNode("Test", TextType.BOLD)
        node2 = TextNode("Test", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_url(self):
        node = TextNode("Test", TextType.BOLD, None)
        node2 = TextNode("Test", TextType.BOLD, None)
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
    

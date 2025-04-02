import unittest
from htmlnode import LeafNode, ParentNode, HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_HTML_props(self):
        node = HTMLNode("a", "Test", None, {"href": "https://www.google.com", "target": "_blank"})
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)
        
        node2 = HTMLNode("a", "Test", None, None)
        expected_output2 = ""
        self.assertEqual(node2.props_to_html(), expected_output2)
        
        node3 = HTMLNode("img", "Test", None, {"src": "https://www.google.com"})
        expected_output3 = ' src="https://www.google.com"'
        self.assertEqual(node3.props_to_html(), expected_output3)
        
    def test_HTML_tags(self):
        node = HTMLNode("a",None,None,None)
        node2 = HTMLNode("p",None,None,None)
        self.assertNotEqual(node, node2)
        
    def test_HTML_values(self):
        node = HTMLNode(None,"Testing",None,None)
        node2 = HTMLNode(None,"Testing",None,None)
        self.assertEqual(node,node2)
    
    def test_leaf_tag(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello world!")
        self.assertEqual(node.to_html(), "Hello world!")
        
    def test_leaf_props(self):
        node = LeafNode("img", "Test", {"src": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<img src="https://www.google.com">Test</img>')
        
    def test_parent_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_parent_parent_children(self):
        child_node = LeafNode("b", "first child")
        child_node2 = LeafNode("i", "second child")
        child_node3 = LeafNode("b", "third child")
        parent_node = ParentNode("div", [child_node, child_node2])
        parent_node2 = ParentNode("div", [parent_node, child_node3])
        self.assertEqual(parent_node2.to_html(), "<div><div><b>first child</b><i>second child</i></div><b>third child</b></div>")
        
if __name__ == "__main__":
    unittest.main()
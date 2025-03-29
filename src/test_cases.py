import unittest
from htmlnode import *
from textnode import *
from split_nodes import *
from extract_markdown import *

# test HTMLNode
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
        
# test split nodes
class TestSplitNodes(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
        
    def test_split_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])
        
    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])
        
    def test_split_non_text(self):
        node = TextNode("This is text with a **bold** word", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a **bold** word", TextType.BOLD)
        ])
        
    def test_split_multiple(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is another text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ],[
            TextNode("This is another text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
        
# test TextNode
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
        
    def test_text_to_leaf_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_to_leaf_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_to_leaf_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_to_leaf_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_to_leaf_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props_to_html(), ' href="https://www.google.com"')
        
    def test_text_to_leaf_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props_to_html(), ' src="https://www.google.com" alt="This is a text node"')

# test markdown images and links
class TestMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_images_non_image(self):
        node = TextNode("This is text without an image. ![This is fake]", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text without an image. ![This is fake]", TextType.TEXT)], new_nodes)
        
    def test_split_images_with_link(self):
        node = TextNode("This is text with a link, not an image. [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with a link, not an image. [to boot dev](https://www.boot.dev)", TextType.TEXT)], new_nodes)
    
    def test_split_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes
        )
        
    def test_split_links_non_link(self):
        node = TextNode("This is text without a link. [This is fake]", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text without a link. [This is fake]", TextType.TEXT)], new_nodes)
        
    def test_split_links_with_image(self):
        node = TextNode("This is text with an image, not a link. ![fake image](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with an image, not a link. ![fake image](https://www.boot.dev)", TextType.TEXT)], new_nodes)

if __name__ == "__main__":
    unittest.main()
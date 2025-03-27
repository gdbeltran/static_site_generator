from textnode import *
from extract_markdown import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            lines = node.text.split(delimiter)
            for i in range(len(lines)):
                if i % 2 == 1:
                    new_nodes.append(TextNode(lines[i], text_type))
                else:
                    new_nodes.append(TextNode(lines[i], TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
        for match in matches:
            print(match)
            image_alt = match[0]
            image_link = match[1]
            sections = node.text.split(f"![{image_alt}]({image_link})")
            print(sections)

def split_nodes_link(old_nodes):
    pass
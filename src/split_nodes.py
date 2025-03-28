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
        remaining_text = node.text
        matches = extract_markdown_images(remaining_text)
        if not matches:
            new_nodes.append(node)
            continue
        for match in matches:
            image_alt = match[0]
            image_link = match[1]
            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            remaining_text = sections[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        matches = extract_markdown_links(remaining_text)
        if not matches:
            new_nodes.append(node)
            continue
        for match in matches:
            link_text = match[0]
            link_url = match[1]
            sections = remaining_text.split(f"[{link_text}]({link_url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            remaining_text = sections[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        
    return new_nodes
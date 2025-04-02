import re

from textnode import TextNode, TextType

def parse_link(matched_text):
    text_start = matched_text.index("[") + 1
    text_end = matched_text.index("]")
    text = matched_text[text_start:text_end]

    url_start = matched_text.index("(") + 1
    url_end = matched_text.index(")")
    url = matched_text[url_start:url_end]

    return text, url

def parse_image(matched_text):
    alt_start = matched_text.index("![") + 2
    alt_end = matched_text.index("]")
    alt_text = matched_text[alt_start:alt_end]

    url_start = matched_text.index("(") + 1
    url_end = matched_text.index(")")
    img_url = matched_text[url_start:url_end]

    return alt_text, img_url

def find_first_match(regex, text):
    match = re.search(regex, text)
    if not match:
        return None
    
    first_group = None
    first_start = len(text)
    for name, value in match.groupdict().items():
        if value:
            start = match.start(name)
            if start < first_start:
                first_start = start
                first_group = name
    
    return first_group, first_start, match.group(first_group)

def text_to_textnodes(remaining_text):
    pattern = (
    r"(?P<bold>\*\*(.+?)\*\*)" +
    r"|(?P<italic>_(.+?)_)" +
    r"|(?P<code>`(.+?)`)" +
    r"|(?P<link>\[(.+?)\]\((.+?)\))" +
    r"|(?P<image>!\[(.+?)\]\((.+?)\))"
    )
    if not remaining_text:
        return []
    
    first_group, start_index, matched_text = find_first_match(pattern, remaining_text)
    nodes = []
    
    if start_index > 0:
        plain_text = remaining_text[:start_index]
        nodes.append(TextNode(plain_text, TextType.TEXT))
    match (first_group):
        case ("bold"):
            nodes.append(TextNode(matched_text.strip("**"), TextType.BOLD))
        case ("italic"):
            nodes.append(TextNode(matched_text.strip("_"), TextType.ITALIC))
        case ("code"):
            nodes.append(TextNode(matched_text.strip("`"), TextType.CODE))
        case ("link"):
            text, url = parse_link(matched_text)
            nodes.append(TextNode(text, TextType.LINK, url))
        case ("image"):
            alt_text, img_url = parse_image(matched_text)
            nodes.append(TextNode(alt_text, TextType.IMAGE, img_url))
    new_remaining_text = remaining_text[start_index + len(matched_text):]
    return nodes + text_to_textnodes(new_remaining_text)

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

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
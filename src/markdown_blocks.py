import re
from enum import Enum
from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6
    
def markdown_to_blocks(markdown):
    blocks = []
    markdown = markdown.strip()
    for block in markdown.split("\n\n"):
        if not block.strip():
            continue
        lines = block.split("\n")
        cleaned_lines = [line.strip() for line in lines]
        cleaned_block = "\n".join(cleaned_lines)
        blocks.append(cleaned_block)
    return blocks
    
def block_to_block_type(markdown):
    if re.match(r"^#{1,6} .+", markdown):
        return BlockType.HEADING
    
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE

    lines = markdown.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if len(lines) > 0:
        is_ordered = True
        for index, line in enumerate(lines, start=1):
            if not line.startswith(f"{index}. "):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    
    return html_nodes

def blockquote(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        if line.startswith(">"):
            cleaned_lines.append(line[1:].strip())
        else:
            cleaned_lines.append(line.strip())
    content = " ".join(cleaned_lines)
    
    text_nodes = text_to_children(content)
    blockquote_node = ParentNode("blockquote", text_nodes)
    
    return blockquote_node

def unordered_list_block(block):
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        if line.strip() and line.strip().startswith("- "):
            item_text = line[2:].strip()
            text_nodes = text_to_children(item_text)
            list_item = ParentNode("li", text_nodes)
            list_items.append(list_item)
    
    ul_node = ParentNode("ul", list_items)
    return ul_node

def ordered_list_block(block):
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        if line.strip() and re.match(r"^\d+\.\s", line):
            item_text = re.sub(r"^\d+\.\s*", "", line).strip()
            text_nodes = text_to_children(item_text)
            list_item = ParentNode("li", text_nodes)
            list_items.append(list_item)
    
    ol_node = ParentNode("ol", list_items)
    return ol_node

def heading_block(block):
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    text = block[level:].strip()
    text_nodes = text_to_children(text)
    heading_node = ParentNode(f"h{level}", text_nodes)
    
    return heading_node

def code_block(block):
    lines = block.split("\n")
    content = "\n".join(lines[1:-1]) + "\n"
    text_node = TextNode(content, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [html_node])
    pre_node = ParentNode("pre", [code_node])
    
    return pre_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    new_blocks = []
    for block in blocks:
        block_type = block_to_block_type(block)
        try:
            if block_type == BlockType.HEADING:
                new_blocks.append(heading_block(block))
            elif block_type == BlockType.UNORDERED_LIST:
                new_blocks.append(unordered_list_block(block))
            elif block_type == BlockType.ORDERED_LIST:
                new_blocks.append(ordered_list_block(block))
            elif block_type == BlockType.QUOTE:
                blockquote_node = blockquote(block)
                new_blocks.append(blockquote_node)
            elif block_type == BlockType.CODE:
                new_blocks.append(code_block(block))
            elif block_type == BlockType.PARAGRAPH:
                block_text = block.replace("\n", " ")
                text_nodes = text_to_children(block_text)
                new_blocks.append(ParentNode("p", text_nodes))
        except ValueError as e:
            print(f"Error processing block: {block}")
            print(f"Block type: {block_type}")
            raise e
            
    return ParentNode("div", new_blocks)
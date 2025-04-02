from enum import Enum
import re

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
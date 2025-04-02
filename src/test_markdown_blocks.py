import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdowntoHTML(unittest.TestCase):
  
    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_two(self):
        md = """
        This is _italic_ along with **bold**.
It should be two lines long.

Second paragraph.
.
With
weird spaces.

- item
- thing
- fidget
-

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, 
            [
                "This is _italic_ along with **bold**.\nIt should be two lines long.",
                "Second paragraph.\n.\nWith\nweird spaces.",
                "- item\n- thing\n- fidget\n-"
            ])
        
    def test_is_ordered_list(self):
        valid_block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(valid_block), BlockType.ORDERED_LIST)
        
if __name__ == "__main__":
    unittest.main()
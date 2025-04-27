import unittest

from markdown import *


class TestTextNode(unittest.TestCase):
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
    
    def test_block_type_conversion_heading(self):
        text = "# This is a heading"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.HEADING, block_type)

        text = "## This is a heading too"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.HEADING, block_type)

        text = "### This is a heading 3"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_type_conversion_code(self):
        text = "```This is a code block```"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_type_conversion_quote(self):
        text = "> A wise man once said\n> 'This is a quote'"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_type_conversion_unordered_list(self):
        text = "- This is an unordered list\n- with items"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_block_type_conversion_ordered_list(self):
        text = "1. This is an ordered list\n2. with items\n3. the hardest to get right"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

    def test_block_type_conversion_ordered_list_bad_1(self):
        text = "0. This is an bad ordered list\n1. with items"
        block_type = block_to_block_type(text)
        self.assertNotEqual(BlockType.ORDERED_LIST, block_type)

    def test_block_type_conversion_ordered_list_bad_2(self):
        text = "1. This is an bad ordered list\n1. with items"
        block_type = block_to_block_type(text)
        self.assertNotEqual(BlockType.ORDERED_LIST, block_type)

    def test_block_type_conversion_ordered_list_bad_3(self):
        text = "1. This is an bad ordered list\n4. with items"
        block_type = block_to_block_type(text)
        self.assertNotEqual(BlockType.ORDERED_LIST, block_type)

    def test_block_type_conversion_paragraph(self):
        text = "This is just some text, but becomes a paragrafh"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

if __name__ == "__main__":
    unittest.main()
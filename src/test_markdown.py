import unittest

from markdown import *


class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks_1(self):
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
    
    def test_markdown_to_blocks_2(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_3(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
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

    def test_block_type_conversion_code_2(self):
        text = "```\nThis is a\n code block\n```"
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

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> and the next line is here,
> together with the last one.

1. item
2. items
3. itemss
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a quote and the next line is here, together with the last one.</p></blockquote><ol><li>item</li><li>items</li><li>itemss</li></ol></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
>
> together with the last one.

1. item
2. items
3. itemss
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a quote together with the last one.</p></blockquote><ol><li>item</li><li>items</li><li>itemss</li></ol></div>",
        )

    def test_extract_title(self):
        md = """
# This is the title

> This is a quote
> and the next line is here,
> together with the last one.

## this is not the title

1. item
2. items
3. itemss
"""
        title = extract_title(md)
        self.assertEqual(
            title,
            "This is the title"
        )

        

    def test_extract_title_bad(self):
        md = """
> This is a quote
> and the next line is here,
> together with the last one.

## this is not the title

1. item
2. items
3. itemss
"""
        try:
            extract_title(md)
        except Exception:
            return
        

if __name__ == "__main__":
    unittest.main()
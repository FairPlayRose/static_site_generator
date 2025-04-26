import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_neq_text(self):
        node = TextNode("This is text", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_neq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "google.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("3+4=7", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "3+4=7")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "google.com"})
    
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "google.com/image")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "google.com/image", "alt": "This is an image"})
    
    def test_splitter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )
    
    def test_splitter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )
    
    def test_splitter_delim_pair(self):
        # In the implementation, make sure that delimiter and TextType always match for split_nodes_delimiter
        # It is implementers responcebility to ensure this is the case
        pass

    def test_splitter_with_none_text_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_splitter_with_invalid_markdown(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        try:
            split_nodes_delimiter([node], "`", TextType.CODE)
        except:
            return
    
    def test_splitter_with_invalid_markdown_2(self):
        node = TextNode("This is text with a **bold word", TextType.TEXT)
        try:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        except:
            return
    
    def test_splitter_recursive_code_bold(self):
        node = TextNode("This is text with a **bold** word and a `code block`", TextType.TEXT)
        new_bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_bold_nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode("", TextType.TEXT)
            ]
        )

    def test_splitter_recursive_italic_bold(self):
        node = TextNode("This is text with a **bold** word and an _italic_ word", TextType.TEXT)
        new_bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_bold_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_splitter_recursive_code_italic(self):
        node = TextNode("This is text with an _italic_ word and a `code block`", TextType.TEXT)
        new_bold_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_bold_nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode("", TextType.TEXT)
            ]
        )

    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_link_bad(self):
        text = "This is text with a link [to [][]boot dev](https://www.boot.dev) and [to youtube](https:()()//www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_image(self):
        text = "This is text with a ![rick [][] roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i()())().imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [])

if __name__ == "__main__":
    unittest.main()
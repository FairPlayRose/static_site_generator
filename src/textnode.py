from enum import Enum
from htmlnode import HTMLNode,LeafNode,ParentNode
from typing import Self
import re

class TextType(Enum):
    TEXT = "Normal text"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "Links"
    IMAGE = "Images"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other: Self):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
# == Worker functions ==
    
def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    out = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            out.append(node)
        else:
            split_text = node.text.split(f'{delimiter}')
            if len(split_text) % 2 == 0:
                raise Exception(f"Delimitor '{delimiter}' missing somewhere. Invalid Markdown.")
            
            out.extend([TextNode(text, TextType.TEXT if i % 2 == 0 else text_type) for i, text in enumerate(split_text)])
    
    return out

def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str,str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
    out = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            out.append(node)
            continue
        
        image_links = extract_markdown_images(node.text)

        # This would cause issues if the same image link with the same alt text is present in two different places in the node text,
        # but with maxsplit = 1 you only ever split on the first instance, so rest is a len 1 list.
        acc: list[str] = []
        last = node.text
        for image_link in image_links:
            first, *rest = last.split(f"![{image_link[0]}]({image_link[1]})", maxsplit=1)
            last = rest[0]
            acc.append(first)
        if last:
            acc.append(last)
        
        for i in range(len(acc) + len(image_links)):
            if i % 2 == 0:
                out.append(TextNode(acc[i//2], TextType.TEXT))
            else:
                out.append(TextNode(image_links[i//2][0], TextType.IMAGE, image_links[i//2][1]))
        
    return out

def split_nodes_link(old_nodes: list[TextNode]):
    out: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            out.append(node)
            continue
        
        link_links = extract_markdown_links(node.text)

        # This would cause issues if the same image link with the same alt text is present in two different places in the node text,
        # but with maxsplit = 1 you only ever split on the first instance, so rest is a len 1 list.
        acc: list[str] = []
        last = node.text
        for link_link in link_links:
            first, *rest = last.split(f"[{link_link[0]}]({link_link[1]})", maxsplit=1)
            last = rest[0]
            acc.append(first)
        if last:
            acc.append(last)
        
        for i in range(len(acc) + len(link_links)):
            if i % 2 == 0:
                out.append(TextNode(acc[i//2], TextType.TEXT))
            else:
                out.append(TextNode(link_links[i//2][0], TextType.LINK, link_links[i//2][1]))
        
    return out

def text_to_textnodes(text):
    nodes_1 = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes_2 = split_nodes_delimiter(nodes_1, "_", TextType.ITALIC)
    nodes_3 = split_nodes_delimiter(nodes_2, "`", TextType.CODE)
    nodes_4 = split_nodes_link(nodes_3)
    nodes_5 = split_nodes_image(nodes_4)
    return nodes_5
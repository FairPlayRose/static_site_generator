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

def extract_markdown_images(text: str) -> list[str]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[str]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    out = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            out.append(node)
            continue
        else:
            out.extend()
    
    return out

def split_nodes_link(old_nodes):
    pass
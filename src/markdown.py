from enum import Enum
from textnode import *
from htmlnode import *
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    return [text.strip() for text in markdown.split('\n\n')]

def is_consecutive(lst: list[tuple[str,str]]):
    # Helper function to determine if list is a sequence of numbers
    if not lst:
        return False
    if int(lst[0][1]) != 1:
        return False
    for i in range(len(lst) - 1):
        if int(lst[i][1]) + 1 != int(lst[i + 1][1]):
            return False
    return True

def block_to_block_type(markdown: str):
    if re.match(r"#{1,6} ", markdown):
        return BlockType.HEADING
    elif markdown[:3] == "```" and markdown[-3:] == "```":
        return BlockType.CODE
    elif all([re.match(r"^>", line) for line in markdown.split('\n')]):
        return BlockType.QUOTE
    elif all([re.match(r"^-", line) for line in markdown.split('\n')]):
        return BlockType.UNORDERED_LIST
    elif is_consecutive(re.findall(r"(\n|^)(\d*)\.", markdown)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def text_to_children(text) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block == "":
            continue

        match block_type:
            case BlockType.CODE:
                nodes.append(ParentNode("pre", [LeafNode("code", block[4:-4])]))
            case BlockType.HEADING:
                head_idx, text = block.split(" ", maxsplit=1)
                head_count = len(head_idx)
                nodes.append(ParentNode(f"h{head_count}", text_to_children(text)))
            case BlockType.QUOTE:
                texts = block.split("\n")
                text = " ".join([text[2:] for text in texts if text[2:] != ""])
                nodes.append(ParentNode("blockquote", text_to_children(text)))
            case BlockType.UNORDERED_LIST:
                texts = block.split("\n")
                childrens = [text_to_children(text[2:]) for text in texts if text[2:] != ""]
                nodes.append(ParentNode("ul", [ParentNode("li", children) for children in childrens]))
            case BlockType.ORDERED_LIST:
                texts = block.split("\n")
                childrens = [text_to_children(text[3:]) for text in texts if text[3:] != ""]
                nodes.append(ParentNode("ol", [ParentNode("li", children) for children in childrens]))
            case BlockType.PARAGRAPH:
                texts = block.split("\n")
                text = " ".join(texts)
                nodes.append(ParentNode("p", text_to_children(text)))
    
    return ParentNode("div", nodes)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if re.match(r"# ", block):
            return block[2:]
    
    raise Exception("Markdown has no title")
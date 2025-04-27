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
    elif re.match(r"^```.*?```$", markdown):
        return BlockType.CODE
    elif all([re.match(r"^> |\n> ", line) for line in markdown.split('\n')]):
        return BlockType.QUOTE
    elif all([re.match(r"^- |\n- ", line) for line in markdown.split('\n')]):
        return BlockType.UNORDERED_LIST
    elif is_consecutive(re.findall(r"(\n|^)(\d*)\.", markdown)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
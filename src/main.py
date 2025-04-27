from textnode import TextNode, TextType
import re

def is_consecutive(lst: list[str]):
    # Helper function to determine if list is a sequence of numbers
    if not lst:
        return False
    if int(lst[0][1]) != 1:
        return False
    for i in range(len(lst) - 1):
        if int(lst[i][1]) + 1 != int(lst[i + 1][1]):
            return False
    return True

def main():
    markdown = "1. This is an bad ordered list\n4. with items"
    out = re.findall(r"(\n|^)(\d*)\.", markdown)
    print(out)
    print(is_consecutive(out))

main()
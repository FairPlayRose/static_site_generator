from textnode import TextNode, TextType

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "google.com")
    print(node)

main()
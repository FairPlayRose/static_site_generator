import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(node.__repr__(), "tag: '', value: '', props: {}, children: []")

    def test_tag(self):
        node = HTMLNode(tag="Tag")
        self.assertEqual(node.__repr__(), "tag: 'Tag', value: '', props: {}, children: []")

    def test_value(self):
        node = HTMLNode(value="Some text here")
        self.assertEqual(node.__repr__(), "tag: '', value: 'Some text here', props: {}, children: []")
    
    def test_props(self):
        node = HTMLNode(props={"prop1": "nothing", "prop2": "something"})
        self.assertEqual(node.__repr__(), "tag: '', value: '', props: {'prop1': 'nothing', 'prop2': 'something'}, children: []")

    def test_children(self):
        node1 = HTMLNode()
        node2 = HTMLNode(tag="Tag")
        node3 = HTMLNode(value="Some text here")
        node = HTMLNode(children=[node1,node2,node3])
        self.assertEqual(node.__repr__(), "tag: '', value: '', props: {}, children: [tag: '', value: '', props: {}, children: []],[tag: 'Tag', value: '', props: {}, children: []],[tag: '', value: 'Some text here', props: {}, children: []],")

    def test_to_html(self):
        node = HTMLNode()
        try:
            node.to_html()
        except NotImplementedError:
            return
    
    def test_empty_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html(self):
        node = HTMLNode(props={"prop1": "nothing", "prop2": "something"})
        self.assertEqual(node.props_to_html(), ' prop1="nothing" prop2="something"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_left_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_siblings(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_bad_parent(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        try:
            parent_node.to_html()
        except ValueError:
            return

    def test_to_html_with_bad_child(self):
        child_node = LeafNode("span", None)
        parent_node = ParentNode("div", [child_node])
        try:
            parent_node.to_html()
        except ValueError:
            return

    def test_to_html_with_no_child(self):
        parent_node = ParentNode("div", [])
        try:
            parent_node.to_html()
        except ValueError:
            return
        
    def test_to_html_with_none_child(self):
        parent_node = ParentNode("div", None)
        try:
            parent_node.to_html()
        except ValueError:
            return

if __name__ == "__main__":
    unittest.main()
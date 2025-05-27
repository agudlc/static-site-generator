import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")

    def test_leaf_has_value(self):
        node = LeafNode("p")
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception),'All leaf nodes must have a value')

    def test_leaf_none_tag(self):
        node = LeafNode(None, "Hello without tag!")
        self.assertEqual(node.to_html(), "Hello without tag!")

    def test_leaf_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_b_props(self):
        node = LeafNode("b", "Pandaaa", {"class":"font-large font-black", "id":"Image123"})
        self.assertEqual(node.to_html(), '<b class="font-large font-black" id="Image123">Pandaaa</b>')
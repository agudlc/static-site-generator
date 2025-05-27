import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq(self):
        node = TextNode('This is a crazy node', TextType.NORMAL)
        node2 = TextNode('This is a normal node', TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode('This is a better node', TextType.ITALIC)
        self.assertEqual(node.url, None)

    def test_eq_2(self):
        node = TextNode('This is the worst node', TextType.IMAGE)
        node2 = TextNode('This is the worst node', TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_properties(self):
        node = TextNode('Is this a node?', TextType.LINK)
        node2 = TextNode('crazy', TextType.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
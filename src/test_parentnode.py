import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_multiple_children(self):
        first_leaf_node = LeafNode("b", "Bold text")
        second_leaf_node = LeafNode(None, "Normal text")
        third_leaf_node = LeafNode("i", "italic text")
        four_leaf_node = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [first_leaf_node, second_leaf_node, third_leaf_node, four_leaf_node])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_with_multiple_children_and_levels(self):
        first_leaf_node = LeafNode("b", "Bold text")
        second_leaf_node = LeafNode(None, "Normal text")
        third_leaf_node = LeafNode("i", "italic text")
        four_leaf_node = LeafNode(None, "Normal second")
        third_level_parent_node = ParentNode("h3", [four_leaf_node])
        second_level_parent_node_less = ParentNode("h1", [second_leaf_node,])
        second_level_parent_node_more = ParentNode("h2", [third_leaf_node, third_level_parent_node])
        parent_node = ParentNode("p", [first_leaf_node, second_level_parent_node_less, second_level_parent_node_more])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b><h1>Normal text</h1><h2><i>italic text</i><h3>Normal second</h3></h2></p>")

    def test_with_props_in_levels(self):
        first_leaf_node = LeafNode("a", "Link text", {"class":"bolder", "href":"https://www.google.com"})
        second_leaf_node = LeafNode(None, "Normal text")
        second_parent_node = ParentNode("p", [second_leaf_node], {"class":"subcontainer"})
        parent_node = ParentNode("div", [first_leaf_node, second_parent_node], {"class":"container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><a class="bolder" href="https://www.google.com">Link text</a><p class="subcontainer">Normal text</p></div>')
    
    def test_raise_none_tag(self):
        first_leaf_node = LeafNode(None, "Normal text")
        parent_node = ParentNode(None, [first_leaf_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "The node doesn't have a tag")

    def test_raise_none_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "The node doesn't have a children")
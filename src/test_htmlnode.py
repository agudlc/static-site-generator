import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_a(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(tag="a", props=props)
        to_props = node.props_to_html()
        props_str = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(to_props, props_str)

    def test_to_html_image(self):
        props = {
            "alt": "alt text",
            "src": "/path/smth.png"
        }
        node = HTMLNode(tag="image", props=props)
        to_props = node.props_to_html()
        props_str = ' alt="alt text" src="/path/smth.png"'
        self.assertEqual(to_props, props_str)

    def test_to_html_bold(self):
        props = {
            "class": "bg-light"
        }
        node = HTMLNode(tag="bold", value="carlos", props=props)
        to_props = node.props_to_html()
        props_str = ' class="bg-light"'
        self.assertEqual(to_props, props_str)
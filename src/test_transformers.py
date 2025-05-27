import unittest
from textnode import TextNode, TextType
from transformers import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestTransformersFn(unittest.TestCase):
    def test_text(self):
        node = TextNode("this is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "this is a text node")

    def test_text_bold(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")

    def test_text_italic(self):
        node = TextNode("This is a italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text")
        
    def test_text_code(self):
        node = TextNode("This is a code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text")

    def test_text_link(self):
        node = TextNode("This is link anchor text", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is link anchor text")
        self.assertEqual(html_node.props_to_html(), ' href="https://www.google.com"')

    def test_text_image(self):
        node = TextNode("This is an alt text", TextType.IMAGE, "/path/smth")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props_to_html(), ' src="/path/smth" alt="This is an alt text"')

class TestSplitNodes(unittest.TestCase):
    def test_node_creation(self):
        node = TextNode("This is a text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL)
        ])
    
    def test_node_bold(self):
        node = TextNode("This is a text with a **bold** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.NORMAL)
        ])

    def test_node_italic(self):
        node = TextNode("This is a text with a _italic_ word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.NORMAL)
        ])

    def test_multiple_nodes(self):
        node_code = TextNode("This is a text with a `code block` word", TextType.NORMAL)
        node_bold = TextNode("This is a text with a **bold** word", TextType.NORMAL)
        node_italic = TextNode("This is a text with a _italic_ word", TextType.NORMAL)
        new_nodes_code = split_nodes_delimiter([node_code, node_bold, node_italic], "`", TextType.CODE)
        self.assertListEqual(new_nodes_code, [TextNode('This is a text with a ', TextType.NORMAL), TextNode("code block", TextType.CODE), TextNode(" word", TextType.NORMAL), TextNode("This is a text with a **bold** word", TextType.NORMAL) , TextNode("This is a text with a _italic_ word", TextType.NORMAL)])

    def test_bold_italic(self):
        node = TextNode("**bold** and _italic_", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(new_nodes, [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC)
        ])

    def test_double_code(self):
        node = TextNode("`one code` test for `two codes`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(new_nodes, [
            TextNode("one code", TextType.CODE),
            TextNode(" test for ", TextType.NORMAL),
            TextNode("two codes", TextType.CODE)
        ])

    def test_wrong_format(self):
        node = TextNode("This is a wrong `text syntax", TextType.NORMAL)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "Is not valid markdown syntax")

class TestExtractingProps(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [alt text](https://www.google.com)")
        self.assertListEqual(matches, [("alt text", "https://www.google.com")])

    def test_multiple_images(self):
        matches = extract_markdown_images("This is text with two images: 1 - ![image1](https://i.imgur.com/zjjcJKZ.png), 2 - ![image2](/path/smth)")
        self.assertListEqual(matches, [("image1", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "/path/smth")])

    def test_multiple_links(self):
        matches = extract_markdown_links("This is text with two links: 1 - [link1](https://www.google.com), 2 - [link2](https://www.boot.dev)")
        self.assertListEqual(matches, [("link1", "https://www.google.com"), ("link2", "https://www.boot.dev")])

    def test_images_and_links(self):
        text = "This is text with an image ![image](https://i.imgur.com/zjjcJKZ.png) and a link [link](https://www.google.com)"
        matches_images = extract_markdown_images(text)
        matches_links = extract_markdown_links(text)
        self.assertListEqual(matches_images, [("image", "https://i.imgur.com/zjjcJKZ.png")])
        self.assertListEqual(matches_links, [("link", "https://www.google.com")])

class TestSplittingImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode("This is text with a [link](https://www.google.com) and another [second link](https://www.boot.dev)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second link", TextType.LINK, "https://www.boot.dev"
                ),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.NORMAL),
            ],
            new_nodes,
        )

class TestTextToNodes(unittest.TestCase):
    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_text_multiple_images_and_links(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg), another ![second image](/path/somth), a [link](https://boot.dev) and a [second link](https://www.google.com)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(", another ", TextType.NORMAL),
            TextNode("second image", TextType.IMAGE, "/path/somth"),
            TextNode(", a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("second link", TextType.LINK, "https://www.google.com"),
        ])

    def test_text_multiple_italics(self):
        text = "This is **text** with an _italic_ and _gorgeous_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg), another ![second image](/path/somth), a [link](https://boot.dev) and a [second link](https://www.google.com)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.NORMAL),
            TextNode("gorgeous", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(", another ", TextType.NORMAL),
            TextNode("second image", TextType.IMAGE, "/path/somth"),
            TextNode(", a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("second link", TextType.LINK, "https://www.google.com"),
        ])

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_block(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_excessive_newlines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks, [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ])

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_heading(self):
        block = "##### This is a h5"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_heading_fail(self):
        block = "###Fail heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_heading_second_fail(self):
        block = "##!# Second Fail"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_code(self):
        block = "``` const javascript = cool ```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_fail(self):
        block = "``` const javascript = good ``"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_quote(self):
        block = ">Quoting Abraham Lincoln"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_unordered(self):
        block = "- This is a list/n- where we check the list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED)

    def test_block_unordered_fail(self):
        block = "-This is a fail\nHello"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_ordered(self):
        block = "1. first\n2. second\n3. third"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED)

    def test_block_ordered_fail(self):
        block = "1. first\n3. third\n2. second"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_block(self):
        md = """
- list item 1
- list item 2

- list item 3
- list item 4
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>list item 1</li><li>list item 2</li></ul><ul><li>list item 3</li><li>list item 4</li></ul></div>")

    def test_quote_block(self):
        md = """
>Quoting my father
>Quoting my mom
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>Quoting my father Quoting my mom</blockquote></div>")

    def test_ordered_block(self):
        md = """
1. first item
2. second item
3. third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>first item</li><li>second item</li><li>third item</li></ol></div>")

    def test_heading_block(self):
        md = """
### Heading three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>Heading three</h3></div>")

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )
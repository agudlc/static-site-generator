import re
from leafnode import LeafNode
from textnode import TextType, TextNode
from htmlnode import HTMLNode
from enum import Enum
from parentnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED = 'unordered_list'
    ORDERED = 'ordered_list'


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("Text type not allowed")
    match text_node.text_type:
        case TextType.NORMAL:
            clean_text = text_node.text.replace("\n", " ")
            return LeafNode(None, clean_text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        split_list = []
        splitted_node = node.text.split(delimiter)
        if len(splitted_node) % 2 == 0:
            raise Exception(f"Is not valid markdown syntax")
        for i in range(len(splitted_node)):
            if splitted_node[i] == '':
                continue
            if i % 2 == 0:
                split_list.append(TextNode(splitted_node[i], TextType.NORMAL))
            else:
                split_list.append(TextNode(splitted_node[i], text_type))
        new_nodes.extend(split_list)
    return new_nodes    

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL or node.text == '':
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        current_text = node.text
        node_list = []
        for alt, url in images:
            splitted_text = current_text.split(f"![{alt}]({url})", maxsplit=1)
            if splitted_text[0]:
                node_list.append(TextNode(splitted_text[0], TextType.NORMAL))
            node_list.append(TextNode(alt, TextType.IMAGE, url))
            if len(splitted_text) > 1:
                current_text = splitted_text[1]
            else:
                current_text = ''
        if current_text:
            node_list.append(TextNode(current_text, TextType.NORMAL))
        new_nodes.extend(node_list)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL or node.text == '':
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        current_text = node.text
        node_list = []
        for text, url in links:
            splitted_text = current_text.split(f"[{text}]({url})", maxsplit=1)
            if splitted_text[0]:
                node_list.append(TextNode(splitted_text[0], TextType.NORMAL))
            node_list.append(TextNode(text, TextType.LINK, url))
            if len(splitted_text) > 1:
                current_text = splitted_text[1]
            else:
                current_text = ''
        if current_text:
            node_list.append(TextNode(current_text, TextType.NORMAL))
        new_nodes.extend(node_list)
    return new_nodes

def text_to_textnodes(text):
    initial_node = TextNode(text,TextType.NORMAL)
    bold_text = split_nodes_delimiter([initial_node], "**", TextType.BOLD)
    italic_text = split_nodes_delimiter(bold_text, "_", TextType.ITALIC)
    code_text = split_nodes_delimiter(italic_text, "`", TextType.CODE)
    images_extract = split_nodes_image(code_text)
    links_extract = split_nodes_link(images_extract)
    return links_extract

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for item in blocks:
        if item in "":
            continue
        new_blocks.append(item.strip())
    return new_blocks

def block_to_block_type(block):
    if block[0] == ">":
        return BlockType.QUOTE
    if block[:2] == "- ":
        return BlockType.UNORDERED
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    if block[0] == "#":
        if re.match(r"^#{1,6} ", block):
            return BlockType.HEADING
    if block[1] == "." and block[0].isdigit():
        blocks = block.split("\n")
        for i, text in enumerate(blocks):
            have_digits = re.match(r"^(\d+)\.\s", text)
            if not have_digits or int(have_digits.group(1)) != i + 1:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes

def count_leading_hashes(s):
    count = 0
    for char in s:
        if char == "#":
            count += 1
        else:
            break
    return count

def type_block_to_html_node(block_type, block):
    match block_type:
        case BlockType.QUOTE:
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                if line.startswith(">"):
                    cleaned_line = line[1:].lstrip()
                    cleaned_lines.append(cleaned_line)
                else:
                    cleaned_lines.append(line)
            cleaned_block = "\n".join(cleaned_lines)
            children = text_to_children(cleaned_block)

            quote_node = HTMLNode("blockquote", None, children)
            return quote_node
        case BlockType.UNORDERED:
            lines = block.split("\n")
            ul_children = []
            for line in lines:
                li_children = text_to_children(line[2:].lstrip())
                li_node = HTMLNode("li", None, li_children)
                ul_children.append(li_node)
            ul_node = HTMLNode("ul", None, ul_children)
            return ul_node
        case BlockType.CODE:
            lines = block.split("\n")
            code_content = "\n".join(lines[1:-1]) + "\n"
            text_node = TextNode(code_content, TextType.CODE)
            code_node = text_node_to_html_node(text_node)
            pre_node = HTMLNode("pre", None, [code_node])
            return pre_node
        case BlockType.HEADING:
            heading_number = count_leading_hashes(block)
            children = text_to_children(block[heading_number+1:].lstrip())
            heading_node = HTMLNode(f"h{heading_number}", None, children)
            return heading_node
        case BlockType.ORDERED:
            lines = block.split("\n")
            ol_children = []
            for line in lines:
                li_children = text_to_children(line[2:].lstrip())
                li_node = HTMLNode("li", None, li_children)
                ol_children.append(li_node)
            ol_node = HTMLNode("ol", None, ol_children)
            return ol_node
        case BlockType.PARAGRAPH:
            children = text_to_children(block)
            paragraph_node = HTMLNode("p", None, children)
            return paragraph_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for item in blocks:
        block_type = block_to_block_type(item)
        node = type_block_to_html_node(block_type, item)
        children.append(node)
    parent_node = ParentNode("div", children)
    return parent_node
        

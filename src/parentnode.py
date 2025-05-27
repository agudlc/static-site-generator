from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("The node doesn't have a tag")
        if self.children == None:
            raise ValueError("The node doesn't have a children")
        mapped_children = ''.join(list(map( lambda node: node.to_html() , self.children)))
        return f"<{self.tag}{self.props_to_html()}>{mapped_children}</{self.tag}>"
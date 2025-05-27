from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self,  tag=None, value=None, props=None):
        super().__init__(tag=tag,value=value, props=props)
    
    def to_html(self):
        if self.value == None:
            print(self)
            raise ValueError('All leaf nodes must have a value')
        if self.tag == None:
            return f"{self.value}"
        props = self.props_to_html()
        tagged = f"<{self.tag}{props}>{self.value}</{self.tag}>"
        return tagged
        
        
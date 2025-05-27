class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            if self.value is None:
                raise ValueError("Node without tag must have a value")
            return self.value
        
        if self.value is not None and self.children is not None:
            raise ValueError("Node cannot have both a value and children")
        
        props_html = self.props_to_html()

        if self.children is not None:
            children_html = "".join(child.to_html() for child in self.children)
            return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
        
        if self.value is not None:
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
        
        return f"<{self.tag}{props_html}></{self.tag}>"
    
    def props_to_html(self):
        if not self.props:
            return ''
        props_tuples = list(self.props.items())
        mapped_keys = ' '.join(map(lambda k: f"{k[0]}=\"{k[1]}\"", props_tuples))
        return f" {mapped_keys}"
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
     
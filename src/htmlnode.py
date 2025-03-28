class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props)
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_string = ""
        for key, value in self.props.items():
            props_string += f' {key}="{value}"'
        return props_string
    
    def __repr__(self):
        print (f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (self.tag == other.tag and self.value == other.value and self.props == other.props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("value needed for LeafNode")
        if not self.tag:
            return self.value
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        props_string = ""
        for key, value in self.props.items():
            props_string += f' {key}="{value}"'
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children,  props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if not self.tag:
            raise ValueError("tag needed for ParentNode")
        if not self.children:
            raise ValueError("children missing for ParentNode")
        children_string = ""
        for child in self.children:
            children_string += child.to_html()
        
        if not self.props:
            return f"<{self.tag}>{children_string}</{self.tag}>"
        else:
            props_string = ""
            for key, value in self.props.items():
                props_string += f' {key}="{value}"'
            return f"<{self.tag}{props_string}>{children_string}</{self.tag}>"
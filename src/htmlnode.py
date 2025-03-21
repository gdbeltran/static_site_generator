class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_list = []
        for key, prop in self.props:
            props_list.append(f" {key}={prop}")
        return props_list
    
    def __repr__(self):
        print (f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")
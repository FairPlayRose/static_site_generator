from typing import Self

# == Node Classes ==
class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[Self] | None = None, props: dict[str,str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        return "".join([f' {k}="{v}"' for k,v in self.props.items()])
    
    # implement indentation decorator?
    def __repr__(self):
        out = ""
        
        out += f"tag: '{self.tag}', " if self.tag != None else "tag: '', "
        out += f"value: '{self.value}', " if self.value != None else "value: '', "
        out += f"props: {self.props}, " if self.props != None else "props: {}, "
        if self.children:
            out += "children: "
            for child in self.children:
                out += f"[{child.__repr__()}],"
        else:
            out += "children: []"
        return out
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf nodes must be non-empty.")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag Error - No tag given for html element.")
        if (not self.children) or (self.children == None):
            raise ValueError("Node Error - Parent nodes must have child nodes")
        if isinstance(self.children, str):
            raise ValueError("value given where child node expected")
        
        value = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{value}</{self.tag}>"


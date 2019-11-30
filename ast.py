import json


class AstNode:
    def __init__(self, root_dict):
        self.type = root_dict["type"][25:]
        if 'start' in root_dict:
            self.start = root_dict["start"]
            self.end = root_dict["end"]
        props = []
        if 'declares' in root_dict:
            self.declares = root_dict['declares']
        if 'key' in root_dict:
            self.key = root_dict['key']

        for k, v in root_dict["properties"].items():
            # print(k, ' ', v)
            if isinstance(v, list):
                # print(k, ' ', v)
                props += [(k, AstNode(x)) for x in v]
            elif isinstance(v, dict):
                # print(k, ' ', v)
                props.append((k, AstNode(v)))
            else:
                props.append((k, v))
        # print(props)
        self.properties = props

    # def list_view(self, name) -> List:
    #     try:
    #         value = self.properties[name]
    #         if isinstance(value, list):
    #             return value
    #         else:
    #             return [value]
    #     except KeyError:
    #         return []

    # @property
    # def meta(self):
    #     return SimpleNamespace(**self.meta_dict())

    def meta_dict(self):
        return [x for x in self.properties if not isinstance(x[1], AstNode)]
        # return {k: v for k, v in self.properties.items() if not isinstance(v, (list, AstNode))}

    # @property
    # def child(self):
    #     return SimpleNamespace(**self.children_dict())

    def children_dict(self):
        return [x for x in self.properties if isinstance(x[1], AstNode)]
        # return {k: v for k, v in self.properties.items() if isinstance(v, (list, AstNode))}

    def __str__(self):
        return "<{type}{metas}>".format(
            type=self.type,
            metas=" " + ",".join("%s=%s" % x for x in self.meta_dict())
        )

    def __repr__(self):
        return str(self)

    def dfs(self, behavior):
        behavior.pre(self)
        ch = self.children_dict()
        for u in ch:
            # print("#", u)
            behavior.f_edge = u[0]
            u[1].dfs(behavior)
        behavior.post(self)


class DoOnAST:
    def __init__(self):
        self.layers = 0
        self.nodeCount = 0
        self.preOrder = []
        self.postOrder = []
        self.f_edge = "root"

    def pre(self, node):
        self.nodeCount += 1
        self.preOrder.append(node.type)
        for x in range(self.layers):
            print("    ", end="")
        print(node.type)
        self.layers += 1

    def post(self, node):
        self.postOrder.append(node.type)
        self.layers -= 1


if __name__ == '__main__':
    f = open('Main.json')
    f = open("RowIterators.json")
    js = json.loads(f.read())
    # print(js)
    bh = DoOnAST()
    ast = AstNode(js)
    ast.dfs(bh)
    print(bh.nodeCount)
    print(bh.preOrder)
    print(bh.postOrder)

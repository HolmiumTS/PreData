import json
import os

from ast import AstNode


class MethodSelector:
    def __init__(self, typeDict):
        self.method = None
        self.params = []
        self.typeDict = typeDict
        self.path = ""
        self.count = 0
        self.preOrder = []
        self.postOrder = []
        self.file = None
        self.ast = None
        self.mxlen = 0
        self.file = open(r"D:\Codes\AIProjects\T1\test1.txt", "w")
        pass

    def dfs(self, node, param_name):
        fl = 0
        # if hasattr(node, "start"):
        #     print(node.start, ' ', node.type)
        # else:
        #     print(node.type)
        if hasattr(node, "type"):
            self.preOrder.append(node.type)
        else:
            return 0
        ch = node.children_dict()
        meta = node.meta_dict()
        for son in meta:
            if son == ("identifier", param_name) and node.type == "SimpleName":
                self.postOrder.append(node.type)
                return 1
        for son in ch:
            fl = self.dfs(son[1], param_name) or fl
        if fl:
            self.postOrder.append(node.type)
        else:
            del self.preOrder[-1]
        return fl

    def dfs1(self, node):
        if node.type == "MethodDeclaration":
            self.setM(node)
            self.selectM()
            # print(self.params)
            return
        ch = node.children_dict()
        for p in ch:
            if isinstance(p[1], AstNode):
                self.dfs1(p[1])

    def getParams(self):
        self.params = []
        for pro in self.method.properties:
            if pro[0] == "parameters":
                for pa in pro[1].properties:
                    if pa[0] == "name":
                        ch = pa[1].meta_dict()
                        # print(ch)
                        for name in ch:
                            if name[0] == "identifier":
                                self.params.append(name[1])

    def setAST(self, ast_js, path):
        self.count = 0
        self.ast = AstNode(ast_js)
        self.path = path
        # self.file = open(self.path, "w")
        self.dfs1(self.ast)
        # self.file.close()

    def setM(self, node):
        self.method = node

    def clear(self):
        self.preOrder = []
        self.postOrder = []

    def selectM(self):
        tmp = None
        self.getParams()
        for son in self.method.properties:
            if son[0] == "body":
                tmp = son[1]
        for param in self.params:
            self.clear()
            self.count += 1
            # print(param)
            tmp = self.dfs(tmp, param)
            if tmp == 0:
                continue
            order = [self.typeDict[x] for x in self.preOrder] + [-1] + [self.typeDict[x] for x in self.postOrder]
            # print(order)
            if len(order) == 0:
                continue
            s = param + " " + str(len(order)) + " "
            for n in order:
                for x in range(133):
                    if x == n:
                        s += "1 "
                    else:
                        s += "0 "
            # print(self.path)
            if 35 <= len(order) < 50:
                self.file.write(s + "\n")
            # self.mxlen = max(self.mxlen, len(order))
            # print(s)


def scan_files(directory, prefix=None, postfix=None):
    files_list = []

    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))

    return files_list


if __name__ == "__main__":
    f = open("ASTNodeType.txt")
    tmp = f.readlines()
    cnt = 0
    typeDict = {}
    for tp in tmp:
        typeDict[tp[:-1]] = cnt
        cnt += 1
    m = MethodSelector(typeDict)
    f.close()
    files = scan_files(r"D:\Codes\AIProjects\JSData\training\cassandra", postfix=".json")
    # pt = r"D:\Codes\AIProjects\MData\training\gradle"
    pt = r"D:\Codes\AIProjects\T1\test1.txt"
    for file in files:
        f = open(file)
        # d = os.path.join(pt, str(file.split('\\')[-1]))
        # print(d)
        m.setAST(json.loads(f.read()), pt)
        f.close()
    print(m.mxlen)
    m.file.close()

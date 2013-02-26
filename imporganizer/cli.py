import argparse
import ast

from collections import namedtuple


Import = namedtuple(
    'Import',
    ['name', 'asname'],
)


ImportFrom = namedtuple(
    'ImportFrom',
    ['module', 'names', 'level'],
)


class MyVisitor(ast.NodeVisitor):
    def __init__(self, root_node):
        self.root_node = root_node
        self.imports = []

    def is_top_level_node(self, node):
        return node in self.root_node.body

    def visit_Import(self, node):
        if self.is_top_level_node(node):
            self.imports.extend(
                [Import(n.name, n.asname)
                 for n in node.names]
            )

    def visit_ImportFrom(self, node):
        if self.is_top_level_node(node):
            self.imports.append(
                ImportFrom(
                    module=node.module,
                    names=[
                        Import(
                            name=name.name,
                            asname=name.asname)
                        for name in node.names
                    ],
                    level=node.level,
                )
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    args = parser.parse_args()

    target_file = args.target

    with open(target_file) as f:
        root_node = ast.parse(f.read())

    visitor = MyVisitor(root_node)
    visitor.visit(root_node)
    print visitor.imports

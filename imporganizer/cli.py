import argparse
import ast

from collections import namedtuple


Name = namedtuple(
    'Name',
    ['name', 'asname'],
)

Import = namedtuple(
    'Import',
    ['node', 'names'],
)


ImportFrom = namedtuple(
    'ImportFrom',
    ['node', 'module', 'names', 'level'],
)


class MyVisitor(ast.NodeVisitor):
    def __init__(self, root_node):
        self.root_node = root_node
        self.imports = []

    def is_top_level_node(self, node):
        return node in self.root_node.body

    def visit_Import(self, node):
        if self.is_top_level_node(node):
            self.imports.append(
                Import(
                    node=node,
                    names=[
                        Name(n.name, n.asname)
                        for n in node.names
                    ]))

    def visit_ImportFrom(self, node):
        if self.is_top_level_node(node):
            self.imports.append(
                ImportFrom(
                    node=node,
                    module=node.module,
                    names=[
                        Name(
                            name=name.name,
                            asname=name.asname)
                        for name in node.names
                    ],
                    level=node.level,
                )
            )


class ImportOrganizer(object):
    def __init__(self, stream):
        self.stream = stream
        self.root_node = ast.parse(self.stream.read())

    def _collect_imports(self, visitor):
        visitor.visit(self.root_node)
        return visitor.imports

    def _remove_nodes_from_root(self, nodes):
        for node in nodes:
            self.root_node.body.remove(node)

    def __call__(self):
        visitor = MyVisitor(self.root_node)
        imports = self._collect_imports(visitor)
        self._remove_nodes_from_root(
            [import_.node for import_ in imports])

        print ast.dump(self.root_node)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    args = parser.parse_args()

    target_file = args.target

    with open(target_file) as f:
        ImportOrganizer(f)()


import typing

from node import Node

from LL1 import LL1


class ParserOutput:

    def __init__(
        self,
        parser: LL1,
        sequence: typing.Tuple[bool, typing.List[int]]
    ):
        self.parser = parser
        self.sequence: typing.List[int] = sequence[1]

        self.output = []
        nodes = []
        self.root = Node(parser.grammar.startingPoint)
        self.root.index = 1

        self.tree = []

        self.EPSILON = "ε"

        if not sequence[0]:
            raise Exception("Sequence is not valid")


    def generate_parse_tree(self):
        nodes = [self.root]
        self.tree = [self.root]
        node_index = 2
        index = 0

        while index < len(self.sequence) and len(nodes) > 0:
            node = nodes[-1]

            if node.value in self.parser.grammar.terminals + [self.EPSILON]:
                while len(nodes) > 0 and nodes[-1].right_sibling is None:
                    nodes.pop()

                if len(nodes) == 0:
                    break

                nodes.pop()
                continue

            
            production = self.parser.get_production_by_label(self.sequence[index])
            production.reverse()

            for i, value in enumerate(production):
                new_index = node_index  + len(production) - i - 1

                new_node = Node(value)
                new_node.parent = node
                new_node.index = new_index

                if i != 0:
                    new_node.right_sibling = new_index + 1

                
                nodes.append(new_node)
                self.tree.append(new_node)

            node_index += len(production)
            index += 1


    def print_parse_tree(self):
        # Sort the nodes by their index
        self.tree.sort(key = lambda node: node.index)
        
        string = ""
        for node in self.tree:
            parent = 0 if node.parent is None else node.parent.index
            right_sibling = 0 if node.right_sibling is None else node.right_sibling
            string += f"{node.index} {node.value} {parent} {right_sibling}\n"

        return string
    



            
    

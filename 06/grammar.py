import typing


class Grammar:
     
    def __init__(
        self,
        file: str,
    ):

        self.file = file

        self.nonterminals = []
        self.terminals = []
        self.startingPoint = ""
        self.production_rules = {}

    
    def scan(self):
        with open(self.file, 'r', encoding = 'utf-8') as file:
            lines = file.readlines()

            self.nonterminals = lines[0].split()
            self.terminals = lines[1].split()
            self.startingPoint = lines[2].strip()

            for index in range(3, len(lines)):
                key, values = lines[index].split("->")

                splitValues = values.split("|")

                if key not in self.production_rules.keys():
                    self.production_rules[key] = []

                for val in splitValues:
                    self.production_rules[key] += [val.strip()]
    

    def get_nonterminal_productions(
        self, 
        nonterminal: str
    ):
        if nonterminal in self.production_rules.keys():
            return self.production_rules[nonterminal]
    

    def is_context_fre(self) -> bool:
        for key in self.production_rules.keys():
            values = key.split()

            if len(values) > 1:
                return False
            
        return True


    def get_rhs_productions(
        self,
        nonterminal: str
    ) -> typing.List[typing.Tuple[str, typing.List[str]]]:
        rhs_productions = []

        for key, prods in self.production_rules.items():
            for prod in prods:
                nodes = prod.split()
                result_nodes = nodes.copy()

                for node in nodes:
                    result_nodes.remove(node)

                    if nonterminal == node:
                        rhs_productions += [(key, result_nodes)]
                        break 


        return rhs_productions
    

   
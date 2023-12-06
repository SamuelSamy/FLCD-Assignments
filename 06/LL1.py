import json
from grammar import Grammar


class LL1:
    def __init__(
        self,
        grammar: Grammar
    ):
        self.grammar = grammar
        self.firsts_set = {}
        self.follow_set = {}

        self.EPSILON = "ε"

        self.parser_table = {}

    
    def size_one_concat(self, terminal, nonterminals):

        if len(nonterminals) == 0:
            return set() # it means that we have added the terminals 
        
        if len(nonterminals) == 1:
            return self.firsts_set[nonterminals[0]] # we have to add the first of only one elem
        
        
        concat = set()

        # if all nonterminals contain epsilon => we have to add the first found terminal
        all_nonterminals_contain_epsilon = True

        for elem in nonterminals:
            if not self.EPSILON in self.firsts_set[elem]:
                all_nonterminals_contain_epsilon = False

        if all_nonterminals_contain_epsilon:
            if terminal != "":
                concat.add(terminal)
            else:
                concat.add(self.EPSILON)
        
        # first we put the first of the first nonterminal and if that contains ε we increase the index
        # and we put the first of the next element, we do this until the current elem does not contain ε
        # or if we reached the end of the list of nonterminals 
        index = 0 

        while index < len(nonterminals):
            nonterminal_contains_epsilon = False
            current_first_values = self.firsts_set[nonterminals[index]]

            for elem in current_first_values:
                if elem == self.EPSILON:
                    nonterminal_contains_epsilon = True
                else:
                    concat.add(elem)
            
            # the current terminal contains ε => we also take the first of the next terminal
            if nonterminal_contains_epsilon:
                index = index + 1
            else:
                break # if the current terminal does NOT contain ε => the first is composed only of its first
        
        return concat


    
    def FIRST(self):
        
        # we have to compute FIRST of each nonterminal
        nonterminals_list = self.grammar.nonterminals

        # FIRST0
        for nonterminal in nonterminals_list:
            self.firsts_set[nonterminal] = set() # initialize current FIRST with empty set for each nonterminal

            productions_of_nonterminal = self.grammar.get_nonterminal_productions(nonterminal)

            for production_string in productions_of_nonterminal:
                # if the production of a nonterminal starts with terminal or epsilon
                if production_string[0] in self.grammar.terminals or production_string[0] == 'ε':
                    self.firsts_set[nonterminal].add(production_string[0])

        # we stop when the current column FIRST is equal to the prev column FIRST
        changed_first = True

        while changed_first:
            changed_first = False

            # current_column contains the current FIRST for each nonterminal
            current_column = {}

            for nonterminal in nonterminals_list:
                productions_of_nonterminal = self.grammar.get_nonterminal_productions(nonterminal)
            
                # current_first contains the current terminals for each nonterminal
                # firstly, we get what we had in the prev first
                current_first = set()
                current_first.update(self.firsts_set[nonterminal])

                for production_string in productions_of_nonterminal:
                    production_symbols = production_string.split()
                    production_nonterminals = [] # we put the nonterminals in the right hand side until we reach a terminal
                    production_first_terminal = "" # we stop when we find the first terminal in the right hand side

                    for symbol in production_symbols:
                        if symbol in self.grammar.nonterminals:
                            production_nonterminals.append(symbol)
                        else:
                            production_first_terminal = symbol
                            break

                    current_first.update(self.size_one_concat(production_first_terminal, production_nonterminals))
                
                if current_first != self.firsts_set[nonterminal]:
                    changed_first = True
                
                current_column[nonterminal] = current_first

            # the FIRST is represented by the last computed column
            self.firsts_set = current_column 
                    

        
    def FOLLOW(self):
        
        for nonterminal in self.grammar.nonterminals:
            self.follow_set[nonterminal] = set()

            if nonterminal == self.grammar.startingPoint:
                self.follow_set[nonterminal].add(self.EPSILON)
        
        current_column = {}

        while current_column != self.follow_set:
            
            for nonterminal in self.grammar.nonterminals:
                
                current_column[nonterminal] = self.follow_set[nonterminal] # Initialize the current column with the previous column

                rhs_prods = self.grammar.get_rhs_productions(nonterminal)

                for rhs_prod in rhs_prods:
                    left_node = rhs_prod[0] # The left node of the production
                    right_nodes = rhs_prod[1] # The right nodes of the production

                    if len(right_nodes) == 0: # We do not have any nodes in the right hand side, therefore everything in follow(left_node) is in follow(nonterminal)
                        current_column[nonterminal].update(self.follow_set[left_node])
                        continue

                    for i in range(len(right_nodes)): # Iterate through the nodes in the right hand side
                        node = right_nodes[i]

                        if node in self.grammar.terminals: # If the current node is a terminal, we add it to follow(nonterminal) and break
                            current_column[nonterminal].add(node)
                            break

                        firsts = self.firsts_set[node] # Get the firsts of the current node

                        current_column[nonterminal].update(firsts - {self.EPSILON}) # Add the firsts of the current node to follow(nonterminal) without epsilon

                        if self.EPSILON not in firsts:
                            break
                            
                        if i == len(right_nodes) - 1: # We reached the end of the right hand side and all the nodes contain epsilon
                            current_column[nonterminal].update(self.follow_set[left_node]) # Add follow(left_node) to follow(nonterminal)

            self.follow_set = current_column

    def get_production_first(self, prod: str):
        nonterminals, terminal = [], ""
        prod = prod.split()

        if prod[0] in self.grammar.terminals + [self.EPSILON]:
            return set(prod[0])

        for node in prod:
            if node in self.grammar.terminals + [self.EPSILON]:
                terminal = node
                break
            nonterminals.append(node)
        
        return self.size_one_concat(terminal, nonterminals)
        

    def init_parser_table(self):
        self.parser_table = {}

        for nonterm in self.grammar.nonterminals:
            self.parser_table[nonterm] = {}
        
        for term in self.grammar.terminals:
            self.parser_table[term] = {}
        
        self.parser_table["$"] = {}

        for node in self.parser_table.keys():
            for term in self.grammar.terminals + ["$"]:
                self.parser_table[node][term] = []  


    def construct_parser_table(self):
        self.init_parser_table()

        self.parser_table["$"]["$"] = ("accept")

        for term in self.grammar.terminals:
            self.parser_table[term][term] += ("pop")

        for nonterm in self.grammar.nonterminals:
            for prod in self.grammar.get_nonterminal_productions(nonterm):
                first = self.get_production_first(prod)

                if self.EPSILON in first:
                    follow = self.follow_set[nonterm]

                    for node in follow:
                        node = node if node != self.EPSILON else "$"
                        self.parser_table[nonterm][node] += (prod) # TUPLE
                
                    first.remove(self.EPSILON)

                for node in first:
                    self.parser_table[nonterm][node] += (prod)
        

                







        



            

    

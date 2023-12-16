import json
import typing
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

        self.production_labels = {}
        self.__label_productions()

    
    def size_one_concat(self, terminal, nonterminals):
        """
        The size_one_concat function in context-free grammar analysis combines the FIRST sets of a sequence of non-terminals, optionally starting with a terminal symbol. 
        It returns an empty set for no non-terminals and directly returns the FIRST set for a single non-terminal. 
        If all non-terminals can derive epsilon (ε), it adds a given terminal to the set, or ε if no terminal is provided. 
        Concatenation logic is the following: Iteratively adds symbols from each non-terminal FIRST set to a concat set, excluding ε, until it encounters a non-terminal that doesn't derive ε. 
        Finally, it returns the concat set, representing the combined FIRST set of the given sequence of non-terminals and the initial terminal.
        """

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
        """
        The code initializes empty FIRST sets for each non-terminal in the grammar. 
        It populates the FIRST sets with terminals or epsilon directly derivable from non-terminals. 
        The algorithm enters a loop to iteratively refine the FIRST sets. During each iteration, the FIRST set of each non-terminal is updated based on its productions. 
        The process identifies the first terminal symbol in each production or accumulates non-terminals until a terminal is encountered. 
        The function, size_one_concat() is used for combining these symbols to update the FIRST set. 
        The loop continues until there are no changes in any FIRST set during an iteration. 
        Finally, self.firsts_set holds the complete FIRST sets for each non-terminal, marking the end of the computation.
        """
        
        # we have to compute FIRST of each nonterminal
        nonterminals_list = self.grammar.nonterminals

        # FIRST0
        for nonterminal in nonterminals_list:
            self.firsts_set[nonterminal] = set() # initialize current FIRST with empty set for each nonterminal

            productions_of_nonterminal = self.grammar.get_nonterminal_productions(nonterminal)

            if productions_of_nonterminal is None:
                raise Exception(f"Nonterminal {nonterminal} does not have any productions")

            for production_string in productions_of_nonterminal:
                # if the production of a nonterminal starts with terminal or epsilon
                production_string = production_string.split()
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
        """
        Firstly the function initializes the follow set for each nonterminal with an empty set (except for the starting point which contains epsilon)
        The algorithm stops when the current column is equal to the previous column
        For each nonterminal we initialize the current column with the previous column. Then we use the `get_rhs_productions` function to get the productions in which the nonterminal appears in the right hand side.
        For each production we get the left node and the right nodes. 
        If the right nodes are empty we add the follow of the left node to current's node follow set.
        If the right nodes are not empty we iterate through them.
            - If the current node is a terminal we add it to the current node's follow set and break
            - We get the firsts of the current node and add them to the current node's follow set without epsilon
            - If the current node's firsts do not contain epsilon we break
            - If we reached the end of the right nodes and all of them contain epsilon we add the follow of the left node to the current node's follow set
        """

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
        """
        This function computes the FIRST set of a production rule.
        - If the production rule starts with a terminal, the FIRST set is the terminal itself.
        - If the production rule does not start with a terminal, we iterate through the symbols in the production rule until we find a terminal adding everything to a list of nonterminals.
        - We then call the size_one_concat function to compute the FIRST set of the nonterminals and the initial terminal.
        """
        nonterminals, terminal = [], ""
        prod = prod.split()

        if prod[0] in self.grammar.terminals + [self.EPSILON]:
            result = set()
            result.add(prod[0])
            return result

        for node in prod:
            if node in self.grammar.terminals + [self.EPSILON]:
                terminal = node
                break
            nonterminals.append(node)
        
        return self.size_one_concat(terminal, nonterminals)
        

    def init_parser_table(self):
        """
        Sets up an initial parsing table for a given grammar. 
        It starts by creating an empty dictionary called parser_table, which will hold the parsing table. 
        For each non-terminal in the grammar, it adds a row in the table with an empty dictionary as its initial value. 
        Similarly, it adds rows for each terminal in the grammar, each initialized with an empty dictionary. 
        The function includes a special row for the end-of-input marker, $. 
        It then populates each cell of the table (corresponding to a pair of row and column headers) with empty lists. 
        These cells are intersections of non-terminals and terminals, including the end-of-input marker.
        """
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
        """
        It begins by calling init_parser_table() to create an initial, empty parser table. 
        Then, it sets an "accept" action for the end-of-input marker ($) in the parser table, indicating the successful completion of parsing. 
        For each terminal, a "pop" action is added, instructing the parser to remove the terminal from the stack when it matches the input symbol. 
        The function iterates over each non-terminal and its productions. 
            - For each production, it computes the FIRST set (first). If epsilon (ε) is in the FIRST set, the FOLLOW set of the non-terminal (follow) is used. 
            - Each symbol in the FOLLOW set is mapped to the production in the parser table, with a special case handling for ε, which is replaced by $. 
            - For each symbol in the FIRST set (excluding ε), the production is added to the corresponding cell in the parser table. 
        """
        self.init_parser_table()

        self.parser_table["$"]["$"] += [("accept")]

        for term in self.grammar.terminals:
            self.parser_table[term][term] += [("pop")]

        for nonterm in self.grammar.nonterminals:
            for prod in self.grammar.get_nonterminal_productions(nonterm):
                first = self.get_production_first(prod)

                if self.EPSILON in first:
                    follow = self.follow_set[nonterm]

                    for node in follow:
                        node = node if node != self.EPSILON else "$"
                        self.parser_table[nonterm][node].append([prod, self.production_labels[f'{nonterm}`{prod}']])
                
                    first.remove(self.EPSILON)

                for node in first:
                    self.parser_table[nonterm][node].append([prod, self.production_labels[f'{nonterm}`{prod}']])
        

                
    def __label_productions(self):
        """
        This method assigns unique labels to each production rule. 
        It iterates through the production rules and assigns an incrementing number as a label to each rule. 
        These labels are stored in self.production_labels for easy reference and are used in construct_parser_table to include alongside productions in the parser table.
        """
        count = 0
        for key in self.grammar.production_rules.keys():
            for prod  in self.grammar.production_rules[key]:
                self.production_labels[f'{key}`{prod}'] = count + 1
                count += 1


    def is_ll1_grammar(self):
        """
        This method checks if the grammar is LL1.
        It iteraters through the parser table and checks if there are any conflicts in the table.
        """
        ll1 = True

        for nonterm in self.parser_table.keys():
            for term in self.parser_table[nonterm].keys():
                if len(self.parser_table[nonterm][term]) > 1:
                    print(f"Conflict in parser table for nonterminal {nonterm} and terminal {term} {self.parser_table[nonterm][term]}") 
                    ll1 = False

        return ll1


        
    def parse_sequence(
        self, 
        sequence: str
    ):
        """
        This method parses a given sequence using the parser table.
        It starts by initializing the working stack and input stack with the sequence.
        The working stack is initialized with the starting point of the grammar and the input stack is initialized with the sequence.
        The algorithm iterates until the input stack and the working stack are empty.
            - It gets the top of the input stack and the top of the working stack.
            - It gets the production from the parser table for the given nonterminal and terminal.
                - If the production is empty, it means that the sequence is not valid and an exception is raised.
                - If the production is "pop", it means that the parser should pop the top of the input stack and the top of the working stack.
                - If the production is "accept", it means that the sequence is valid and the algorithm returns True.
                - If the production is not empty, it means that the parser should replace the top of the working stack with the production.
            - The algorithm appends the production to the output stack.
        This method returns a tuple containing a boolean value and the output stack. (the boolean value indicates if the sequence is valid or not)
        """

        working_stack = []
        input_stack = []
        output = []

        sequence = sequence.split()
        
        for char in sequence:
            input_stack.append(char)
        input_stack.append("$")
        input_stack.reverse()


        working_stack.append("$")
        working_stack.append(self.grammar.startingPoint)

        while not input_stack[-1] == "$" or not working_stack[-1] == "$":

            input_top = input_stack[-1]
            working_top = working_stack[-1]

            pair = self.parser_table[working_top][input_top]

            if len(pair) == 0:
                raise Exception(f"Sequence is not valid. No production found for nonterminal {working_top} and terminal {input_top}")
                return False, output
            

            if len(pair) == 1 and pair[0] == "pop":
                input_stack.pop()
                working_stack.pop()
                continue

            if len(pair) == 1 and pair[0] == "accept":
                return True, output
            
            working_stack.pop()

            if pair[0][0] != self.EPSILON:
                prods = pair[0][0].split()
                prods.reverse()
                working_stack += prods
                

            output.append(pair[0][1])


        return True, output



    def get_production_by_label(self, index) -> typing.List[str]:
        """
        This method returns the production rule corresponding to a given label.
        """
        for key in self.production_labels.keys():
            if self.production_labels[key] == index:
                return key.split("`")[1].split()




            

    

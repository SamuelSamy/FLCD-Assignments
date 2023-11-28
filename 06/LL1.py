class LL1:
    def __init__(
        self,
        grammar
    ):
        self.grammar = grammar
        self.firsts_set = {}

    
    def size_one_concat(self, terminal, nonterminals):


        if len(nonterminals) == 0:
            return set() # it means that we have added the terminals 
        
        if len(nonterminals) == 1:
            return self.firsts_set[nonterminals[0]] # we have to add the first of only one elem
        
        concat = set()

        # if all nonterminals contain epsilon => we have to add the first found terminal
        all_nonterminals_contain_epsilon = True

        for elem in nonterminals:
            if not "ε" in self.firsts_set[elem]:
                all_nonterminals_contain_epsilon = False

        if all_nonterminals_contain_epsilon:
            if terminal != "":
                concat.add(terminal)
            else:
                concat.add("ε")
        
        # first we put the first of the first nonterminal and if that contains ε we increase the index
        # and we put the first of the next element, we do this until the current elem does not contain ε
        # or if we reached the end of the list of nonterminals 
        index = 0 

        while index < len(nonterminals):
            nonterminal_contains_epsilon = False

            for elem in self.firsts_set[nonterminals]:
                if elem == "ε":
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
        
        nonterminals_list = self.grammar.nonterminals

        for nonterminal in nonterminals_list:
            self.firsts_set[nonterminal] = set()

            productions_of_nonterminal = self.grammar.get_nonterminal_productions(nonterminal)

            for production_string in productions_of_nonterminal:
                # if the production of a nonterminal starts with terminal or epsilon
                if production_string[0] in self.grammar.terminals or production_string[0] == 'ε':
                    self.firsts_set[nonterminal] += production_string[0]

        changed_first = True

        while  changed_first:
            changed_first = False

            # current_column contains the current firsts for each nonterminal
            current_column = {}

            for nonterminal in nonterminals_list:
                productions_of_nonterminal = self.grammar.get_nonterminal_productions(nonterminal)

                # current_first contains the current terminals for each nonterminal
                # firstly, we get what we had in the prev first
                current_first = self.firsts_set[nonterminal]

                for production_string in productions_of_nonterminal:
                    production_symbols = production_string.split()
                    production_nonterminals = [] 
                    production_terminal = "" # we stop when we find the first terminal in the production

                    for symbol in production_symbols:
                        if symbol in self.grammar.nonterminals:
                            production_nonterminals.append(symbol)
                        else:
                            production_terminal = symbol
                            break

                    current_first.add(self.size_one_concat(production_terminal, production_nonterminals))
                
                if current_first != self.firsts_set[nonterminal]:
                    changed_first = True
                
                current_column[nonterminal] = current_first

            # the FIRST is represented by the last computed column
            self.firsts_set = current_column 
                    

           

            

    

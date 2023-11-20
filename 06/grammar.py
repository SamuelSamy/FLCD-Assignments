class Grammar:
     
    def __init__(
        self,
        file: str,
    ):

        self.file = file

        self.nonterminals = []
        self.terminals = []
        self.startingPoint = ""
        self.productionRules = {}

    
    def scan(self):
        with open(self.file, 'r') as file:
            lines = file.readlines()

            self.nonterminals = lines[0].split()
            self.terminals = lines[1].split()
            self.startingPoint = lines[2]
            for index in range(3, len(lines)):
                key, values = lines[index].split("->")
                splitValues = values.split("|")

                if key not in self.productionRules.keys():
                    self.productionRules[key] = []

                for val in splitValues:
                    self.productionRules[key] += [val.strip()]
    
    def get_nonterminal_productions(self, nonterminal):
        if nonterminal in self.productionRules :
            return self.productionRules[nonterminal]
        
            
gramm = Grammar("06/g1.txt")
gramm.scan()

print(gramm.nonterminals)
print(gramm.terminals)
print(gramm.startingPoint)
print(gramm.productionRules)

print(gramm.get_nonterminal_productions("A"))
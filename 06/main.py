from grammar import Grammar


gramm = Grammar("06/g1.txt")
gramm.scan()

print(gramm.nonterminals)
print(gramm.terminals)
print(gramm.startingPoint)
print(gramm.productionRules)

print(gramm.get_nonterminal_productions("A"))
import json

from LL1 import LL1
from grammar import Grammar

gramm = Grammar("06/g2.txt")
gramm.scan()

def print_menu():
    print('1. Display nonterminals')
    print('2. Display terminals')
    print('3. Display starting point')
    print('4. Display production rules')
    print('5. Display productions of given nonterminal')
    print('6. Check if given grammar is context free grammar (CFG)')
    print('7. LL1 parser')
    print('8. Exit')

def LL1_parser():
    ll1 = LL1(gramm)
    ll1.FIRST()
    ll1.FOLLOW()
    ll1.construct_parser_table()

    # This floods the terminal for big grammars
    # print(ll1.firsts_set)
    # print(ll1.follow_set)
    # print(json.dumps(ll1.parser_table, indent = 2))

    # print(ll1.is_ll1_grammar())

    # convert the sets to lists for json
    firsts = {}
    for key in ll1.firsts_set.keys():
        firsts[key] = list(ll1.firsts_set[key])

    follows = {}
    for key in ll1.follow_set.keys():
        follows[key] = list(ll1.follow_set[key])

    with open("06/firsts_set.json", "w") as file:
        json.dump(firsts, file, indent = 2)

    with open("06/follow_set.json", "w") as file:
        json.dump(follows, file, indent = 2)

    with open("06/parser_table.json", "w") as file:
        json.dump(ll1.parser_table, file, indent = 2)

    


def main():
    choice = 0

    while choice != 7:

        print_menu()

        choice = int(input('>> '))

        if choice == 1:
            print(gramm.nonterminals)
            continue

        if choice == 2:
            print(gramm.terminals)
            continue

        if choice == 3:
            print(gramm.startingPoint)
            continue

        if choice == 4:
            print(gramm.production_rules)
            continue

        if choice == 5:
            read_nonterminal = str(input('Enter nonterminal: '))
            if read_nonterminal != "":
                print(gramm.get_nonterminal_productions(read_nonterminal))
            continue

        if choice == 6:
            print(gramm.is_context_fre())
            continue
        
        if choice == 7:
            LL1_parser()
            continue

        if choice == 8:
            break


if __name__ == '__main__':
    main()
    
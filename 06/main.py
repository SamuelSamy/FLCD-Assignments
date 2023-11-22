from grammar import Grammar

gramm = Grammar("06/g1.txt")
gramm.scan()

def print_menu():
    print('1. Display nonterminals')
    print('2. Display terminals')
    print('3. Display starting point')
    print('4. Display production rules')
    print('5. Display productions of given nonterminal')
    print('6. Check if given grammar is context free grammar (CFG)')
    print('7. Exit')

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
            print(gramm.productionRules)
            continue

        if choice == 5:
            read_nonterminal = str(input('Enter nonterminal: '))
            if read_nonterminal != "":
                print(gramm.get_nonterminal_productions(read_nonterminal))
            continue

        if choice == 6:
            continue


if __name__ == '__main__':
    main()
    
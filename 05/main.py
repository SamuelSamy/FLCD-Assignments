from fa import FA


fa = FA('05/fas/fa-identifiers.in')


def print_menu():
    print('1. Display states')
    print('2. Display alphabet')
    print('3. Display transitions')
    print('4. Display initial state')
    print('5. Display final states')
    print('6. Check if sequence is accepted')
    print('7. Exit')


def main():
    choice = 0

    while choice != 7:

        print_menu()

        choice = int(input('>> '))

        if choice == 1:
            print(fa.get_states())
            continue

        if choice == 2:
            print(fa.get_alphabet())
            continue

        if choice == 3:
            print(fa.get_transitions())
            continue

        if choice == 4:
            print(fa.get_initial_state())
            continue

        if choice == 5:
            print(fa.get_final_states())
            continue

        if choice == 6:
            sequence = input('Sequence: ')
            print(fa.check_sequence(sequence))
            continue



if __name__ == '__main__':
    main()
    
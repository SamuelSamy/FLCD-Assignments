class FA:

    def __init__(self, file_path: str) -> None:
        
        self.__states = []
        self.__alphabet = []
        self.__transitions = {}
        self.__initial_state = None
        self.__final_states = []

        self.__read_file(file_path)


    def __read_file(self, file_path: str) -> None:

        with open(file_path, 'r') as file:
            lines = file.readlines()

        self.__states = lines[0].strip().split(' ') # The first line contains the states
        self.__alphabet = lines[1].strip().split(' ') # The second line contains the alphabet
        self.__initial_state = lines[2].strip() # The third line contains the initial state
        self.__final_states = lines[3].strip().split(' ') # The fourth line contains the final states

        # The rest of the lines contain the transitions in the form: (state0, weight, state1)
        for line in lines[4:]:
            line = line.strip()
            state0, weight, state1 = line.split(' ')

            if state0 not in self.__transitions:
                self.__transitions[state0] = []

            self.__transitions[state0].append((state1, weight))


    # Check if a sequence is accepted by the FA
    def check_sequence(self, sequence: str) -> bool:
        current_state = self.__initial_state

        for symbol in sequence:
            if symbol not in self.__alphabet:
                return False
            
            # Try to find a transition for the current state with the current symbol
            was_found = False
            for state, weight in self.__transitions[current_state]:
                if weight == symbol:
                    current_state = state
                    was_found = True
                    break
            
            # No transition was found for the current state and symbol
            if not was_found:
                return False

        # If we reached the end of the sequence and the current state is a final state, the sequence is accepted
        return current_state in self.__final_states


    def __repr__(self) -> str:
        return f'{self}'
    

    def __str__(self) -> str:
        states = ', '.join(self.__states)
        alphabet = ', '.join(self.__alphabet)
        initial_state = self.__initial_state
        final_states = ', '.join(self.__final_states)
        transitions = '\n'.join([f'{key}: {value}' for key, value in self.__transitions.items()])
        return f'States: {states}\nAlphabet: {alphabet}\nInitial state: {initial_state}\nFinal states: {final_states}\nTransitions:\n{transitions}'


    def get_states(self) -> list:
        return f'{self.__states}'
    

    def get_alphabet(self) -> list:
        return f'{self.__alphabet}'
    

    def get_transitions(self) -> dict:
        transistions = ''
        for key, value in self.__transitions.items():
            transistions += f'{key}: {value}\n'
        return transistions


    def get_initial_state(self) -> str:
        return f'{self.__initial_state}'
    

    def get_final_states(self) -> list:
        return f'{self.__final_states}'
    
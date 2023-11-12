import re

from fa import FA
from token_type import TokenType
  
from tabulate import tabulate
from exceptions import ScanningError
from symbolTable import SymbolTable
  
  
class Scanner:

    def __init__(
        self,
        file: str,
        tokens_path: str
    ):
        self.tokens = self.__read_token_file(tokens_path)

        self.file = file

        self.symbol_table = SymbolTable()
        self.pif_table = []
        self.errors = []

        self.__fa__constants = FA('05/fas/fa-consts.in')
        self.__fa__identifiers = FA('05/fas/fa-identifiers.in')


    def scan(self):
        with open(self.file, 'r') as file:
            lines = file.readlines()

        try:
            for index, line in enumerate(lines):
                self.__parse_line(index, line)
        except ScanningError as error:
            self.errors.append(f'{error}')


    def __parse_line(
        self,
        index: int,
        line: str
    ):
        if line.strip() == '':
            return
        
        line = line.strip()
        word = ''
        column = 0
        while column < len(line):
            char = line[column]

            # Check if the char is ` or '  and mark it as the start of the string
            if char in ['`', "'"]:
                starting_char = char
                word = starting_char
                column += 1
                
                while column < len(line) and line[column] != starting_char:
                    char = line[column]
                    word += char
                    column += 1
                
                # If the string is not closed, we raise an error
                if column == len(line):
                    raise ScanningError(f'Invalid string at line {index + 1}')
                
                word += line[column]
                column += 1

                # We process the string
                self.__process_token(word, index)


            # If the char is a separator, we process the word and the separator
            if self.tokens['separators'].get(char) is not None:
                if word != '':
                    self.__process_token(word, index)
                
                self.__process_separator(char)
                word = ''
                column += 1
                continue
                
            # If the char is an operator, we process the word and the operator
            if self.__is_operator(char):

                # a>2
                # If the word is not empty, it means we have a word before the operator, therefore we process it
                if word != '' and self.__is_identifier_or_constant(word):
                    self.__process_token(word, index)
                    word = ''
                # = = = = = = = = = =
                # >========
                # We have operators that are made of 2 characters, so we check if the next character is also an operator
                while column < len(line) and self.__is_operator(line[column]):
                    word += line[column]
                    column += 1

                # We process the operator
                self.__process_token(word, index)
                word = ''    
                continue
            
            # Add the char to the word
            word += char
            column += 1

        # We might have lines that do not end with a separator, so we process the last word
        if word != '':
            self.__process_token(word, index)


    def __process_token(
        self,
        word: str,
        line: int
    ):
        
        if self.__is_reserved_word(word):
            self.__process_non_identifier(word, TokenType.KEYWORD)
            return
        
        if self.__is_operator(word):
            self.__process_non_identifier(word, TokenType.OPERATOR)
            return
        

        if self.__is_identifier(word):
            self.__process_identifier(word, TokenType.IDENTIFIER)
            return
        
        if self.__is_constant(word):
            self.__process_identifier(word, TokenType.CONSTANT)
            return

        raise ScanningError(f'Invalid token: {word} at line {line + 1}')

    
    def __process_separator(
        self,
        separator: str
    ):
        if separator in [' ', '\t']:
            return

        self.__process_non_identifier(separator, TokenType.SEPARATOR)


    def __process_non_identifier(
        self,
        word: str,
        token_type: int
    ):
        if token_type == TokenType.KEYWORD:
            word = self.tokens['keywords'][word]

        if token_type == TokenType.OPERATOR:
            word = self.tokens['operators'][word]

        if token_type == TokenType.SEPARATOR:
            word = self.tokens['separators'][word]
            
        self.pif_table.append((word, -1))


    def __process_identifier(
        self,
        word: str,
        token_type: int
    ):
        self.symbol_table.insert(word)
        index = self.symbol_table.search(word)[1]   

        if token_type == TokenType.IDENTIFIER:
            word = 1

        if token_type == TokenType.CONSTANT:
            word = 2
        
        self.pif_table.append((word, index))


    def __is_reserved_word(
        self,
        word: str
    ):
        return self.tokens['keywords'].get(word) is not None
    

    def __is_operator(
        self,
        word: str
    ):
        return self.tokens['operators'].get(word) is not None
    

    def __is_identifier_or_constant(
        self,
        word: str
    ):
        return self.__is_identifier(word) or self.__is_constant(word)


    def __is_identifier(
        self,
        word: str
    ):
        return self.__fa__identifiers.check_sequence(word)
    

    def __is_constant(
        self,
        word: str
    ):
         # Check if the word is an integer constant using the FA, if it's not an integer constant, we check if it's a string / double constant using regex
        return self.__fa__constants.check_sequence(word) or re.match(r"^`.*`|'.'|'\\n'|(\+|-)?(\d)+\.(\d)+$", word) is not None
        # return re.match(r"^`.*`|'.'|'\\n'|(\+|-)?(\d)+\.(\d)+|(\+|-)?(\d)+$", word) is not None
    
    

    def get_pif(self):
        # print it using pretty table
        table = [['Token', 'Address']] + self.pif_table
        return tabulate(table, headers = 'firstrow', colalign = ('center', 'center'))
    

    def get_symbol_table(self):
        return f'{self.symbol_table}'
    
    

    def scan_message(self):
        if len(self.errors) == 0:
            return 'Lexically correct'
        
        return '\n'.join(self.errors)
    

    def __read_token_file(
        self,
        tokens_path: str
    ):
        with open(tokens_path, 'r') as file:
            tokens = file.readlines()

        self.tokens = {
            'keywords': {},
            'operators': {},
            'separators': {}
        }

        current_type = None
        index = 3
        for token in tokens:
            if token.startswith('==='):
                current_type = token[3:-4].strip().lower()
                continue
        
            self.tokens[current_type][token.replace('\n', '')] = index
            index += 1

        return self.tokens


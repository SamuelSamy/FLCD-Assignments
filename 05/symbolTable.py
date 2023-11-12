from constants import Constants
from tabulate import tabulate
    
class SymbolTable:

    def __init__(self):
        self.__current_address = 0
        self.__size = 0

        self.__max_size = Constants.InitialHashSize
        self.__load_factor = Constants.LoadFactor

        self.__table = [None] * self.__max_size


    def hash(
        self, 
        key
    ) -> int:
        if not isinstance(key, str):
            key = f'{key}'

        hash = 0
        for char in key:
            hash += ord(char)

        return hash % self.__max_size


    def insert(
        self,
        key,
        address = None
    ) -> None:
        
        # If the key is already in the table, return
        if self.search(key) is not None:
            return

        # Resize the table if the load factor is exceeded
        if self.__size / self.__max_size > self.__load_factor:
            self.__resize()

        # If no address is provided, use the __current_address
        if address is None:
            address = self.__current_address
            self.__current_address += 1

        self.__size += 1

        index = self.hash(key)

        if self.__table[index] is None:
            self.__table[index] = []

        self.__table[index].append((key, address))


    def search(
        self,
        key
    ) -> tuple | None:
        index = self.hash(key)

        if self.__table[index] is None:
            return None
        
        for entry, address in self.__table[index]:
            if entry == key:
                return (entry, address)
            
        return None


    def search_by_address(
        self,
        address
    ) -> tuple | None:
        for list in self.__table:
            if list is None:
                continue
        
            for key, addr in list:
                if addr == address:
                    return (key, addr)

        return None

    def __resize(self) -> None:
        old_table = [entry for entry in self.__table if entry is not None]

        self.__max_size *= 2
        self.__size = 0
        self.__table = [None] * self.__max_size

        for list in old_table:
            for entry in list:
                self.insert(entry[0], entry[1])


    def __repr__(self) -> str:
        return f'{self}'
    

    def __str__(self) -> str:
        to_print = [entry for entry in self.__table if entry is not None]
        table = []
        
        for list in to_print:
            for entry in list:
                table.append([entry[1], entry[0], self.hash(entry[0])])

        # Sort the table by address
        table = sorted(table, key=lambda x: x[0]) if len(table) > 0 else [['-', '-', '-']]
        table = [['Address', 'Symbol', 'Hash Index']] + table

        return tabulate(table, headers = 'firstrow', colalign=('center', 'center', 'center'))


    # Debugging function
    def debug(self) -> str:
        to_print = []
        for index, list in enumerate(self.__table):
            if list is not None:
                to_print.append((index, list))


        table = [['Index', 'Symbol (Address)']]
        for index, list in to_print:
            table.append([index, list])

        message = ''
        message += f'Current address: {self.__current_address}\n'
        message += f'Current size: {self.__max_size}\n'
        message += f'Size: {self.__size}\n'
        message += f'Load factor threshold: {self.__load_factor}\n'
        message += f'Load factor: {self.__size / self.__max_size}\n'
        message += f'Table:\n{tabulate(table, headers="firstrow", tablefmt="fancy_grid")}\n'
    
        return message
    
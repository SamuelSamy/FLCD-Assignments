from symbolTable import SymbolTable


table = SymbolTable()

table.insert('a')
table.insert('b1')
table.insert('c')

table.insert(1)
table.insert(2)
table.insert(3)

table.insert(1.1)
table.insert(2.2)
table.insert(3.3)

print(table)

print('Search by symbol:')
print(table.search('a'))
print(table.search('b2'))
print(table.search(3))
print(table.search(2.2))

print('\nSearch by address:')
print(table.search_by_address(0))
print(table.search_by_address(1))
print(table.search_by_address(2))
print(table.search_by_address(100))

print(table.debug())

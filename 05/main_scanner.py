import sys

from scanner import Scanner

if len(sys.argv) != 3:
    print("Usage: scanner.py <code_filename> <token_filename>")
    raise SystemExit(1)


file = sys.argv[1]
tokens = sys.argv[2]


scanner = Scanner(file, tokens)
scanner.scan()

result = scanner.scan_message()
pif = scanner.get_pif()
symbolTable = scanner.get_symbol_table()

actual_file_name = file.split('\\')[-1][:-3]

with open(f'05\out\{actual_file_name}-PIF.out', 'w') as file:
    file.write(pif)

with open(f'05\out\{actual_file_name}-ST.out', 'w') as file:
    file.write(symbolTable)


print(result)
with open("test.in", "w") as file:
    file.write("p s\n")

    digits = [str(i) for i in range(10)]
    letters = [chr(ord('a') + i) for i in range(26)] + [chr(ord('A') + i) for i in range(26)]

    for symbol in digits + letters:
        file.write(f"{symbol} ")

    file.write("\np\ns\n")

    for symbol in letters:
        file.write(f"p {symbol} s\n")

    for symbol in digits + letters:
        file.write(f"s {symbol} s\n")

    
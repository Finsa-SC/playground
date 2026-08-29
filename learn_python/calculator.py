operations = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b if b != 0 else 'Error',
}

op = "+"
f_num = 2
s_num = 7

result = operations.get(op, lambda a, b: "Invalid")(f_num, s_num)
print(result)
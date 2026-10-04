def camelcase(s):
    letter = 1
    for let in s:
        if let.isupper():
            letter += 1

    return letter


if __name__ == "__main__":
    s = "saveChangesInTheEditor"

    result = camelcase(s)

    print(result)
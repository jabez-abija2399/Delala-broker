def capitalize_first_letter(string):
    if string and not string[0].isupper():
        string = string[0].upper() + string[1:]
    return string

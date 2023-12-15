def encrypt(text, s):
    result = ""
    # transverse the plain text
    for i in range(len(text)):
        char = text[i]
        # Encrypt uppercase characters in plain text
        if char.isupper():
            result += chr((ord(char) + s - 65) % 26 + 65)
        # Encrypt lowercase characters in plain text
        else:
            if char.islower():
                result += chr((ord(char) + s - 97) % 26 + 97)
            else:
                result += char

    return result


if __name__ == "__main__":
    # check the above function
    text = "CEASER CIPHER Demo"
    s = 3
    encrypted = encrypt(text, s)
    print("Plain Text : " + text)
    print("Shift pattern : " + str(s))
    print("Cipher: " + encrypted)
    print("Cipher: " + encrypt(encrypted, -s))

def encrypt_show(text, key):
    print(f"Исходный текст: {text}")

    # шифрование
    bytes_text = text.encode('utf-8')
    encrypted = bytearray()

    for b in bytes_text:
        b = ((b << 2) | (b >> 6)) & 0xFF
        b = b ^ key
        encrypted.append(b)

    print(f"Зашифрованные байты: {list(encrypted)}")
    print(f"Зашифрованный текст (hex): {encrypted.hex()}")

    # расшифровываем для проверки
    decrypted = bytearray()
    for b in encrypted:
        b = b ^ key
        b = ((b >> 2) | (b << 6)) & 0xFF
        decrypted.append(b)

    print(f"Расшифрованный текст: {decrypted.decode('utf-8')}")

    return encrypted

encrypt_show("втф", 101)
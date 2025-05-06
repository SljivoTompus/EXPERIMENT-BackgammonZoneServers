def xor_decrypt(data, key=0xf8273645):
    decrypted = bytearray()
    key_bytes = key.to_bytes(4, 'little')  # Pretvori ključ u niz bajtova

    for i in range(0, len(data), 4):
        block = data[i:i+4]
        decrypted_block = bytes(b ^ key_bytes[j % 4] for j, b in enumerate(block))
        decrypted.extend(decrypted_block)

    return decrypted

# Tvoj šifrovani odgovor od servera
encrypted_response = bytes.fromhex("11 53 54 8c 15 57 44 93 20 42 16 ca 76")

# Dešifruj podatke
decrypted_data = xor_decrypt(encrypted_response)

# Ispis rezultata
print("Dešifrovani podaci (ASCII):", decrypted_data.decode(errors="ignore"))
print("Dešifrovani podaci (HEX):", decrypted_data.hex())

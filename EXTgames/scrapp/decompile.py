import struct

# Primer raw podataka
data = b"\x93i_\t\xc8'6E\xf9'\x06E\xfb'6E\xbdbd\x03\xf8'6E\xf8'6E\xf8'6E##k\x97\xc4\xe5$\x0ch#~\x915w)\xb3"

# Pokušaj da pročitaš podatke kao niz 32-bitnih brojeva
decoded = struct.unpack('I' * (len(data) // 4), data)
print("Decoded as 32-bit integers:", decoded)

# Alternativno - pročitaj kao niz bajtova u heksadecimalnom obliku
hex_representation = ' '.join(f'{byte:02x}' for byte in data)
print("Hex representation:", hex_representation)

from reedsolo import RSCodec

# Acest script calculeaza bitii pentru corectarea erorilor folosind Algoritmul Reed-Solomon

decimal_values = [64, 164, 215, 146, 5, 21, 34, 4, 54, 246, 70, 80, 236, 17, 236, 17, 236, 17, 236]
print(decimal_values) # Le afisam pentru verificare

# Numarul de octeti de corectare a erorii pentru QR Type 1 - L
n_error_bytes = 7 # 7 

# Calculam cei 7 octeti de corectare a erorii folosind Reed Solomon
# Se creaza un obiect de tip RSCodec care va codifica cele 19 valori conform algoritmului
# Aceste date sunt stocate in encoded_data (atat datele originale, cat si octetii pentru corectarea erorilor)
# La final vom extrage doar ultimii 7 octeti, cei care ne intereseaza
rs = RSCodec(n_error_bytes)
encoded_data = rs.encode(decimal_values)
error_correction_bytes = encoded_data[-n_error_bytes:]

# Convertirea valorilor obtinute in voloare zecimala si apoi in binar
decimal_error_bytes = [byte for byte in error_correction_bytes]
error_binary = ''.join(format(value, '08b') for value in decimal_error_bytes)

# Afisarea bitilor de corectare a erorii in forma binara
print(decimal_error_bytes)
print("Șirul binar de corectare a erorii:", error_binary)
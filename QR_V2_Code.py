from reedsolo import RSCodec
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Acest program genereaza un cod QR Type 2 pentru un text introdus de utilizator
# Acest tip de cod are o capacitate maxima de 44 de octeti
# Pentru acest program am folosit un nivel de corectare a erorilor LOW (adica 10 octeti)
# Inca 1 octet este folosit pentru dimensiunea mesajului
# Inca 1 octet e folosit pentru tipul de date codat (4 biti) si secventa de stop (4 biti)
# Astfel, vor ramane 32 octeti pentru a stoca date utile

# Initializam fereastra in care utilizatorul va introduce mesajul
root = tk.Tk()
root.title("QR Code Generator")
label = tk.Label(root, text= "Mesajul tau (maxim 32 caractere)")
label.pack(pady=5)
entry = tk.Entry(root)
entry.pack(pady=5)

# Functie pentru a primi textul utilizatorului
def submit_text():
    global input_variable
    input_variable = entry.get()[:32]  # Maxim 32 caractere
    if len(input_variable) > 0:
        root.destroy()  # Inchide fereastra
    else:
        messagebox.showwarning("Empty Input", "Please enter at least one character.") # Aratam avertisment

# Buton de Submit
submit_button = tk.Button(root, text= "Submit", command = submit_text)
submit_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()

# Mesajul primit este salvat in input_variable
print(f"Mesajul primit: {input_variable}")

# Mesajul care trebuie codat - folosim V2 (maxim 32 caractere)
message = input_variable # Mesajul este cel introdus de noi

# Convertim mesajul in binar si concatenam totul intr-un sir 
message_binary_string = ''.join(format(ord(char), '08b') for char in message)

# Lungimea sirului citit (cate caractere are)
message_length = len(message) 

# Convertim numarul de caractere din decimal in binar
message_binary_length = format(message_length, '08b')  # 8 bits

character_limit = 32 # pentru QR code V2

# Biti de padding pentru a ajunge la 32 bytes de date
padding_bits = "1110110000010001"  # 16 biti (2 bytes)

# Numarul de bytes de padding de care avem nevoie
needed_padding = character_limit - message_length
print("Avem nevoie de atatia bytes de padding:", needed_padding)

padding1 = padding_bits[0:8]  # Primii 8 biti din secventa de paddding

# Calculam de cati bytes de padding avem nevoie 
if needed_padding % 2 == 0:
    padding_bits_total = padding_bits * (needed_padding // 2)  # Repetam secventa de padding
else:
    padding_bits_total = padding_bits * (needed_padding // 2) + padding1  # Adaugam doar primii 8 biti

# Afisam bitii de padding necesari
print("Bitii de padding sunt:", padding_bits_total) 

data_type = "0100" # Pentru binar
stop_sequence = "0000" # Secventa de stop dupa mesaj

# Sirul final de biti obtinut prin concatenare
final_string = data_type + message_binary_length + message_binary_string + stop_sequence + padding_bits_total
print("Sirul final de date:", final_string)

# Impartim șirul în grupuri de câte 8 biți și convertim în zecimal
# Cu aceste date vom afla cei 10 bytes de eraore folosind Algoritmul Reed Solomon
decimal_values = [int(final_string[i:i+8], 2) for i in range(0, len(final_string), 8)]

# Numarul de bytes de corectare a erorii
n_error_bytes = 10 # 10 pentru QR V2 - L

# Calculam cei 10 bytes de corectare a erorii
rs = RSCodec(n_error_bytes)
encoded_data = rs.encode(decimal_values)
error_correction_bytes = encoded_data[-n_error_bytes:]

# Convertirea valorilor obtinute in voloare zecimala si apoi in binar
decimal_error_bytes = [byte for byte in error_correction_bytes]
biti_eroare_binar = ''.join(format(value, '08b') for value in decimal_error_bytes)

# Afisarea bitilor de corectare a erorii in forma binara
print("Șirul binar de corectare a erorii:", biti_eroare_binar)

# Acum concatenam totul si completam codul QR
sir_final_final = final_string + biti_eroare_binar
print("Șirul final:", sir_final_final)

# Acum trebuie sa cream o matrice de forma unui cod QR si sa o populam cu datele noastra in binar
# Initializarea matricei de 25x25 cu valori de 3
matrix = [[3] * 25 for _ in range(25)] # Pentru QR V2

# Convertirea sirului de caractere in intr-un vector de valori pentru a completa matricea
elements = sir_final_final
values = list(map(int, elements))

# Definim pattern-ul zig zag pentru a umple matricea
# Fiecare indice contine coordonatele biecarui bit din elements in cadrul matricei QR
indices = [
    (24,24), (24,23), (23,24), (23,23), (22,24), (22,23), (21,24), (21,23), (20,24), (20,23), (19,24), (19,23), (18,24), (18,23), (17,24), (17,23), (16,24), (16,23), (15,24), (15,23), (14,24), (14,23), (13,24), (13,23), (12,24), (12,23), (11,24), (11,23), (10,24), (10,23), (9,24), (9,23), 
    (9,22), (9,21), (10,22), (10,21), (11,22), (11,21), (12,22), (12,21), (13,22), (13,21), (14,22), (14,21), (15,22), (15,21), (16,22), (16,21), (17,22), (17,21), (18,22), (18,21), (19,22), (19,21), (20,22), (20,21), (21,22), (21,21), (22,22), (22,21), (23,22), (23,21), (24,22), (24,21),
    (24,20), (24,19), (23,20), (23,19), (22,20), (22,19), (21,20), (21,19), (15,20), (15,19), (14,20), (14,19), (13,20), (13,19), (12,20), (12,19), (11,20), (11,19), (10,20), (10,19), (9,20), (9,19), 
    (9,18), (9,17), (10,18), (10,17), (11,18), (11,17), (12,18), (12,17), (13,18), (13,17), (14,18), (14,17), (15,18), (15,17), (21,18), (21,17), (22,18), (22,17), (23,18), (23,17), (24,18), (24,17),
    (24,16), (24,15), (23,16), (23,15), (22,16), (22,15), (21,16), (21,15), (20,15), (19,15), (18,15), (17,15), (16,15), (15,16), (15,15), (14,16), (14,15), (13,16), (13,15), (12,16), (12,15), (11,16), (11,15), (10,16), (10,15), (9,16), (9,15), (8,16), (8,15), (7,16), (7,15), (5,16), (5,15), (4,16), (4,15), (3,16), (3,15), (2,16), (2,15), (1,16), (1,15), (0,16), (0,15),
    (0,14), (0,13), (1,14), (1,13), (2,14), (2,13), (3,14), (3,13), (4,14), (4,13), (5,14), (5,13), (7,14), (7,13), (8,14), (8,13), (9,14), (9,13), (10,14), (10,13), (11,14), (11,13), (12,14), (12,13), (13,14), (13,13), (14,14), (14,13), (15,14), (15,13), (16,14), (16,13), (17,14), (17,13), (18,14), (18,13), (19,14), (19,13), (20,14), (20,13), (21,14), (21,13), (22,14), (22,13), (23,14), (23,13), (24,14), (24,13),
    (24,12), (24,11), (23,12), (23,11), (22,12), (22,11), (21,12), (21,11), (20,12), (20,11), (19,12), (19,11), (18,12), (18,11), (17,12), (17,11), (16,12), (16,11), (15,12), (15,11), (14,12), (14,11), (13,12), (13,11), (12,12), (12,11), (11,12), (11,11), (10,12), (10,11), (9,12), (9,11), (8,12), (8,11), (7,12), (7,11), (5,12), (5,11), (4,12), (4,11), (3,12), (3,11), (2,12), (2,11), (1,12), (1,11), (0,12), (0,11),
    (0,10), (0,9), (1,10), (1,9), (2,10), (2,9), (3,10), (3,9), (4,10), (4,9), (5,10), (5,9), (7,10), (7,9), (8,10), (8,9), (9,10), (9,9), (10,10), (10,9), (11,10), (11,9), (12,10), (12,9), (13,10), (13,9), (14,10), (14,9), (15,10), (15,9), (16,10), (16,9), (17,10), (17,9), (18,10), (18,9), (19,10), (19,9), (20,10), (20,9), (21,10), (21,9), (22,10), (22,9), (23,10), (23,9), (24,10), (24,9),
    (16,8), (16,7), (15,8), (15,7), (14,8), (14,7), (13,8), (13,7), (12,8), (12,7), (11,8), (11,7), (10,8), (10,7), (9,8), (9,7), 
    (9,5), (9,4), (10,5), (10,4), (11,5), (11,4), (12,5), (12,4), (13,5), (13,4), (14,5), (14,4), (15,5), (15,4), (16,5), (16,4),
    (16,3), (16,2), (15,3), (15,2), (14,3), (14,2), (13,3), (13,2), (12,3), (12,2), (11,3), (11,2), (10,3), (10,2), (9,3), (9,2),
    (9,1), (9,0), (10,1), (10,0), (11,1), (11,0), (12,1), (12,0), (13,1) 
    ]

for index, (i, j) in enumerate(indices):
    matrix[i][j] = values[index]

print("Matricea Initiala:")
for row in matrix:
    print(row)

# Acum trebuie sa aplicam masca
# Exista 8 tipuri de masti, noi o vom alege pe cea mai usor de implementat - masca 010
# Orice masca este valida, singura diferenta este data de viteza de citire a codului QR

# Definirea coloanelor unde vrem sa inversam valorile (a 3-a coloana)
columns_to_invert = {0, 3, 9, 12, 15, 18, 21, 24}

# Initializarea unei noi matrice pentru a aplica masca
new_matrix = [[0] * 25 for _ in range(25)]

# Iteram matricea pe linii si coloane
for i in range(25):
    for j in range(25):
        # Testam daca elementele din aceasta coloana trebuie sa fie inversate
        if j in columns_to_invert:
            # Daca da, inversam valorile (0 cu 1 si 1 cu 0)
            new_matrix[i][j] = 1 if matrix[i][j] == 0 else 0
        else:
             # Altfel, doar copiem valorile din matricea initiala
            new_matrix[i][j] = matrix[i][j]

# Afisarea matricei de date dupa aplicarea mastii
print("Matricea Initiala dupa masca:")
for row in new_matrix:
    print(row)

# Acum am terminat cu datele si octetii de corectie a erorii
# Dar trebuie sa completam restul codului QR
# Incepem cu cele 2 siruri de 15 caractere (format information)
format_info = "111110110101010"*2

# Conversia sirului intr-o lista de intregi
values = list(map(int, format_info))

indices_format = [
    (8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (8,7), (8,8), (7,8), (5,8), (4,8), (3,8), (2,8), (1,8), (0,8),
    (24,8), (23,8), (22,8), (21,8), (20,8), (19,8), (18,8), (8,17), (8,18), (8,19), (8,20), (8,21), (8,22), (8,23), (8,24)
]

# Adaugare biti de format (Masca 010, Nivel Corectare L)
for index, (i, j) in enumerate(indices_format):
    new_matrix[i][j] = values[index]

# Afisare matrice acum
print("Matricea FINALA fara Patrate si Timing:")
for row in new_matrix:
    print(row)

# Tot ce ramane de facut este sa adaugam si elementele definitorii 
# (Timing and Square Patterns) = (Elementele de sincronizare)
indices_patrate = [
    (17,8), 
    (8,6), (10,6), (12,6), (14,6), (16,6),
    (6,8), (6,10), (6,12), (6,14), (6,16),
    (6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (5,6), (4,6), (3,6), (2,6), (1,6), (0,6), (0,5), (0,4), (0,3), (0,2), (0,1), (0,0), (1,0), (2,0), (3,0), (4,0), (5,0),
    (0,18), (1,18), (2,18), (3,18), (4,18), (5,18), (6,18), (6,19), (6,20), (6,21), (6,22), (6,23), (6,24), (5,24), (4,24), (3,24), (2,24), (1,24), (0,24), (0,23), (0,22), (0,21), (0,20), (0,19),
    (18,0), (18,1), (18,2), (18,3), (18,4), (18,5), (18,6), (19,6), (20,6), (21,6), (22,6), (23,6), (24,6), (24,5), (24,4), (24,3), (24,2), (24,1), (24,0), (23,0), (22,0), (21,0), (20,0), (19,0),
    (2,2), (2,3), (2,4), (3,2), (3,3), (3,4), (4,2), (4,3), (4,4),
    (2,20), (2,21), (2,22), (3,20), (3,21), (3,22), (4,20), (4,21), (4,22),
    (20,2), (20,3), (20,4), (21,2), (21,3), (21,4), (22,2), (22,3), (22,4),
    (16,16), (16,17), (16,18), (16,19), (16,20), (17,20), (18,20), (19,20), (20,20), (20,19), (20,18), (20,17), (20,16), (19,16), (18,16), (17,16), (18,18)
]

# Adaugarea bitilor impliciti (Masca 010, marime L)
# Coordonatele din indices vor primi valoarea 1, restul coordonatelor o sa ramana 3
for index, (i, j) in enumerate(indices_patrate):
    new_matrix[i][j] = 1

# Afisarea matricei finale folosita pentru a genera codul QR
print("Matricea FINALA FINALA:")
for row in new_matrix:
    print(row)

# Convertirea matricei intr-o imagine care sa afiseze un cod QR
square_size = 20 # Dimensiunea in pixeli a fiecarui patrat din codul QR
quiet_zone_size = 4 # Quiet zone va avea 4 biti in jurul codului QR

# Calcularea noilor dimensiuni ale imaginii finale cu aplicarea quiet zone-ului
height = len(new_matrix)
width = len(new_matrix[0])
new_height = height + 2 * quiet_zone_size
new_width = width + 2 * quiet_zone_size

# Crearea unei noi imagini cu un fundal alb
# Se va desena codul QR peste aceasta imagine
img = Image.new('RGB', (new_width * square_size, new_height * square_size), "white")

# Umplerea imaginii pe baza matricei
# Fiecare patrat e colorat alb sau negru in functie de valoarea din new_matrix
for y in range(height):
    for x in range(width):
        color = (0, 0, 0) if new_matrix[y][x] == 1 else (255, 255, 255)  # Black for 1, white for 0
        for i in range(square_size):
            for j in range(square_size):
                img.putpixel(((x + quiet_zone_size) * square_size + i, (y + quiet_zone_size) * square_size + j), color)

# Afisarea si salvarea imaginii finale
img.show()
img.save("QR_Code.png")

# auto-py-to-exe pentru a converti in .exe
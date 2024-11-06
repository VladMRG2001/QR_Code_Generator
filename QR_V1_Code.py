from reedsolo import RSCodec
from PIL import Image
import tkinter as tk
from tkinter import messagebox

# Acest program genereaza un cod QR Type 1 pentru un text introdus de utilizator
# Acest tip de cod are o capacitate maxima de 26 de octeti
# Pentru acest program am folosit un nivel de corectare a erorilor LOW (adica 7 octeti)
# Inca 1 octet este folosit pentru dimensiunea mesajului
# Inca 1 octet e folosit pentru tipul de date codat (4 biti) si secventa de stop (4 biti)
# Astfel, vor ramane 17 octeti pentru a stoca date utile

# Crearea fereastrei in care utilizatorul va introduce mesajul
root = tk.Tk()
root.title("QR Code Generator")
label = tk.Label(root, text= "Mesajul tau (maxim 17 caractere)")
label.pack(pady=5)
entry = tk.Entry(root)
entry.pack(pady=5)

# Definirea functiei sumbit_message care preia si proceseaza textul introdus
def submit_message():
    global input_variable
    input_variable = entry.get()[:17] # Limitam textul la 17 caractere
    if len(input_variable) > 0: # Daca avem cel putin un caracter
        root.destroy() # Inchidem fereastra
    else:
        messagebox.showwarning("Eroare", "Trebuie sa introduci cel putin un caracter.") # Aratam avertisment

# Crearea butonului de Submit pentru a trimite textul
submit_button = tk.Button(root, text= "Submit", command = submit_message)
submit_button.pack(pady=10)

root.mainloop() # Fereastra va ramane activa pana cand utilizatorul va intercationa cu ea

# Afisarea mesajului primit pentru a ne asigura ca textul este transmis corect
print(f"Mesajul primit: {input_variable}")

# Mesajul care trebuie codat - textul introdus de utilizator
message = input_variable

# Conversia mesajului in binar
# ord(char) da valoarea ASCII a caracterului
# format(..., '08b') converteste valoarea ASCII in binar pe 8 biti
# .join(...) concateneaza sirurile binare intr-un singur sir
message_binary_string = ''.join(format(ord(char), '08b') for char in message)

# Lungimea sirului citit si il convertim in binar
message_length = len(message) 
message_binary_length = format(message_length, '08b') 

# Limita de caractere pentru mesaj
character_limit = 17 # pentru QR Type 1 - L

# Biti de padding pentru a ajunge la 17 octeti de date
# Aceasta secventa se va repeta pana la ocuparea celor 17 octeti de date in caz ca mesajul este prea scurt
padding_bits = "1110110000010001"  # 16 biti (2 octeti)

# Calcularea numarului de octeti de padding de care avem nevoie
needed_padding = character_limit - message_length
print("Octeti de padding necesari:", needed_padding)

padding1 = padding_bits[0:8]  # Primii 8 biti din secventa de paddding

# Generarea efectiva a bitilor de padding necesari pentru mesajul nostru
if needed_padding % 2 == 0:
    padding_bits_total = padding_bits * (needed_padding // 2)  # Repetam secventa de padding
else:
    padding_bits_total = padding_bits * (needed_padding // 2) + padding1  # Adaugam doar primii 8 biti

# Afisarea bitilor de padding necesari
print("Bitii de padding sunt:", padding_bits_total) 

# Definirea tipului de date si secventei de stop
data_type = "0100" # Pentru ca lucram cu datele in binar
stop_sequence = "0000" # Secventa de stop dupa mesaj

# Sirul final de biti obtinut prin concatenarea tuturor sirurilor
# In total 19 octeti (1 pentru tipul de date si secventa de stop + 1 pentru lungimea mesajului + 17 pentru mesajul efectiv si bitii de padding necesari)
final_data_string = data_type + message_binary_length + message_binary_string + stop_sequence + padding_bits_total

# Afisarea sirului final de date pentru a verifica daca totul e in regula
print("Sirul final de date:", final_data_string) # Trebuie sa aiba 19 * 8 = 152 de biti

# In continuare vom avea inca 7 octeti liberi din codul nostru
# Vom afla cei 7 octeti de eroare folosind Algoritmul Reed Solomon
# Parcurgem sirul de tate si il impartim în grupuri de câte 8 biți
# Fiecare astfel de grup o sa fie convertit apoi in valoare zecimala 
# La final vom avea 19 numere intregi
decimal_values = [int(final_data_string[i:i+8], 2) for i in range(0, len(final_data_string), 8)]
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
print("Șirul binar de corectare a erorii:", error_binary)

# Acum concatenam totul si completam codul QR
final_total_string = final_data_string + error_binary
print("Șirul final:", final_total_string) # Acest sir are 26 de octeti, adica 208 biti

# Acum trebuie sa cream o matrice de forma unui cod QR si sa o populam cu datele noastra in binar
# Initializarea matricei de 21x21 cu valori de 3
matrix = [[3] * 21 for _ in range(21)] # Pentru QR V1

# Convertirea sirului de caractere in intr-un vector de valori pentru a completa matricea
elements = final_total_string
values = list(map(int, elements))

# Definim pattern-ul zig zag pentru a umple matricea
# Fiecare indice contine coordonatele biecarui bit din elements in cadrul matricei QR
indices = [
    (20,20), (20,19), (19,20), (19,19), (18,20), (18,19), (17,20), (17,19), (16,20), (16,19), (15,20), (15,19), (14,20), (14,19), (13,20), (13,19), (12,20), (12,19), (11,20), (11,19), (10,20), (10,19), (9,20), (9,19), 
    (9,18), (9,17), (10,18), (10,17), (11,18), (11,17), (12,18), (12,17), (13,18), (13,17), (14,18), (14,17), (15,18), (15,17), (16,18), (16,17), (17,18), (17,17), (18,18), (18,17), (19,18), (19,17), (20,18), (20,17),
    (20,16), (20,15), (19,16), (19,15), (18,16), (18,15), (17,16), (17,15), (16,16), (16,15), (15,16), (15,15), (14,16), (14,15), (13,16), (13,15), (12,16), (12,15), (11,16), (11,15), (10,16), (10,15), (9,16), (9,15),
    (9,14), (9,13), (10,14), (10,13), (11,14), (11,13), (12,14), (12,13), (13,14), (13,13), (14,14), (14,13), (15,14), (15,13), (16,14), (16,13), (17,14), (17,13), (18,14), (18,13), (19,14), (19,13), (20,14), (20,13),
    (20,12), (20,11), (19,12), (19,11), (18,12), (18,11), (17,12), (17,11), (16,12), (16,11), (15,12), (15,11), (14,12), (14,11), (13,12), (13,11), (12,12), (12,11), (11,12), (11,11), (10,12), (10,11), (9,12), (9,11), (8,12), (8,11), (7,12), (7,11), (5,12), (5,11), (4,12), (4,11), (3,12), (3,11), (2,12), (2,11), (1,12), (1,11), (0,12), (0,11),
    (0,10), (0,9), (1,10), (1,9), (2,10), (2,9), (3,10), (3,9), (4,10), (4,9), (5,10), (5,9), (7,10), (7,9), (8,10), (8,9), (9,10), (9,9), (10,10), (10,9), (11,10), (11,9), (12,10), (12,9), (13,10), (13,9), (14,10), (14,9), (15,10), (15,9), (16,10), (16,9), (17,10), (17,9), (18,10), (18,9), (19,10), (19,9), (20,10), (20,9),
    (12,8), (12,7), (11,8), (11,7), (10,8), (10,7), (9,8), (9,7),
    (9,5), (9,4), (10,5), (10,4), (11,5), (11,4), (12,5), (12,4),
    (12,3), (12,2), (11,3), (11,2), (10,3), (10,2), (9,3), (9,2),
    (9,1), (9,0), (10,1), (10,0), (11,1), (11,0), (12,1), (12,0)
]

# Iteram matricea pe linii (i) si coloane (j) si la fiecare set de coordonate se plaseaza valoarea din values
# Astfel, matricea se completeaza treptat cu datele QR in ordinea specificata de indices
for index, (i, j) in enumerate(indices):
    matrix[i][j] = values[index]

print("Matricea Initiala:")
for row in matrix:
    print(row)

# Acum trebuie sa aplicam masca
# Exista 8 tipuri de masti, noi o vom alege pe cea mai usor de implementat - masca 010
# Orice masca este valida, singura diferenta este data de viteza de citire a codului QR

# Definirea coloanelor unde vrem sa inversam valorile (a 3-a coloana)
columns_to_invert = {0, 3, 9, 12, 15, 18}

# Initializarea unei noi matrice pentru a aplica masca
new_matrix = [[3] * 21 for _ in range(21)]

# Iteram matricea pe linii si coloane
for i in range(21):
    for j in range(21):
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
    (20,8), (19,8), (18,8), (17,8), (16,8), (15,8), (14,8), (8,13), (8,14), (8,15), (8,16), (8,17), (8,18), (8,19), (8,20)
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
indices_patterns = [
    (13,8), 
    (8,6), (10,6), (12,6),
    (6,8), (6,10), (6,12),
    (6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (5,6), (4,6), (3,6), (2,6), (1,6), (0,6), (0,5), (0,4), (0,3), (0,2), (0,1), (0,0), (1,0), (2,0), (3,0), (4,0), (5,0),
    (0,14), (1,14), (2,14), (3,14), (4,14), (5,14), (6,14), (6,15), (6,16), (6,17), (6,18), (6,19), (6,20), (5,20), (4,20), (3,20), (2,20), (1,20), (0,20), (0,19), (0,18), (0,17), (0,16), (0,15),
    (14,0), (14,1), (14,2), (14,3), (14,4), (14,5), (14,6), (15,6), (16,6), (17,6), (18,6), (19,6), (20,6), (20,5), (20,4), (20,3), (20,2), (20,1), (20,0), (19,0), (18,0), (17,0), (16,0), (15,0),
    (2,2), (2,3), (2,4), (3,2), (3,3), (3,4), (4,2), (4,3), (4,4),
    (2,16), (2,17), (2,18), (3,16), (3,17), (3,18), (4,16), (4,17), (4,18),
    (16,2), (16,3), (16,4), (17,2), (17,3), (17,4), (18,2), (18,3), (18,4)
]

# Adaugarea bitilor impliciti (Masca 010, marime L)
# Coordonatele din indices vor primi valoarea 1, restul coordonatelor o sa ramana 3
for index, (i, j) in enumerate(indices_patterns):
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
        color = (0, 0, 0) if new_matrix[y][x] == 1 else (255, 255, 255)  # Daca valoarea e 1 o vom colora negru, altfel, daca este 0 sau 3 va fi alba
        for i in range(square_size):
            for j in range(square_size):
                img.putpixel(((x + quiet_zone_size) * square_size + i, (y + quiet_zone_size) * square_size + j), color)

# Afisarea si salvarea imaginii finale
img.show()
img.save("QR_Code.png")

# auto-py-to-exe pentru a converti in .exe (generarea executabilului)

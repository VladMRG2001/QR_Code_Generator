# QR Code Generator

Acest proiect Python generează un cod QR de la zero, folosind un mesaj introdus de utilizator. <br><br>
!!!Acest document este inca în dezvoltare!!! <br>

### Ce este un cod QR?
Un cod QR (Quick Response code) este un tip de cod de bare bidimensional (sub forma matriceala), <br>
care poate stoca informații sub forma unei grile de pătrate negre și albe. <br>
Acesta poate fi citit de dispozitive digitale precum smartphone-uri și scanerele QR. <br>

### Cum arata un cod QR?
Un cod QR este o matrice de pătrate alb-negre și vine în mai multe versiuni, fiecare cu capacități diferite de stocare. <br>
Cu cât versiunea este mai mare, cu atât codul poate stoca mai multe date: <br>
Modelul inițial (Model 1) are 21x21 patrate. <br>
A doua versiune (Model 2) are 25x25 patrate. <br>
Fiecare model superior adaugă câte 4 rânduri și coloane, până la versiunea 40, care ajunge la 177x177 pătrate. <br>

### QR Code Model 1
In acest proiect voi genera coduri QR Model 1. <br>
Mai jos se poate observa un astfel de cod QR. <br>
Acesta are o dimensiune de 21x21 pixeli. Daca il scanam vom observa mesajul "My QR Code". <br><br>
<img src="https://github.com/user-attachments/assets/22d8fd3c-d1e6-4da6-9600-1b5931b3629c" width="300"> <br>
In continuare o sa aflam cum functioneaza. <br>

### Componentele Codului QR
Orice cod QR are anumite componente definitorii: <br>
&emsp;**- Formă pătrată:** Codurile QR sunt întotdeauna de formă pătrata. <br>
&emsp;**- Pătrate de aliniere:** În colțurile codului QR există trei pătrate mari, numite pătrate de aliniere, care ajută la orientarea și citirea codului. <br>
&emsp; Acestea sunt situate în colțurile din stânga sus, dreapta sus și stânga jos. <br>
&emsp; De la versiunea 2 in sus exista un patrat mai mic si in partea dreapta jos.<br>
&emsp;**- Pătrățele de sincronizare:** Cele 3 patrate mari sunt unite prin intermediul unor linii de patratele care alterneaza intre alb si negru. <br>
&emsp;**- Quiet zone:** În jurul codului QR există o margine albă, numită „quiet zone”, care ajută la separarea codului QR de alte elemente vizuale. <br>
&emsp;**- Informație:** Informația stocată în codul QR poate include URL-uri, texte, numere de telefon, adrese de e-mail sau alte tipuri de date. <br><br>

### Elementele definitorii 
In imaginea de mai jos am separat zonele definitorii ale oricarui cod QR. <br>
Zonele inconjurate cu linie rosie sunt identice pentru orice QR. <br>
<img src="https://github.com/user-attachments/assets/fff4d635-3ca1-4765-a5f5-6a8831d2ebe9" width="300"> <br><br>
In imaginea urmatoare putem observa o alta sectiune rezervata. <br>
Zona delimitata cu albastru contine alte patratele care nu contin datele proriuzise, o sa vorbim despre ele mai tarziu. <br>
Acel patrat desenat cu verde in interiorul zonei albastre este intotdeauna negru. <br>
<img src="https://github.com/user-attachments/assets/c2db5ee8-798f-48c7-933b-1f25e4a18207" width="300"> <br><br>
Restul codului QR este destinat datelor efective. <br>
Aceste date sunt reprezentate in format binar (adica in 0 si 1). <br>
Culoarea alb reprezinta 0, iar culoarea negru reprezinta 1. <br>
Daca am sta sa numaram toate celelate patrate ramase am obtine un total de 208. Asta inseamna 208 biti cu valori de 0 sau 1. <br>
Insa datele (caracterele care sunt codate) sunt stocate sub forma de octeti, adica fiecare caracter are un octet, adica 8 biti. <br>
De aici rezulta ca tot acest spatiu ramas are 208/8 = 26 de octeti de date. <br>
Asta inseamna ca putem stoca 26 de caractere? <br>
Ei bine... nu. Este putin mai complicat. <br>

### Corectarea erorilor
Arhitectura codurilor QR impune alocarea unor biti de corectare a erorilor. <br> 
Acest lucru este prevazut pentru a putea corecta eventualele greseli, deteriorari sau parti care lipsesc din cod. <br>
Asadar, pentru orice tip de cod exista 4 niveluri de corectare de eroare in functie de ce procent de date pot fi recuperate. <br> 
- L (Low) - 7%,
- M (Medium) - 15%,
- Q (Quartile) - 25%,
- H (High) - 30%. <br>
<br>
Mai jos avem schema de alocare a octetilor pentru codul QR din cazul nostru. <br>
|  CE  | C | OC | OI | OD | T  |
|------|---|----|----|----|----|
| "01" | L |  7 |  2 | 17 | 26 | 
| "00" | M | 10 |  2 | 14 | 26 |
| "11" | Q | 13 |  2 | 11 | 26 |
| "10" | H | 17 |  2 |  7 | 26 |

<br>
unde:
CE = codul tipului de corectare in format binar
C = tipul de corectare a erorilor ales
OC = numarul de octeti rezervati pentru corectarea erorilor
OI = numarul de octeti rezervati pentru identificarea datelor (mereu 2)
OD = numarul total de octeti alocati pentru datele propriuzise stocate in codul qr
T = numarul total de octeti disponibili (26 in acest caz)
<br>
Cu cat nivelul e mai mare, cu atat e nevoie de alocarea mai multor biti pentru corectare. <br>
In exemplul meu am ales un nivel Low (L), pentru a permite cat mai multe date reale sa fie stocate.<br> 
Astfel, nu vom irosi spatiul pentru biti de eroare. <br>
Acesti biti sunt necesari in caz ca vom printa codul QR pe hartie si aceasta poate fi deteriorat. <br>
Pentru codul QR Model 1 si nivel de corectare a erorilor L, avem 7 octeti pentru corectarea erorilor. <br>
Acestia vor fi aflati prin intermediul unui algoritm special numit Reed-Solomon. <br>
Astfel, vor ramane 19 octeti (din cei 26) pentru datele propriuzise. <br>
Dintre acestia, 2 octeti (adica 16 biti) sunt rezervati pentru: <br>
Tipul de date stocate (4 biti), numarul de caractere pe care le are mesajul codat (8 biti) si secventa de stop a mesajului (4 biti). <br>
Asadar, in final, vom ramane doar cu 17 octeti. <br>
Asta inseamna ca putem coda un mesaj de maximum 17 caractere in interiorul unui cod QR Model 1. <br>

### Analogie
Pentru a face o analogie simpla sa presupunem ca vreau sa trimit un mesaj binar, unde 1 inseamna START si 0 inseamna STOP. <br>
Daca eu trimit 0, dar informatia este perturbata si ajunge 1, nici nu o sa stiu ca s-a produs o eroare. <br>
Acum hai sa aloc 2 biti (unul pentru datele propriuzise si unul pentru a semnala eroarea). Astfel, voi trimite 11 pentru START si 00 pentru STOP. <br>
Daca unul din biti se schimba din diferite probleme o sa ajunga la destinatar 01 sau 10, astfel el o sa stie ca s-a produs o eroare, dar nu isi poate da seama unde s-a produs eroarea. <br>
De data aceasta voi trimite 3 biti, 111 pentru START si 000 pentru STOP. Daca eu trimit 111 si unul din biti este alterat, destinatarul o sa primeasca o secventa de genul: 110, 101 sau 011. <br>
Acesta isi va da seama ca eroarea este acel 0 care a aparut si ca mesajul corect transmis era de fapt 111, adica START. <br>
Ceva de genul se intampla si in cazul codurilor QR, dar este mult mai complex. <br>
Daca o bucatica din cod este rupta sau deteriorata, acei biti de eroare reusesc sa "ghiceasca" mesajul initial. <br>

### Convertire zecimal in binar
Pentru a converti un numar zecimal in binar trebuie sa reusim sa il scriem sub forma unei sume de puteri ale lui 2. <br>
De exemplu numarul 10 este 2^3 + 2^1 = 8 + 2 <br>
Numarul 15 este 2^3 + 2^2 +2^1 + 2^0 = 8 + 4 + 2 + 1 <br>
Numarul 150 este 2^7 + 2^4 + 2^2 + 2^1 = 128 + 16 + 4 + 2 <br>
Acum hai sa rescriem aceasta suma incluzand toate puterile lui 2 de la 2^7 pana la 2^0. <br>
Astfel 150 = 1 * 2^7 + 0 * 2^6 + 0 * 2^5 + 1 * 2^4 + 0 * 2^3 + 1 * 2^2 + 1 * 2^1 + 0 * 2^0 <br>
Pentru a converti din zecimal in binar vom folosi coeficientii puterilor in ordinea in care apar. <br>
Adica, 150 = 1 0 0 1 0 1 1 0 in binar. <br>
Pentru a converti din binar in zecimal se procedeaza invers. <br>
10011100 = 2^7 + 2^4 + 2^3 + 2^2 = se calculeaza. <br>

## Exemplu practic - pas cu pas
Acum, pentru ca am explicat putin cum functioneaza un cod QR, hai sa construim unul de la zero. <br>
Pentru inceput, vom exclude zonele deja discutate. Asfel, vom ramane cu cei 208 biti de date. <br>
Plecam de la imaginea de mai jos. <br><br>
<img src="https://github.com/user-attachments/assets/91152acc-602d-45e8-972a-3e5b9164e1c6" width="500"> <br>
In aceasta imagine am grupat spatiul disponibil in octeti, asa cum am discutat anterior. <br>
Astfel (aproape) fiecare chenar are 8 biti, adica 8 patratele. <br>

### Completarea codului QR
Completarea codului QR incepe din coltul din dreapta jos (DF_3) pe desen si continua in forma de zig-zag pe tot restul spatiului. <br>
Ordinea de parcurgere este urmatoarea: <br>
DF_3 -> DF_2 -> DF_1 -> DF_0 -> NC_7 -> NC_6 -> ... NC_0 -> 1_7 -> 1_6 -> ...10_0 -> 11_7 -> ... -> E7_1 -> E7_0. <br>
Bun, poate ca pare putin ambiguu pana acum. <br>
Ce inseamna, DF, NC, 1, 2, E1 etc? <br><br>
Mai jos urmeaza explicatiile: <br>
- DF (Data format): acesta este un sir de 4 biti care indica codului QR ce tip de date vrem sa codam. <br>
Exista mai multe tipuri: binar, numeric, alfanumeric si kanji. Fiecare tip are o secventa speciala de biti. <br>
Mai jos putem vedea cei 4 biti in functie de tipul de date: <br>
&emsp;- Numeric : 0001 <br>
&emsp;- Alfanumeric: 0010 <br>
&emsp;- Binar: 0100 <br>
&emsp;- Kanji: 1000 <br>

&emsp;&emsp;Noi o sa lucram cu date in format binar, asa ca cei 4 biti sunt standardizati: "0100", adica DF_3 = 0, DF_2 = 1, DF_1 = 0, DF_0 = 0. <br>
- NC (Number of Characters): este o secventa de 8 biti care codifica numarul de caractere pe care urmeaza un mesaj sa il aiba. <br>
- 1 - 17: Caracterele codate pe 8 biti. <br>
- E1 - E7: Octetii pentru corectarea erorii. <br><br>

Noi o sa vrem sa cream un cod QR pentru mesajul "My QR Code", astfel, daca numaram inclusiv spatiile, ajungem la 10 caractere. <br>
Daca o sa convertim 10 in binar vom obtine 00001010. Adica octetul NC va avea valoarea: 00001010. <br>
Mai detaliat NC_7 = 0, NC_6 = 0, NC_5 = 0, NC_4 = 0, NC_3 = 1, NC_2 = 0, NC_1 = 1, NC_0 = 0. <br>
Asta inseamana ca pana acum am completat primii 4 + 8 biti in felul urmator: <br>
![image](https://github.com/user-attachments/assets/8fc32fe5-0339-41da-b057-7bc1b08ea3cc) <br>
Acum, mesajul nostru are 10 caractere. Deci o sa completam toate patratelele incepand cu 1_7 -> 1_6 -> ... -> 10_1 -> 10_0. <br>
Dar cum? Literele nu au un cod, sunt... litere. <br>
Ba da, au un cod. Toate caracterele au atribuit un numar de la 0 la 127. <br>
Aceste valori sunt prezentate in tabelul ASCII. <br>
<img src="https://github.com/user-attachments/assets/fd48a265-16df-46e0-88de-daf170eeb712" width="700">  <br>

Acolo, observam faptul ca textul nostru "My QR Code" poate fi scris ca "77 121 32 81 82 32 67 111 100 101". <br>
Atentie la diferenta intre litere mari si mici si la faptul ca inclusiv spatiul are un cod, acela este 32. <br> 
Bun, acum tot ce ramane de facut este sa convertim aceste valori in binar. Putem folosi un calculator. <br>
Astfel ajungem la valorile: <br>
01001101 01111001 00100000 01010001 01010010 00100000 01000011 01101111 01100100 01100101. <br>
Atentie ca aceste numere binare sa aiba 8 biti. <br>
Daca numarul poate fi reprezentat pe 6 biti trebuie sa includem doi biti 0 in fata lui. <br>
Pentru a pune aceste valori in codul QR trebuie sa tinem cont de puteri. <br>
De exemplu, caracterul Q este al 4-lea din sir si are valoarea in binar 01010001. <br>
Astfel, vom completa in felul urmator: <br> 
4_7 = 0, 4_6 = 1, 4_5 = 0, 4_4 = 1, 4_3 = 0, 4_2 = 0, 4_1 = 0, 4_0 = 1. <br> 
Se procedeaza la fel pentru toate caracterele din sir. <br><br>
La final se va obtine: <br>
<img src="https://github.com/user-attachments/assets/297602ba-3bee-4cd1-a470-7adcaa29ee66" width="500"> <br>
Ok, dar nu avem nici macar jumatate din cod completat. Nicio problema! <br>
Acum am terminat de codat mesajul nostru. <br>
Pentru a semnala acest lucru trebuie sa adaugam secventa de stop, adica codul "0000". <br>
Astfel 11_7, 11_6, 11_5 si 11_4 o sa fie 0. <br>
Bun, dar in aceasta imagine avem loc destinat datelor pana la 17 octeti si abia apoi observam secventa de stop de 4 biti. <br>
Da, daca aveam un mesaj de 17 caractere am fi procedat asa, dar noi avem doar 10. Asa ca trebuie sa punem secventa de stop acum. <br>
Restul spatiului nu va fi lasat gol. Se va completa cu o secventa de 16 biti de padding care pot fi impartiti in 2 octeti. <br>
Acestia sunt "11101100 00010001" si vor alterna in aceasta ordine de cate ori este nevoie pentru a completa spatiul necesar. <br>
Noi am ocupat doar 10 octeti de date, asa ca o sa avem nevoie de 7 octeti de padding. <br>
Acestia sunt: 11101100 00010001 11101100 00010001 11101100 00010001 11101100 si se vor adauga in continuare. <br><br>
Dupa completarea acestor biti de padding o sa obtinem: <br>
<img src="https://github.com/user-attachments/assets/2062e000-9251-4b43-93cd-956cd7b90c5e" width="500"> <br>
### Adaugarea octetilor de corectare a erorilor
Acum am terminat de introdus toate datele, dar observam ca inca mai avem de introdus 7 octeti numiti E1 - E7. <br>
Acestia sunt cei 7 octeti de corectare a erorii necesari pentru un cod QR Model 1 cu corectare L. <br>
Modul de aflare a acestora e destul de complicat. <br>
Recomand folosirea unui calculator online sau a unui script in python. <br>
Pentru a ii afla trebuie sa concatenam toti bitii introdusi pana acum. Adica vom avea: <br>
4 (DF) + 8 (NC) + 10 * 8 (Mesajul) + 4 (Stop) + 7 * 8 (Padding) = 152 biti. <br> 
Acestia vor fi afisati in ordinea in care sunt scrisi in cod, vor fi delimitati in grupuri de 8 biti si apoi convertiti in 19 valori zecimale. <br>
In cazul nostru avem: <br>
01000000 10100100 11010111 10010010 00000101 00010101 00100010 00000100 00110110 11110110 01000110 01010000 11101100 00010001 11101100 00010001 11101100 00010001 11101100 <br>
Daca le convertim in zecimal avem valorile: <br>
64 164 215 146 5 21 34 4 54 246 70 80 236 17 236 17 236 17 236 <br>
Acestea vor fi introduse ca date de input in Algoritmul Reed-Solomon care va genera 7 numere de corectare a erorii. <br>
Scriptul pentru acest algoritm este prezent in codul sursa. <br>
Cele 7 numere generate sunt: 183, 116, 230, 17, 230, 117, 247. <br>
Adica in binar vom avea: 10110111 01110100 11100110 00010001 11100110 01110101 11110111 <br>
Aceste valori trebuie adaugate in dreptul campurilor pentru octetii de eroare. <br><br>
La final vom obtine: <br>
<img src="https://github.com/user-attachments/assets/4cd67a11-8937-4ff1-a54a-d846895dcf6b" width="500"> <br>
Acum codul QR este aproape complet. Mai avem de completat zonele cu portocaliu. <br>
Dar pentru a face asta avem nevoie de 2 biti de eroare si 3 de masca. <br><br>
### Mascarea codului
Avem nevoie de cei 5 biti de date. <br>
Cei 2 de eroare sunt dati de nivelul de corectare ales, in cazul nostru L, care are codul standard "01". <br>
Mai jos vedem codificarea pentru nivelurile de corectare de eroare: <br>
- Nivel L: 01
- Nivel M: 00
- Nivel Q: 11
- Nivel H: 10

Dar ce este o masca si de unde luam acei biti? <br>
Oricarui cod, dupa ce este completat, i se aplica o masca pentru a facilita citirea sa de catre scannere. <br>
O masca nu este nimic altceva decat o interschimbare a bitilor cu 0 si 1 pe anumite zone in functie de un pattern. <br>
Exista 8 tipuri de masti. <br>
Mai jos le putem observa: <br>
<img src="https://github.com/user-attachments/assets/b7c48adf-8e30-4918-acc1-0f0cd5ed86c7" width="500"> <br>
Noi o sa alegem masca 3, adica masca nr 2 daca numaram de la 0. Astfel, in binar vom avea codul "010". <br>
Aceasta presupune inversarea bitilor de 1 si 0 din 3 in 3 coloane, adica pe coloanele 1, 4, 7, 10, 13, 16 si 19. <br>
Atentie, doar elementele care apartin datelor se schimba, nu si cele definitorii pentru codul QR. <br>
Acum codul arata in felul urmator: <br>
<img src="https://github.com/user-attachments/assets/7e6f475e-59e6-4198-9ea0-c2cb54597998" width="500"> <br>
Galben reprezinta alb si albastru inchis reprezinta negru. <br>
Acum putem sa completam si zona portocalie. <br>
Aceasta e formata din 2 siruri identice de cate 15 biti. <br>
Primii 5 biti sunt "01010", adica cei 2 de eroare + cei 3 de masca. <br>
Ceilalti 10 biti sunt generati in functie de acesti 5 astfel: <br>
<img src="https://github.com/user-attachments/assets/4002b5ab-f31b-45f4-98b3-0cad1a66e8ac" width="500"> <br>

Astfel, in cazul nostru, cei 10 biti sunt: 0110111000. <br>
Deci, sirul complet este: 010100110111000. <br> 
Aceasta valoare trebuie sa fie XOR cu sirul urmator: 101010000010010. <br>
In final sirul care o sa fie trecut in codul QR este: 111110110101010, asa cum se poate vedea si in tabel. <br>
Aceasta secventa o sa fie trecuta in zona portocalie in ambele locuri in ordinea indicata. <br><br>
Codul QR arata acum asa: <br>
<img src="https://github.com/user-attachments/assets/38a7e730-9115-4f2f-8431-226622012153" width="500"> <br>
Hai! Scaneaza-l! Merge? <br>
Probabil ca merge daca te chinui putin, deoarece e colorat cu verde si nuante de gri si are si linii peste el. <br>
Hai sa ii scoatem aceste detalii si sa il lasam doar alb si verde. <br><br>
<img src="https://github.com/user-attachments/assets/6027346d-553c-41a7-8f3e-777960a314b4" width="300"> <br>
<br><br>
Aici este codul QR initial pentru comparatie. <br>
<img src="https://github.com/user-attachments/assets/22d8fd3c-d1e6-4da6-9600-1b5931b3629c" width="300"> <br>
Seamana cele doua coduri? <br>
Raspusul e DA! Pentru ca sunt la fel! <br>
Asadar, acestia sunt pasii pentru a creea un cod QR de la zero. <br>
Pentru celelalte versiuni de cod QR ideea este aceeasi, doar ca e mai mult de munca. <br><br>
Concluzie: <br>
Destul de complicat, dar ideea e foarte interesanta! <br><br>
Bibliografie si referinte: <br>
https://www.thonky.com/qr-code-tutorial/ <br>
https://blog.qartis.com/decoding-small-qr-codes-by-hand/ <br>
https://dev.to/maxart2501/series/13444 <br>
https://www.youtube.com/watch?v=w5ebcowAJD8 <br>


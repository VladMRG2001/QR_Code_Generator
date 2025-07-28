# QR Code Generator

Acest proiect Python construiește **un cod QR de la zero**, pas cu pas, pe baza unui mesaj introdus de utilizator. <br><br>

## Noțiuni teoretice de bază

### Ce este un cod QR?
Un cod QR (Quick Response) este un tip de cod de bare bidimensional (format dintr-o matrice de pătrate alb-negre). <br>
Acesta poate stoca informații precum texte, link-uri, numere de telefon etc., și este ușor scanabil cu un smartphone sau un scaner QR. <br>

### Cum arata un cod QR?
Un cod QR este o matrice de pătrate alb-negre și vine în mai multe versiuni, fiecare cu capacități diferite de stocare. <br>
Cu cât versiunea este mai mare, cu atât codul poate stoca mai multe date: <br>
Modelul inițial (Model 1) are 21x21 patrate. <br>
A doua versiune (Model 2) are 25x25 patrate. <br>
Fiecare model superior adaugă câte 4 rânduri și coloane, până la versiunea 40, care ajunge la 177x177 pătrate. <br>

### QR Code Model 1
In acest proiect vom genera coduri QR Model 1. <br>
Mai jos se poate observa un astfel de cod QR. <br>
Acesta are o dimensiune de 21x21 pixeli. Daca il scanam vom observa mesajul "My QR Code". <br><br>
<img src="https://github.com/user-attachments/assets/22d8fd3c-d1e6-4da6-9600-1b5931b3629c" width="300"> <br>
Fig 1. Codul QR cu mesajul "My QR Code" <br><br>
In continuare o sa aflam cum functioneaza. <br>

### Componentele Codului QR
Orice cod QR are anumite componente definitorii: <br>
&emsp;**- Formă pătrată:** Codurile QR sunt întotdeauna de formă pătrata. <br>
&emsp;**- Pătrate de aliniere:** În colțurile codului QR există trei pătrate mari, numite pătrate de aliniere, care ajută la orientarea și citirea codului. <br>
&emsp; Acestea sunt situate în colțurile din stânga sus, dreapta sus și stânga jos. <br>
&emsp; De la versiunea 2 in sus exista un patrat mai mic si in partea dreapta jos. <br>
&emsp;**- Linii de sincronizare:** Cele 3 patrate mari sunt unite prin intermediul unor linii de patratele alternante alb-negru. <br>
&emsp;**- Quiet zone:** În jurul codului QR există o margine albă, numită „quiet zone”, care ajută la separarea codului QR de alte elemente vizuale. <br>
&emsp;**- Zona de date:** Informația stocată în codul QR poate include URL-uri, texte, numere de telefon, adrese de e-mail sau alte tipuri de date. <br><br>

### Elementele definitorii 
Mai jos am separat zonele definitorii ale oricarui cod QR. <br>
Zonele inconjurate cu linie rosie sunt patratele de aliniere si linile de sincronizare. <br>
<img src="https://github.com/user-attachments/assets/fff4d635-3ca1-4765-a5f5-6a8831d2ebe9" width="300"> <br>
Fig 2. Patratele de aliniere si sinctronizare (rosu) <br><br>
In imaginea urmatoare putem observa o alta sectiune rezervata. <br>
Zona delimitata cu albastru contine alte patratele (secventa de mascare si corectare) care nu contin datele proriuzise. O sa vorbim despre acea portiune mai tarziu. <br>
In plus, acel patratel desenat cu verde in interiorul zonei albastre este intotdeauna negru. <br>
<img src="https://github.com/user-attachments/assets/c2db5ee8-798f-48c7-933b-1f25e4a18207" width="300"> <br>
Fig 3. Secventa de mascare si corectare (albastru) <br><br>
Restul codului QR este destinat datelor efective. <br>
Aceste date sunt reprezentate in format binar (adica in 0 si 1). <br>
Culoarea alb reprezinta 0, iar culoarea negru reprezinta 1. <br>
Daca am sta sa numaram toate celelate patratele ramase am obtine un total de 208. Asta inseamna 208 biti cu valori de 0 sau 1. <br>
Insa datele (caracterele care sunt codate) sunt stocate sub forma de octeti, adica fiecare caracter are un octet, adica 8 biti. <br>
De aici rezulta ca tot acest spatiu ramas are 208/8 = 26 de octeti de date. <br>
Asta inseamna ca putem stoca 26 de caractere? <br>
Ei bine... nu. Este putin mai complicat. <br>

### Corectarea erorilor
Arhitectura codurilor QR impune alocarea unor biti de corectare a erorilor. <br> 
Acest lucru este prevazut pentru a putea corecta eventualele greseli, deteriorari sau parti care lipsesc din cod. <br>
De exemplu daca printam codul QR pe hartie si aceasta este deteriorata partial din diferite cauze. <br>
Asadar, pentru orice tip de cod exista 4 niveluri de corectare de eroare in functie de ce procent de date pot fi recuperate. <br> 
- L (Low) - 7%,
- M (Medium) - 15%,
- Q (Quartile) - 25%,
- H (High) - 30%. <br>

Cu cat nivelul e mai mare, cu atat e nevoie de alocarea mai multor biti pentru corectare. <br><br>
Mai jos avem schema de alocare a octetilor pentru codul QR din cazul nostru. <br><br>

|  CE  | C | OC | OI | OD | T  |
|------|---|----|----|----|----|
| "01" | L |  7 |  2 | 17 | 26 |
| "00" | M | 10 |  2 | 14 | 26 |
| "11" | Q | 13 |  2 | 11 | 26 |
| "10" | H | 17 |  2 |  7 | 26 |

<br>
unde: <br>
CE = codul tipului de corectare in format binar <br>
C = tipul de corectare a erorilor ales <br>
OC = numarul de octeti rezervati pentru corectarea erorilor <br>
OI = numarul de octeti rezervati pentru identificarea datelor (mereu 2) <br>
OD = numarul total de octeti alocati pentru datele propriuzise stocate in codul QR <br>
T = numarul total de octeti disponibili (26 in acest caz) <br>
<br>
In exemplul meu am ales un nivel Low (L) de corectare a  erorilor, pentru a permite cat mai multe date reale sa fie stocate. <br> 
Astfel, nu vom irosi spatiul pentru biti de eroare. <br>
Pentru codul QR Model 1 si nivel de corectare a erorilor L, avem 7 octeti pentru corectarea erorilor. <br>
Acestia vor fi aflati prin intermediul unui algoritm special numit **Reed-Solomon**. <br>
Astfel, vor ramane 19 octeti (din cei 26) pentru datele propriuzise. <br>
Dintre acestia, 2 octeti (adica 16 biti) sunt rezervati pentru identificarea datelor astfel: <br>
Tipul de date stocate (4 biti), numarul de caractere pe care le are mesajul codat (8 biti) si secventa de stop a mesajului (4 biti). <br>
Asadar, in final, vom ramane doar cu 17 octeti. <br>
Asta inseamna ca putem coda un mesaj de maximum 17 caractere in interiorul unui cod QR Model 1, asa cum se poate vedea si din tabel. <br>

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

## Exemplu de creare a unui cod QR (pas cu pas)
Acum, pentru ca am explicat putin cum functioneaza un cod QR, hai sa construim unul de la zero. <br>
Pentru inceput, vom exclude zonele deja discutate. Asfel, vom ramane cu cei 208 biti de date. <br>
Plecam de la imaginea de mai jos. <br><br>
<img src="https://github.com/user-attachments/assets/91152acc-602d-45e8-972a-3e5b9164e1c6" width="500"> <br>
Fig 4. Harta zonei de stocare in codul QR <br><br>
In aceasta imagine am grupat spatiul disponibil in octeti, asa cum am discutat anterior. <br>
Astfel (aproape) fiecare chenar are 8 biti, adica 8 patratele. <br>

### Completarea codului QR
Completarea codului QR incepe din coltul din dreapta jos (DF_3) pe desen si continua in forma de zig-zag pe tot restul spatiului. <br>
Ordinea de parcurgere este urmatoarea: <br>
**DF_3 -> DF_2 -> DF_1 -> DF_0 -> NC_7 -> NC_6 -> ... NC_0 -> 1_7 -> 1_6 -> ...10_0 -> 11_7 -> ... -> E7_1 -> E7_0**. <br>
Bun, poate ca pare putin ambiguu pana acum. <br>
Ce inseamna totusi DF, NC, 1, 2, E1 etc? <br><br>
Mai jos urmeaza explicatiile: <br>
- **DF (Data format):** acesta este un sir de 4 biti care indica codului QR ce tip de date vrem sa codam. <br>
Exista mai multe tipuri: binar, numeric, alfanumeric si kanji. Fiecare tip are o secventa speciala de biti. <br>
Mai jos putem vedea cei 4 biti in functie de tipul de date: <br>
&emsp;- Numeric : 0001 <br>
&emsp;- Alfanumeric: 0010 <br>
&emsp;- Binar: 0100 <br>
&emsp;- Kanji: 1000 <br>

&emsp;&emsp;Noi o sa lucram cu date in format binar, asa ca cei 4 biti sunt standardizati: "0100", adica **DF_3 = 0, DF_2 = 1, DF_1 = 0, DF_0 = 0**. <br>
- **NC (Number of Characters):** este o secventa de 8 biti care codifica numarul de caractere pe care urmeaza un mesaj sa il aiba. <br>
- **1 - 17:** Mesajul nostru, unde fiecare caracter este codat pe 8 biti. <br>
- **E1 - E7:** Octetii pentru corectarea erorii. <br><br>

Noi o sa vrem sa cream un cod QR pentru mesajul "**My QR Code**", astfel, daca numaram inclusiv spatiile, ajungem la **10 caractere**. <br>
Daca o sa convertim 10 in binar vom obtine 00001010. Adica octetul NC va avea valoarea: 00001010. <br>
Mai detaliat **NC_7 = 0, NC_6 = 0, NC_5 = 0, NC_4 = 0, NC_3 = 1, NC_2 = 0, NC_1 = 1, NC_0 = 0**. <br>
Asta inseamana ca pana acum am completat primii 4 + 8 biti in felul urmator: <br>
![image](https://github.com/user-attachments/assets/8fc32fe5-0339-41da-b057-7bc1b08ea3cc) <br>
Fig 5. Completarea DF (Data format) si NC (Number of Characters) <br><br>
Acum, mesajul nostru are 10 caractere. Deci o sa completam toate patratelele incepand cu 1_7 -> 1_6 -> ... -> 10_1 -> 10_0. <br>
Dar cum? Literele nu au un cod, sunt... litere. <br>
Ba da, au un cod. Toate caracterele au atribuit un numar de la 0 la 127. <br>
Aceste valori sunt prezentate in tabelul ASCII. <br>
<img src="https://github.com/user-attachments/assets/fd48a265-16df-46e0-88de-daf170eeb712" width="700"> <br>
Fig 6. Tabelul ASCII de codificare a caracterelor <br>

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
Fig 7. Codul QR completat cu datele noastre <br><br>
Ok, dar nu avem nici macar jumatate din cod completat. Nicio problema! <br>
Acum am terminat de codat mesajul nostru. <br>
Pentru a semnala acest lucru trebuie sa adaugam **secventa de stop**, adica codul **0000**. <br>
Astfel **11_7, 11_6, 11_5 si 11_4 o sa fie 0**. <br>
Bun, dar in aceasta imagine avem loc destinat datelor pana la 17 octeti si abia apoi observam secventa de stop de 4 biti. <br>
Da, daca aveam un mesaj de 17 caractere am fi procedat asa, dar noi avem doar 10. Asa ca trebuie sa punem secventa de stop acum. <br>
Restul spatiului nu va fi lasat gol. Se va completa cu o secventa de **16 biti de padding** care pot fi impartiti in 2 octeti. <br>
Acestia sunt "11101100 00010001" si vor alterna in aceasta ordine de cate ori este nevoie pentru a completa spatiul necesar. <br>
Noi am ocupat doar 10 octeti de date, asa ca o sa avem nevoie de 7 octeti de padding. <br>
Acestia sunt: 11101100 00010001 11101100 00010001 11101100 00010001 11101100 si se vor adauga in continuare. <br><br>
Dupa completarea acestor biti de padding o sa obtinem: <br>
<img src="https://github.com/user-attachments/assets/2062e000-9251-4b43-93cd-956cd7b90c5e" width="500"> <br>
Fig 8. Codul QR dupa adaugarea secventei de padding <br><br>

### Adaugarea octetilor de corectare a erorilor
Acum am terminat de introdus toate datele, dar observam ca inca mai avem de introdus 7 octeti numiti E1 - E7. <br>
Acestia sunt cei 7 octeti de corectare a erorii necesari pentru un cod QR Model 1 cu corectare L. <br>
Modul de aflare a acestora e destul de complicat. <br>
Recomand folosirea unui calculator online sau a unui script in python. <br>
Pentru a ii afla trebuie sa **concatenam toti bitii** introdusi pana acum. Adica vom avea: <br>
4 (DF) + 8 (NC) + 10 * 8 (Mesajul) + 4 (Stop) + 7 * 8 (Padding) = 152 biti. <br> 
Acestia vor fi afisati in ordinea in care sunt scrisi in cod, vor fi delimitati in grupuri de 8 biti si apoi convertiti in 19 valori zecimale. <br>
Atentie, nu mai conteaza ce tip de biti sunt, daca reprezinta DF, NC, mesajul sau Padding. <br>
Aceasta secventa de 152 de biti este scrisa exact asa cum se afla in codul QR si apoi impartita in 152/8 = 19 octeti. <br>
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
Fig 9. Codul QR dupa completarea octetilor de corectare a erorilor <br><br>
Acum codul QR este aproape complet. Mai avem de completat zonele cu portocaliu. <br>
Dar pentru a face asta avem nevoie de 2 biti de eroare si 3 de masca. <br><br>

### Mascarea codului
Avem nevoie de cei 5 biti de date. <br>
Cei 2 de eroare sunt dati de nivelul de corectare ales, in cazul nostru L, care are codul standard "01", asa cum am aratat in tabel. <br><br>
Dar ce este o masca si de unde luam acei biti? <br>
Oricarui cod, dupa ce este completat, i se aplica o masca pentru a facilita citirea sa de catre scannere. <br>
O masca nu este nimic altceva decat o interschimbare a bitilor cu 0 si 1 pe anumite zone in functie de un pattern. <br>
Exista 8 tipuri de masti. <br>
Mai jos le putem observa: <br>
<img src="https://github.com/user-attachments/assets/b7c48adf-8e30-4918-acc1-0f0cd5ed86c7" width="500"> <br>
<img src="https://github.com/user-attachments/assets/4397e0dd-71a9-41cb-90e3-ff9fd59ec98b" width="500"> <br>
Fig 10. Tipurile de mascare pentru un cod QR <br><br>
Noi o sa alegem masca 3. Aceasta este nr 2 daca numaram de la 0. Astfel, in binar vom avea codul "010". <br>
Aceasta presupune inversarea bitilor de 1 si 0 din 3 in 3 coloane, adica pe coloanele 1, 4, 7, 10, 13, 16 si 19. <br>
Atentie, doar elementele care apartin datelor se schimba, nu si cele definitorii pentru codul QR. <br><br>
Acum codul arata in felul urmator: <br>
<img src="https://github.com/user-attachments/assets/7e6f475e-59e6-4198-9ea0-c2cb54597998" width="500"> <br>
Fig 11. Transformarea bitilor pe baza mastii alese <br><br>
Asa cum am zis, doar coloanele indicate o sa fie afectate de aceasta masca, nu tot codul QR. <br>
Galben reprezinta bitii care erau negrii si acum sunt albi. <br>
Albastru inchis reprezinta bitii care erau albi si acum sunt negrii. <br>
Acum putem sa completam si zona portocalie. <br>
Aceasta e formata din 2 siruri identice de cate 15 biti. <br>
Primii 5 biti sunt "01010", adica cei 2 de eroare  (01) + cei 3 de masca (010). <br>
Ceilalti 10 biti sunt generati in functie de acesti 5 astfel: <br>
<img src="https://github.com/user-attachments/assets/4002b5ab-f31b-45f4-98b3-0cad1a66e8ac" width="500"> <br>
Fig 12. Tabelul de generare a secventei de mascare si corectare <br><br>

Astfel, in cazul nostru, cei 10 biti sunt: 0110111000. <br>
Deci, sirul complet este: 010100110111000. <br> 
Aceasta valoare trebuie sa fie **XOR** cu sirul urmator: **101010000010010**. Acest sir este mereu acelasi si este valabil pentru orice cod. <br>
In final sirul care o sa fie trecut in codul QR este: 111110110101010, asa cum se poate vedea si in tabel. <br>
Aceasta secventa o sa fie trecuta in zona portocalie in ambele locuri in ordinea indicata. <br><br>
Codul QR arata acum asa: <br>
<img src="https://github.com/user-attachments/assets/38a7e730-9115-4f2f-8431-226622012153" width="500"> <br>
Fig 13. Codul QR dupa aplicarea tuturor pasilor <br><br>
Hai! Scaneaza-l! Merge? <br>
Probabil ca merge daca te chinui putin, deoarece e colorat cu verde si nuante de gri si are si linii peste el. <br>
Hai sa ii scoatem aceste detalii si sa il lasam doar alb si verde. <br><br>
<img src="https://github.com/user-attachments/assets/b500109b-ce91-4d41-ae6e-ab880249e9bb" width="300"> <br>
Fig 14. Codul QR final (merge chiar si cu verde) <br><br>
Dupa cum se poate observa, acest cod este identic cu cel initial din fig 1. <br><br>
Asadar, acestia sunt pasii pentru a creea un cod QR de la zero. <br>
Pentru celelalte versiuni de cod QR ideea este aceeasi, doar ca e mai mult de munca. <br><br>
Concluzie: <br>
Destul de complicat, dar ideea e foarte interesanta! <br><br>

## Exemplu pentru decodificarea unui cod QR (pas cu pas)
In aceasta sectiune vom aborda in sens invers strategia. <br>
O sa folosim un cod QR de ordin 2 (25x25) si vom decodifica pas cu pas informatia din acesta. <br><br>
Dar mai intai, hai sa vedem structura unui astfel de cod QR. <br>
<img src="https://github.com/user-attachments/assets/00991431-133d-4095-aeb4-82af6a87d100" width="500"> <br>
Fig 15. Structura codului QR de tip 2 <br><br>
Daca il scanam obtinem mesajul "QR Code Model 2", dar hai sa vedem de ce este asa. <br>
Dupa cum vedem in imaginea de mai sus, avem prezente elementele definitorii clasice prezentate pana acum, doar ca mai avem inca un patrat mic de aliniere si evident ca linile de scincronizare sunt mai lungi. <br>
Acum hai sa analizam putin spatiul ramas in acest cod. <br>
Daca numaram toate patratelele libere ramase o sa ajungem la un total de 359. <br>
O proprietate interesanta a tipului 2 este ca 359 nu e divizbil cu 8, astfel nu putem folosi tot spatiul ca in cazul precedent. <br>
Asadar, ultimii 7 biti sunt implicit 0 pentru acest tip de cod QR (sunt notati cu nul pe desen). <br>
Acum ramanem cu 352 biti, care daca ii impartim la 8 ajungem la 352/8 = 44 octeti. <br>
Si in acest caz avem aceleasi 4 niveluri de corectare a erorilor, doar ca numarul de octeti ocupati este diferit. <br><br>
Mai jos observam cum se distribuie informatia in acest caz: <br>

|  CE  | C | OC | OI | OD | T  |
|------|---|----|----|----|----|
| "01" | L | 10 |  2 | 32 | 44 |
| "00" | M | 16 |  2 | 26 | 44 |
| "11" | Q | 22 |  2 | 20 | 44 |
| "10" | H | 18 |  2 | 14 | 44 |

<br>
unde: <br>
CE = codul tipului de corectare in format binar <br>
C = tipul de corectare a erorilor ales <br>
OC = numarul de octeti rezervati pentru corectarea erorilor <br>
OI = numarul de octeti rezervati pentru identificarea datelor (mereu 2) <br>
OD = numarul total de octeti alocati pentru datele propriuzise stocate in codul QR <br>
T = numarul total de octeti disponibili (44 in acest caz) <br><br>

Asadar, putem stoca mai multa informatie, dar si spatiul utilizat pentru corecatarea erorilor este mai mare. <br>

Acum, hai sa incercam sa decodificam un cod QR tip 2. Cunoastem tot ceea ce trebuie. <br>
Plecam de la acest cod gasit pe internet. <br>
<img src="https://github.com/user-attachments/assets/2c35eda6-9b95-40e3-b49e-7e308c1b7f86" width="200"> <br>
Fig 16. Codul QR care treduie decodificat <br><br>
Interesant de vazut cum acest cod poate fi citit foarte usor chiar daca nu e clar. Acest lucru se datoreaza acelor biti de corectare a erorilor. <br><br>
Bun, acum hai sa il facem mai clar ca sa putem lucra usor cu el. In plus o sa delimitam rapid elementele care nu ne intereseaza. <br>
<img src="https://github.com/user-attachments/assets/f442787c-74ed-4ecf-b17c-b918b67d9518" width="500"> <br>
Fig 17. Descompunerea codului QR <br><br>
Am reusit sa delimitam patratele de aliniere si linile de sincronizare. <br>
In plus, am scos in evidenta si secventele de mascare. <br><br>

Dupa cum vedem, avem sirul (14->0) in jurul celor 3 patrate mari tipice QR. <br>
Secventa este **101101101001011** in ambele locuri, deci e valid. Era o problema daca cele 2 secvente erau diferite. <br>
Dupa cum stim, pentru a obtine acest sir s-a aplicat XOR cu sirul de biti: 101010000010010. <br>
Hai sa aplicam din nou Xor pentru a ajunge la sirul initial. <br>
O caracteristica a portii logice Xor este ca se poate folosi si pentru criptare si pentru decodificare, intrucat este simetrica. <br>
Asadar, avem: <br>
101101101001011 Sir final <br>
101010000010010 Xor <br>
000111101011001 Sir initial <br><br>

Sirul initial are 3 parti: 2 biti pentru tipul de eroare, 3 biti pentru masca, 10 biti de corectie pentru primii 5. <br>
Eroare: 00 (M), deci nivelul de corectare a erorilor este mediu. <br>
Masca: 011 (3) deci a 4-a, pentru ca incepe de la 0 (acest tip de masca il avem in fig 10) <br>
Biti de corectie: 1101011001. Daca verificam si cu tabelul de generare a secventei de mascare din fig 12 o sa observam ca fix acesta este sirul corect pentru 00011. <br>
Deci totul e bine pana aici. Nu avem nicio problema de valididate a codului QR. <br><br>
Acum trebuie sa demascam acest cod, adica sa inversam bitii conform mastii respective, in cazul nostru 011). <br>
Dupa cum obsevam, o sa fie putin mai complicat decat in cazul precedent, intrucat acest tip de mascare e mai complex. <br>
<img src="https://github.com/user-attachments/assets/145af75e-a9e8-4205-9a33-4185e63e1c12" width="500"> <br>
Fig 18. Procesul de demascare a codului QR <br><br>
Bun, acum hai sa explic mai in detaliu. <br>
In primul rand, am scos de tot zonele inutile si le-am marcat cu rosu pentru a nu ne mai incurca. <br>
In al doilea rand, pe spatiul ramas am aplicat pattern-ul pe diagonala specific mastii noastre (a se vedea fig 10). <br>
Patratele ramase cu alb si negru nu sunt afectate de acest pattern si vor ramane asa. <br>
Patratele colorate cu albastru sunt in prezent negre si o sa fie transformate in alb in urma demascarii. <br>
Patratele colorate cu galben sunt albe in prezent si o sa fie transformate in negru in urma demascarii. <br>
Acum, ca am explicat aceste notiuni, hai sa interschimbam bitii in discutie si sa ajungem la forma initiala fara masca. <br>
<img src="https://github.com/user-attachments/assets/7153cbd8-9e8b-4652-a5c3-3f8efccf83ac" width="500"> <br>
Fig 19. Codul QR fara masca <br><br>
Dupa acest pas mai complicat am ajuns la forma initiala. <br>
Acum trebuie sa il impartim in blocuri si sa extragem mesajul. <br>
Daca ne uitam la poza de mai sus, primii 4 biti sunt 0100, deci tipul de date este bytes. <br>
Urmatorii 8 biti sunt byte-ul de nr de caractere (00001111) deci 15 caractere. Aceasta este lungimea mesajului nostru. <br>
<img src="https://github.com/user-attachments/assets/2297f2aa-41b3-4f63-943c-5bb7a5e0d90e" width="500"> <br>
Fig 20. Impartirea tipica a unui cod QR <br><br>
Atentie! Aceasta impartire este la modul general pentru cazul de corectare a erorilor M (cum avem si noi), dar in care secventa de stop nu este indicata fix dupa mesaj, ci dupa toti cei 26 de octeti disponibili pentru mesaj. <br> 
Mesajul nostru e mai mic, asa ca o sa avem secventa de stop si apoi octetii de padding pe spatiul ramas pana la octetii de corectare a erorilor. <br>
Totusi, codul nostru QR are o capacitate totala de 44 de bytes. Dintre acestia 2 sunt pentru tipul de date (4 biti la inceput, 1 byte pt nr de caractere si 4 biti la final pentru finalul de sir), deci raman 42. Am selectat eroare medie (M), deci vom avea 16 bytes destinati corectarii erorilor. Astfel ramanem cu 26 de bytes de date. <br>
Noi avem doar 15, deci codul trebuie sa aiba inca 11 bytes de padding dupa secventa de stop (0000). Vom verifica asta. <br><br>

Daca luam toti bitii in ordine obtinem: <br>
0100 00001111 01010001 01010010 00100000 01000011 01101111 01100100 01100101 00100000 01001101 01101111 01100100 01100101 01101100 00100000 00110010 0000 <br><br>

Adica avem caracterele in zecimal: 81 82 32 67 111 100 101 32 77 111 100 101 108 32 50 <br>
Adica avem caracterele: "QR Code Model 2". <br>
Ceea ce este perfect. Pana acum am parcurs totul corect. <br><br>
In continuare ar trebui sa observam cei 11 bytes de padding care alterneaza intre 11101100 si 00010001. <br>
In realitate avem: 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001 11101100. <br>
Deci e perfect pana aici. <br><br>
Acum, pentru calculul octetilor de eroare trebuie sa concatenam toti bitii de pana acum (224 in total) si sa ii impartim in 28 de bytes. <br>
Fiecare octet va fi un coeficient din polinomul pe care il vom introduce in calculatorul Reed Solomon si pentru care vom seta un polinom generator de ordin 16 pentru a gasi cei 16 octeti de eroare necesari. <br><br>
Astfel avem: <br>
01000000 11110101 00010101 00100010 00000100 00110110 11110110 01000110 01010010 00000100 11010110 11110110 01000110 01010110 11000010 00000011 00100000 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001 11101100 00010001 11101100 <br><br>
Sau in zecimal: <br>
64 245 21 34 4 54 246 70 82 4 214 246 70 86 194 3 32 236 17 236 17 236 17 236 17 236 17 236 <br><br>

Acum hai sa vedem daca si restul bitilor sunt corecti. <br>
Daca introducem acesti coeficienti in scriptul Reed-Solomon vom obtine urmatoarele 16 valori: <br>
[126, 87, 175, 63, 59, 224, 140, 188, 103, 165, 37, 115, 191, 207, 239, 207]. <br><br>
Acum hai sa verificam daca acest lucru chiar se intampla in codul nostru. <br>
In realitate avem: 01111110 01010111 10101111 00111111 00111011 11100000 10001100 10111100 01100111 10100101 00100101 01110011 10111111 11001111 11101111 11001111 <br>
In zecimal obtinem: 126 87 175 63 59 224 140 188 103 165 37 115 191 207 239 207 <br>
Este perfect, deoarece in realitate avem fix ceea ce am calculat pe baza scriptului, deci acest cod QR este valid din toate punctele de vedere. <br>
De asemenea, se observa cum ultimii 7 biti din cod sunt 0, o caracteristica tipica pentru QR V2. <br>
Astfel, decodarea este completa si detaliata pas cu pas. <br><br>
Concluzie: <br>
Acest exemplu a durat mai mult, dar aici avem demonstratia! <br><br>
### Bibliografie si referinte: <br>
[1] https://www.youtube.com/watch?v=w5ebcowAJD8 (Video explicativ despre QR - de aici a pornit acest proiect)<br>
[2] https://www.pclviewer.com/rs2/qrtopology.htm (Sumar despre structura unui cod QR) <br>
[3] https://dev.to/maxart2501/series/13444 (Explicatii pentru implementarea software)<br>
[4] https://blog.qartis.com/decoding-small-qr-codes-by-hand/ (Exemplu de decodificare manuala)<br>
[5] https://xor.pw/# (Calculator pentru XOR) <br>
[6] https://www.prepostseo.com/tool/decimal-to-ascii (Util pentru transformarea datelor - a se incerca toate functiile) <br>
[7] https://www.pclviewer.com/rs2/galois.html (Articol despre metoda de detectare si corectare a erorilor folosind algoritmul Reed-Solomon si campurile Galois)<br>

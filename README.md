# QR Code Generator

Acest proiect este implementat in Python si presupune crearea unui cod QR de la zero, pentru un mesaj introdus de utilizator. <br>

### Ce este un cod QR?
Un cod QR (Quick Response code) este un tip de cod de bare bidimensional (sub forma matriceala), care poate stoca informații sub forma unei grile de pătrate negre și albe. <br>
Acesta poate fi citit de dispozitive digitale precum smartphone-uri și scanerele QR. <br>

### Cum arata un cod QR?
Un cod QR arata ca un patrat format din diferite patratele albe si negre. Exista mai multe tipuri de coduri QR in functie de capacitatea acestora. <br>
Cu cat un cod QR este mai mare, cu atat poate stoca mai multe informatii. <br>
De exemplu, primul model de cod QR are o dimensiune de 21x21 patratele. Al doilea model are 25x25. Versiunea numarul 40 are 177x177. <br>
Modelul N are o dimensiune mai mare cu 4 linii si 4 coloane fata de Modelul N-1. <br>

### QR Code Model 1
In acest proiect voi genera coduri QR Model 1. <br>
Mai jos se poate observa un astfel de cod QR. Acesta are o dimensiune de 21x21 pixeli. Daca il scanam vom observa mesajul "My QR Code". <br>
<img src="https://github.com/user-attachments/assets/c24eeb4d-1679-4151-9eaf-784150b1e8d0" width="200"> <br>
In continuare o sa aflam cum functioneaza. <br>

### Componentele Codului QR
Orice cod QR are anumite componente definitorii. <br>
&emsp;**Formă pătrată:** Codurile QR sunt întotdeauna de formă pătrata. <br>
&emsp;**Pătrate de aliniere:** În colțurile codului QR există trei pătrate mari, numite pătrate de aliniere, care ajută la orientarea și citirea codului. <br>
&emsp;Acestea sunt situate în colțurile din stânga sus, dreapta sus și stânga jos. 
&emsp;De la versiunea 2 in sus exista un patrat mai mic si in partea dreapta jos.<br>
&emsp;**Pătrățele de sincronizare:** Cele 3 patrate mari sunt unite prin intermediul unor linii de patratele care alterneaza intre alb si negru. <br>
&emsp;**Quiet zone:** În jurul codului QR există o margine albă, numită „quiet zone”, care ajută la separarea codului QR de alte elemente vizuale. <br>
&emsp;**Informație:** Informația stocată în codul QR poate include URL-uri, texte, numere de telefon, adrese de e-mail sau alte tipuri de date. <br><br>
In imaginea de mai jos am separat zonele definitorii ale oricarui cod QR. <br>
Zonele inconjurate cu linie rosie sunt identice pentru toate codurile QR. <br>
![Codqr1](https://github.com/user-attachments/assets/212ec9ac-f552-4c37-9935-492455ae1bc4) <br>
Mai mult, in zona delimitata cu albastru avem alte patratele care nu contin datele proriuzise, o sa vorbim despre ele mai tarziu. <br>
Acel patrat desenat cu verde in interiorul zonei albastre este intotdeauna negru.<br>
![Codqr2](https://github.com/user-attachments/assets/a273b450-467e-4f83-929e-38be06cefcac) <br>
Restul codului QR este destinat datelor efective. <br>
Aceste date sunt reprezentate in format binar (adica in 0 si 1). Culoarea alb reprezinta 0, iar culoarea negru reprezinta 1. <br>
Daca am sta sa numaram toate celelate patratele ramase am obtine un total de 208. Asta inseamna 208 biti cu valori de 0 sau 1. <br>
Insa datele (caracterele care sunt codate) sunt stocate sub forma de octeti, adica fiecare caracter are un octet, adica 8 biti. <br>
De aici rezulta ca tot acest spatiu ramas are 208/8 = 26 de octeti de date. <br>
Asta inseamna ca putem stoca 26 de caractere? <br>
Ei bine... nu. Este putin mai complicat. <br>
Arhitectura codurilor QR impune alocarea unor biti de corectare a erorilor. <br> 
Acest lucru este prevazut pentru a putea corecta eventualele greseli, deteriorari sau parti lipsa care lipsesc din cod. <br>

#### Analogie
Pentru a face o analogie simpla sa presupunem ca vreau sa trimit un mesaj binar, unde 1 inseamna START si 0 inseamna STOP. <br>
Daca eu trimit 0, dar informatia este perturbata si ajunge 1, nici nu o sa stiu ca s-a produs o eroare. <br>
Acum hai sa aloc 2 biti (unul pentru datele propriuzise si unul pentru a semnala eroarea). Astfel, voi trimite 11 pentru START si 00 pentru STOP. <br>
Daca unul din biti se schimba din diferite probleme o sa ajunga la destinatar 01 sau 10, astfel el o sa stie ca s-a produs o eroare, dar nu isi poate da seama unde s-a produs eroarea. <br>
De data aceasta voi trimite 3 biti, 111 pentru START si 000 pentru STOP. Daca eu trimit 111 si unul din biti este alterat, destinatarul o sa primeasca o secventa de genul: 110, 101 sau 011. <br>
Acesta isi va da seama ca eroarea este acel 0 care a aparut si ca mesajul corect transmis era de fapt 111, adica START. <br><br>
Ceva de genul se intampla si in cazul codurilor QR, dar este mult mai complex. <br>
Asadar, pentru orice tip de cod exista 4 niveluri de corectare de eroare in functie de ce procent de date pot fi recuperate. L - 7%, M - 15%, Q - 25%, H - 30%. <br>
Cu cat nivelul e mai mare, cu atat e nevoie de alocarea mai multor biti pentru corectare. <br>
In exemplul meu am ales un nivel Low (L), pentru a permite cat mai multe date reale sa fie stocate si a nu irosi spatiul pentru biti de eroare, intrucat codul nostru QR nu poate fi deterioarat de conditiile mediului inconjurator. <br>
Pentru codul QR Model 1 si nivel de corectare a erorilor L, avem 7 octeti pentru corectarea erorilor. Acestia vor fi aflati prin intermediul unui algoritm special numit Reed-Solomon. <br>
Astfel vor ramane 19 octeti (din cei 26) pentru datele propriuzise. Dintre acestia, 2 octeti = 16 biti sunt rezervati pentru tipul de date stocate (4 biti), numarul de caractere pe care le are mesajul codat (8 biti) si secventa de stop a mesajului (4 biti). Asadar, in final, vom ramane doar cu 17 octeti. Asta inseamna ca putem coda un mesaj de maximum 17 caractere in interiorul unui cod QR Model 1.








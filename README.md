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
Daca am sta sa numaram toate celelate patratele ramase am obtine un total de 208. Asta inseaamna 208 biti cu valori de 0 sau 1. <br> 






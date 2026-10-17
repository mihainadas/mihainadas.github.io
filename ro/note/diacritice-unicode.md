---
layout: translated-post
title: "Diacritice românești: ce repară normalizarea Unicode"
lang: ro
permalink: /ro/note/diacritice-unicode/
article_kind: Notă de inginerie
description: "Literele ș și ş pot arăta aproape la fel, dar au coduri diferite. Cum reparăm textul românesc fără să modificăm greșit alte limbi."
date: 2026-10-17 13:42:57 +0300
translation_key: romanian-unicode
translation_source: _posts/2026-10-05-nfc-cannot-fix-wrong-diacritic.md
translation_source_url: /2026/10/05/nfc-cannot-fix-wrong-diacritic.html
translation_source_sha256: fae10053fb353dfc8c2f89ddec18bc80ec7bb2a45b4c4971cbfc5b72f03fc353
translation_reviewed: 2026-10-17
context_reviewed: 2026-10-17
editorial_reviewed: 2026-10-17
---

Restaurarea diacriticelor pune semnele lipsă înapoi în text, fără să schimbe celelalte caractere. Româna modernă folosește **ș** și **ț**, cu virgulă dedesubt. În programe mai vechi și în corpusuri convertite apar adesea **ş** și **ţ**, cu sedilă. Un sistem care importă date despre clienți sau evaluează text restaurat trebuie să decidă ce face cu formele vechi: le acceptă ca aceleași litere sau le semnalează pentru că ieșirea trebuia să respecte grafia modernă?

Normalizarea Unicode aduce reprezentările echivalente la o formă consecventă. Varianta NFC poate reuni o literă de bază și un semn combinator într-un singur caracter. În nota mea despre [metricile pentru restaurarea diacriticelor](/2025/09/29/romanian-diacritics-challenge.html), în engleză, am inclus și formele vechi printre pozițiile care pot necesita reparații. Dar trecerea de la sedilă la virgulă cere o regulă separată. Normalizarea nu o face în locul nostru.

Putem vedea exact unde se oprește NFC folosind patru codificări ale cuvântului `fața`. Două au virgulă și două au sedilă. NFC reduce cele patru secvențe de coduri la două șiruri Unicode, nu la unul. Le putem reuni printr-o regulă pentru română, dacă politica datelor și a evaluării permite acest lucru.

## Patru reprezentări, două grupuri

Aceeași formă vizibilă poate folosi o literă precompusă sau o literă de bază urmată de un semn combinator:

| Formă | Literal Python | Codurile relevante |
| --- | --- | --- |
| modernă, precompusă | `fața` | `U+021B` |
| modernă, descompusă | `fat\u0326a` | `U+0074 U+0326` |
| veche, precompusă | `faţa` | `U+0163` |
| veche, descompusă | `fat\u0327a` | `U+0074 U+0327` |

U+0326 este COMBINING COMMA BELOW, iar U+0327 este COMBINING CEDILLA. Diferența se vede greu în unele fonturi, dar rămâne prezentă în text.

Python oferă algoritmul de normalizare prin [`unicodedata.normalize`](https://docs.python.org/3/library/unicodedata.html). Putem verifica direct cele patru cazuri:

```python
from unicodedata import normalize


samples = {
    "modern precomposed": "fața",
    "modern decomposed": "fat\u0326a",
    "legacy precomposed": "faţa",
    "legacy decomposed": "fat\u0327a",
}

for name, value in samples.items():
    print(name, repr(normalize("NFC", value)))
```

Rezultatul păstrează două variante distincte:

```text
modern precomposed 'fața'
modern decomposed  'fața'
legacy precomposed 'faţa'
legacy decomposed  'faţa'
```

NFC face fiecare grup consecvent în interior. Nu unește grupurile. Pentru aceste caractere, NFKC produce același rezultat.

## De ce tabelul Unicode păstrează diferența

[Anexa Unicode #15](https://www.unicode.org/reports/tr15/) definește NFC ca descompunere canonică urmată de compunere canonică. NFKC pornește de la descompunerea de compatibilitate. Niciuna dintre operații nu este o regulă de asemănare vizuală sau un corector ortografic pentru o anumită limbă.

Datele decisive sunt în [UnicodeData.txt](https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt):

```text
U+021B LATIN SMALL LETTER T WITH COMMA BELOW
    -> U+0074 LATIN SMALL LETTER T
     + U+0326 COMBINING COMMA BELOW

U+0163 LATIN SMALL LETTER T WITH CEDILLA
    -> U+0074 LATIN SMALL LETTER T
     + U+0327 COMBINING CEDILLA
```

Litera de bază este aceeași. Semnele combinatoare sunt diferite. Nu există o descompunere canonică sau de compatibilitate care să transforme sedila în virgulă, deci niciuna dintre cele patru forme de normalizare nu poate inventa această transformare.

Este o limită utilă. Normalizarea are reguli stabile, independente de limbă. Dacă ar schimba un semn pentru că o anumită limbă îl tratează ca variantă istorică, ar putea strica textul unei limbi în care sedila este corectă.

## O regulă explicită pentru română

[Secțiunea despre română din standardul Unicode](https://unicode.org/versions/Unicode18.0.0/core-spec/chapter-7/) preferă U+0219 **ș** pentru româna modernă și identifică U+015F **ş** drept s-ul turcesc cu sedilă. Precizează și dificultatea practică: datele românești vechi conțin frecvent codul cu sedilă, iar prelucrarea textului românesc ar trebui să trateze cele două forme ca echivalente.

Aceasta este o operație care ține cont de limbă, aplicată după normalizarea Unicode:

```python
import unicodedata


ROMANIAN_LEGACY = str.maketrans({
    "Ş": "Ș",
    "ş": "ș",
    "Ţ": "Ț",
    "ţ": "ț",
})


def normalize_romanian(text):
    composed = unicodedata.normalize("NFC", text)
    return composed.translate(ROMANIAN_LEGACY)
```

Ordinea contează. Mai întâi, NFC transformă `s` urmat de U+0327 în caracterul precompus U+015F. Tabelul explicit poate apoi să trateze formele precompuse și descompuse folosind aceleași patru intrări. Un apel NFC final ar fi inofensiv aici, dar nu este necesar: toate înlocuirile sunt deja precompuse.

Funcția nu este o curățare Unicode universală. U+015F este valid în turcă. Aplicarea ei fără condiții într-un corpus multilingv ar înlocui o sedilă intenționată cu o virgulă românească. Limba declarată a textului, a câmpului sau a corpusului trebuie să autorizeze transformarea.

Decodarea octeților vine înaintea ambelor etape. Dacă un flux ISO-8859-2 a fost decodat cu o codificare greșită, normalizarea nu poate reconstrui interpretarea pierdută. Caracterul de înlocuire U+FFFD arată că procesul a trecut de această etapă fără informații suficiente.

## Măsurăm separat literele și formatul de ieșire

Să presupunem că referința este `fața știe`, iar sistemul produce `faţa ştie`. Trei comparații răspund la trei întrebări diferite:

```python
reference = "fața știe"
prediction = "faţa ştie"

raw_equal = prediction == reference
nfc_equal = (
    unicodedata.normalize("NFC", prediction)
    == unicodedata.normalize("NFC", reference)
)
romanian_equal = (
    normalize_romanian(prediction)
    == normalize_romanian(reference)
)
```

Rezultatele sunt `False`, `False` și `True`. Comparația brută ține cont de fiecare cod. NFC elimină diferențele accidentale de compunere, dar cere în continuare semnul corect. Transformarea pentru română măsoară literele intenționate, acceptând reprezentarea veche declarată în politică.

Pentru un test de restaurare, aș păstra două perspective:

- un scor al conținutului, după NFC și transformarea explicită a formelor vechi românești;
- un scor al respectării formatului de ieșire, după NFC, dar înaintea acelei transformări.

Primul evită să trateze o convenție veche de codificare ca eroare de limbă. Al doilea detectează un sistem care continuă să emită coduri vechi când cerința este grafia modernă. Numai scorul permisiv ar ascunde defectul de integrare. Numai scorul strict ar putea prezenta o convenție istorică a corpusului drept eșec al restaurării.

Forma brută trebuie păstrată pentru verificări și depanare. Amprentele fișierelor, jurnalele de import și eșantioanele de audit trebuie să poată arăta dacă sursa conținea semne descompuse, sedile sau text deja modern. O normalizare care suprascrie sursa la import poate face imposibilă interpretarea ulterioară a scorului.

## Testăm diferențele care contează

Un tabel mic de regresie este suficient pentru a proteja politica:

```text
modern precomposed   -> modern precomposed
modern decomposed    -> modern precomposed
legacy precomposed   -> modern precomposed, Romanian fields only
legacy decomposed    -> modern precomposed, Romanian fields only
Turkish s-cedilla    -> unchanged outside Romanian fields
invalid byte decode  -> rejected or recorded, never guessed
```

Testul trebuie să acopere **Ș/Ț**, **ș/ț**, ambele semne combinatoare și șiruri mixte. Trebuie să verifice și păstrarea caracterelor fără legătură cu diacriticele, precum și a lungimii la nivel de grafem, adică unitatea percepută de cititor ca un caracter. Modificarea punctuației, a adreselor web sau a numelor este un alt tip de eșec decât alegerea semnului românesc greșit.

Pentru un import exclusiv românesc, succesiunea este scurtă: decodare corectă, NFC, apoi transformarea declarată a caracterelor vechi. Într-un câmp multilingv, păstrăm explicită limita dintre limbi. Două litere aproape identice sunt suficiente pentru ca o regulă de curățare aparent rezonabilă să schimbe textul greșit.

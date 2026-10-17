---
layout: page
title: Cercetare
lang: ro
math: true
permalink: /ro/cercetare/
description: "TinyFabulist, modelele compacte pentru limba română și întrebările din spatele tezei lui Mihai Nadăș."
translation_key: research
translation_source: research.md
translation_source_url: /research/
translation_source_sha256: b4484e06195438280c5c62e5e66c47dbf834a887e2c390d3268106227c5f6e48
translation_reviewed: 2026-10-17
context_reviewed: 2026-10-17
editorial_reviewed: 2026-10-17
---

TinyFabulist este programul meu de cercetare despre modele de limbaj compacte și povești sintetice. Urmăresc un traseu complet: specificarea unei povești în engleză, traducerea ei în română, apoi antrenarea unui model compact care să genereze direct în română. Fiecare etapă aduce o întrebare diferită, de la respectarea instrucțiunilor până la capacitatea unui evaluator de a recunoaște o traducere bună.

Harta de mai jos separă rezultatele publicate de argumentele pe care le dezvolt în teză. Lucrările științifice descriu metodele în detaliu; notele din blog explică, pe rând, câte un experiment. Întrebarea care le leagă este una practică: ce proprietate am măsurat, de fapt, și ce concluzie putem susține pe baza ei?

## TinyFabulist

Programul are trei etape și folosește narațiuni sintetice cu proprietăți specificate în avans.

### TF1: generarea poveștilor

Specificații cu șase câmpuri sunt transformate în instrucțiuni pentru modele cu ponderi publice, de cel mult 8 miliarde de parametri. Rezultatul publicat este un corpus de trei milioane de povești în engleză, însoțite de metadate despre generare și semnale de evaluare.

- [Lucrarea TF1-EN-3M](https://arxiv.org/abs/2504.20605) descrie structura datelor, procesul de generare și resursa publicată.

### TF2: traducerea din engleză în română

TF2 transformă povești selectate din TF1 în resurse paralele engleză-română. Întrebarea este cât de mult poate un model cu ponderi publice, ajustat pentru această sarcină, să reducă diferența față de sisteme mult mai mari, la un cost mai mic de inferență. Setul de referință de 15.000 de perechi, corpusul de trei milioane de perechi și modelul publicat au roluri diferite.

- [Articolul de revistă: Building Large-Scale English–Romanian Literary Translation Resources with Open Models](https://doi.org/10.3389/frai.2026.1807431)
- [Versiunea de preprint](https://arxiv.org/abs/2509.07829v4)
- Articolul distinge corpusul complet de setul de 15.000 de perechi folosit pentru ajustare și evaluare.

### TF3: modele compacte pentru română

TF3 urmărește întregul proces: construirea unui tokenizer, care împarte textul în unitățile modelului, preantrenarea de la zero, compresia, evaluarea și generarea direct în română. Lucrarea distinge modelul de 51,65 milioane de parametri de modelul elev, comprimat, de 26,45 milioane. Formula „un model de 50 de milioane” ar ascunde această diferență.

- [Lucrarea TF3-RO-50M](https://arxiv.org/abs/2601.10410)

## Evaluare și prelucrarea limbii române

Două direcții susțin acest traseu:

- o analiză a literaturii despre generarea de text și cod sintetic ([arXiv](https://arxiv.org/abs/2503.14023));
- restaurarea diacriticelor românești, inclusiv studiul prezentat la InnoComp 2025 și publicat în Springer CCIS 2794 ([articol](https://doi.org/10.1007/978-3-032-12481-4_4), [preprint](https://arxiv.org/abs/2511.13182)).

Grupul de evaluatori cu ponderi publice are, deocamdată, o utilizare măsurată. În protocolul fix TF1, clasamentul sistemelor a urmărit clasamentul dat de o4-mini, cu Spearman \\(\rho=0.93\\) și Kendall \\(\tau=0.78\\). Acordul asupra exemplelor individuale a rămas slab, iar arbitrajul uman planificat nu a fost încă realizat. Folosesc, așadar, grupul pentru comparații agregate în protocolul testat, nu pentru a înlocui evaluarea umană sau pentru a filtra automat texte individuale.

## Din teza în lucru

Teza, aflată în etapa de propunere, leagă cele trei sisteme printr-o întrebare despre măsurare: când numim un proces „controlat”, ce proprietăți ale rezultatului am testat efectiv? Seria de mai jos dezvoltă analizele care nu sunt deja acoperite de prezentarea resurselor publicate.

Aceste note sunt disponibile în engleză:

{% assign thesis_posts = site.posts | where: "series", "controlled-synthetic-narratives" | sort: "series_order" %}
{% for post in thesis_posts %}
- [{{ post.title }}]({{ post.url | relative_url }}) (EN)
{% endfor %}

## Reproductibilitate

Lucrările, datele, instrucțiunile pentru modele și codul public fac rezultatele mai ușor de verificat. Nu garantează însă un comportament identic al hardware-ului, al serviciilor externe sau al execuțiilor cu aleatoriu. Fiecare notă tehnică precizează ce a fost testat și unde se oprește acea verificare.

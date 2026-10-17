---
layout: translated-post
title: "Cum verifici cercetarea unui agent AI"
lang: ro
permalink: /ro/note/cercetare-cu-dovezi/
article_kind: Cercetare aplicată
description: "Cum organizăm căutarea, citirea și verificarea surselor când un agent AI pregătește o decizie de afaceri."
date: 2026-10-17 13:42:57 +0300
translation_key: evidence-budget
translation_source: _posts/2026-10-17-deep-research-needs-evidence-budget.md
translation_source_url: /2026/10/17/deep-research-needs-evidence-budget.html
translation_source_sha256: 5ee1e3b57b262c0d575d98dcf938612b8aba09d61fc52deaf84360993801ffba
translation_reviewed: 2026-10-17
context_reviewed: 2026-10-17
editorial_reviewed: 2026-10-17
---

Un agent de cercetare aprofundată transformă o întrebare într-un raport: caută, citește surse, păstrează dovezi și decide când se oprește. Să presupunem că îl folosim pentru a compara trei furnizori de software într-un proces supus unor cerințe de reglementare. Raportul poate fi fluent și bine organizat. Înainte de alegerea furnizorului, cineva tot trebuie să verifice de unde provine fiecare afirmație importantă.

Aceasta este problema pe care vreau să o rezolve procesul de cercetare: să putem urmări drumul de la sursă la decizie. Un agent util găsește materialul relevant, îl citește, rezolvă contradicțiile și dublurile și arată ce rămâne incert. Mai multe căutări sau un raport mai lung nu demonstrează că a făcut toate aceste lucruri.

Lucrările de mai jos studiază părți diferite ale procesului. Pornind de la ele, propun un mod de organizare: bugete distincte pentru descoperire, inspecție, verificare și sinteză. Este o propunere de testat într-un flux de lucru al unei organizații, nu o afirmație că testele din lucrările citate au validat deja analiza furnizorilor.

## Începem cu o decizie pe care cineva trebuie să o poată justifica

Comparația furnizorilor are nevoie de o dată a deciziei, de o ierarhie a surselor acceptate și de o regulă de oprire. Altfel, agentul nu are un criteriu sigur pentru a distinge o investigație încheiată de o ciornă bine prezentată.

Bugetul de descoperire poate cere documentația oficială a produselor, materiale despre securitate și confidențialitate, condiții contractuale, incidente publice și îndrumările autorității relevante. Bugetul de inspecție cere deschiderea documentelor, verificarea datelor lor și indicarea pasajelor care susțin afirmațiile. Cel de verificare alocă o a doua sursă sau un al doilea evaluator pentru certificări, localizarea datelor, istoricul incidentelor și răspunderea contractuală. Sinteza produce atât comparația, cât și un registru al excepțiilor.

Rezultatul ar trebui să păstreze cel puțin:

1. întrebarea exactă și data deciziei;
2. planul de căutare și sursele consultate;
3. un registru care leagă afirmațiile de pasajele inspectate;
4. contradicțiile și informațiile încă lipsă;
5. regulile de includere, excludere și oprire;
6. recomandarea, cu ipotezele separate de constatări.

Beneficiul urmărit este o verificare umană mai rapidă. Evaluatorul se poate concentra pe dovezile slabe și pe deciziile de interpretare, fără să reconstruiască întreaga sesiune de navigare. Același registru îi oferă următoarei rulări un punct de pornire pentru a verifica sursele sau faptele care s-au schimbat.

## A găsi o pagină nu înseamnă a o citi

[Search-R1](https://arxiv.org/abs/2503.09516) și [ReSearch](https://arxiv.org/abs/2503.19470) antrenează modele de limbaj să alterneze raționamentul cu apeluri de căutare. Nu este doar conectarea unui motor de căutare la model. Sistemul învață când o lipsă de informație justifică o interogare și cum ar trebui materialul găsit să schimbe pasul următor.

Un rezultat de căutare nu este însă încă o dovadă. Lista conține poziții, titluri, adrese și fragmente selectate de un alt sistem. Poate omite o condiție importantă, trimite la o pagină inaccesibilă sau alătura texte care nu erau vecine în document. Dacă tratăm fragmentul drept sursă, procesul devine rapid, dar fragil.

[OpenResearcher](https://arxiv.org/abs/2603.20278) separă explicit trei operații: `search`, `open` și `find`. Mediul său offline folosește un corpus fix de 15 milioane de documente. Autorii raportează peste 97.000 de trasee sintetizate, adică succesiuni de pași de cercetare, inclusiv trasee cu peste 100 de apeluri de instrumente. Experimentele care izolează componente ale sistemului arată că găsirea unui document relevant nu garantează răspunsul corect. Deschiderea și inspecția lui au îmbunătățit performanța.

Distincția reapare în alte implementări. [SFR-DeepResearch](https://arxiv.org/abs/2509.06283) oferă unui singur agent căutare web, citirea paginilor și Python. [DeepResearcher](https://arxiv.org/abs/2504.03160) antrenează comportamentul în interacțiuni cu webul real. [Tongyi DeepResearch](https://arxiv.org/abs/2510.24701) folosește un raport actualizat drept memorie comprimată. A găsi, a citi, a calcula și a păstra informația sunt acțiuni distincte, cu erori distincte.

## Patru bugete pe care le putem inspecta

Bugetele sunt limite legate între ele, nu neapărat sume de bani.

| Buget | Ce controlează | Exemplu de criteriu de încheiere |
| --- | --- | --- |
| Descoperire | Interogări, pagini de rezultate, depozite și baze de date cercetate | Fiecare piață, jurisdicție și sinonim necesar are un traseu de căutare documentat. |
| Inspecție | Surse complete deschise și pasaje relevante citite | Fiecare afirmație importantă citează o sursă inspectată, nu un fragment din căutare. |
| Verificare | Confirmări independente, căutarea contradicțiilor, calcule și identificarea entităților | Afirmațiile cu impact mare au sprijin independent sau o contradicție consemnată. |
| Sinteză | Spațiu pentru compararea dovezilor, incertitudini și redactare | Raportul separă constatările, ipotezele, întrebările deschise și recomandările. |

Limitele nu trebuie să fie numere fixe. Pentru o comparație de produse cu risc mic poate fi suficientă o sursă primară solidă pentru fiecare specificație. Interpretarea unei cerințe de reglementare poate necesita textul regulii, data aplicării, autoritatea responsabilă, modificările ulterioare și îndrumările pentru jurisdicția respectivă. Resursele alocate trebuie să țină cont de consecința unei greșeli.

Separarea face concretă și discuția despre cost. Încă zece căutări adaugă acoperire? Citirea unei surse suplimentare rezolvă o incertitudine importantă? Sinteza consumă resurse fără să adauge dovezi? Numărarea tuturor apelurilor la un loc ascunde aceste diferențe.

## Regula de oprire spune ce considerăm complet

[DeepSearchQA](https://arxiv.org/abs/2601.20975) cuprinde 900 de sarcini cu mai mulți pași, din 17 domenii. Evaluează liste complete de răspunsuri, nu doar găsirea unui singur fapt. Autorii observă atât oprirea prea devreme, care pierde rezultate relevante, cât și includerea unor elemente slab susținute pentru a lărgi artificial acoperirea.

Într-o analiză de piață putem rata un furnizor mic care îndeplinește o cerință esențială. Putem și să facem lista inutilizabilă dacă includem orice companie vag înrudită. Regula bună de oprire depinde de definiția listei. Înainte de căutare, responsabilul deciziei ar trebui să precizeze:

- criteriile de includere și excludere;
- dimensiunile pentru care contează completitudinea;
- dovezile acceptabile pentru fiecare element;
- tratarea dublurilor și a filialelor;
- incertitudinea care poate rămâne la termenul-limită.

Agentul se poate opri când criteriul declarat este îndeplinit. Dacă bugetul se termină înainte, rezultatul trebuie să spună ce ramură a rămas incompletă.

## Evaluarea urmează decizia

[DRACO](https://arxiv.org/abs/2602.11685) construiește 100 de sarcini complexe în 10 domenii, cu surse din 40 de țări. Grilele sale specifice fiecărei sarcini separă acuratețea factuală, amploarea și profunzimea, prezentarea și calitatea citărilor. Un singur scor ar ascunde diferența dintre un text clar fără suficiente dovezi și unul cu multe citări care interpretează greșit sursele.

În timpul antrenării, [DR Tulu](https://arxiv.org/abs/2511.19399) adaptează criteriile de evaluare la dovezile găsite și la diferențele dintre răspunsuri. Criteriile pot astfel continua să distingă rezultatele pe măsură ce modelul se schimbă. [Rethinking the Design of Reinforcement Learning-Based Deep Research Agents](https://arxiv.org/abs/2510.15862), lucrarea din spatele PokeeResearch, testează separat recompensa, algoritmul de învățare prin recompensă, selecția datelor și toleranța la erori de execuție. Autorii raportează îmbunătățiri prin feedback de la modele de limbaj, metoda on-policy RLOO, filtrarea întrebărilor slabe și repararea acțiunilor formulate greșit în timpul testării.

Aceste rezultate nu se transferă automat în achiziții sau conformitate. Lecția ține de structura testului: păstrăm separat validitatea surselor, sprijinul factual, acoperirea cerută, tratarea contradicțiilor, plasarea citărilor și prezentarea. Dacă le comprimăm într-un singur scor, un câștig de formatare poate ascunde o pierdere de dovezi.

## O buclă mică, în care erorile se văd

[OpenSeeker](https://arxiv.org/abs/2603.15594) generează întrebări dificile parcurgând legăturile web și mascând entitățile care ar permite scurtături prin cuvinte-cheie. Comprimă și observațiile mai vechi, păstrând în detaliu informațiile recente. Pentru un sistem de afaceri, ideile utile sunt să testăm navigarea reală prin dovezi și să păstrăm proveniența atunci când comprimăm memoria.

O primă implementare nu are nevoie de un model de vârf sau de o ierarhie complicată de agenți. Are nevoie de o buclă pe care o putem urmări:

```text
plan -> search -> open -> extract -> record -> check coverage
                         ^                    |
                         +---- revise --------+
```

Fiecare afirmație extrasă primește o adresă a sursei, momentul consultării, pasajul sau dovada structurată și o stare de încredere ori de conflict. Rezultatele care nu au fost deschise rămân piste de investigat. Verificarea acoperirii alege ramura încă nerezolvată sau oprește procesul cu un motiv. Sinteza finală scrie numai din registrul de dovezi.

Implementarea poate folosi un model, mai multe modele sau instrumente deterministe. [SFR-DeepResearch](https://arxiv.org/abs/2509.06283) arată că interfața de control poate rămâne mică. Mai multe roluri nu repară un standard de dovezi nedefinit.

La verificarea raportului, pornește de la o afirmație importantă și încearcă să ajungi la sursa inspectată. Uită-te apoi la întrebările nerezolvate și la motivul opririi. Dacă traseul lipsește, raportul nu este pregătit să susțină decizia, oricât de convingător ar suna.

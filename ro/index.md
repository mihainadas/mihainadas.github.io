---
layout: page
title: În română
lang: ro
permalink: /ro/
wide: true
description: "Cercetarea lui Mihai Nadăș, explicată în română: modele de limbaj, calitatea textului și decizii bazate pe dovezi."
---

<div class="romanian-intro" markdown="1">
Scriu despre sisteme pe care le putem testa: modele de limbaj, prelucrarea textului și instrumente care ne ajută să luăm decizii. Mă interesează ce funcționează, în ce condiții și cum ne dăm seama când un rezultat nu se transferă în practică.

Aici găsești ediții în română ale unor texte din blog. Păstrez exemplele și trimiterile la surse, dar explic termenii înainte să îi folosesc. [Arhiva în engleză](/archive/) cuprinde toate notele de cercetare și inginerie.
</div>

<section class="romanian-research" aria-labelledby="research-ro-heading">
  <p class="eyebrow">Un punct de pornire</p>
  <h2 id="research-ro-heading">De la povești sintetice la modele pentru limba română</h2>
  <p>TinyFabulist leagă generarea de povești, traducerea și antrenarea unor modele compacte. Pagina de cercetare explică etapele, indică lucrările publice și separă rezultatele publicate de analizele din teza în lucru.</p>
  <a class="text-link" href="{{ '/ro/cercetare/' | relative_url }}">Descoperă cercetarea →</a>
</section>

<section aria-labelledby="note">
  <h2 id="note">Note în română</h2>
  <div class="post-grid">
    {% assign romanian_notes = site.pages | where: 'layout', 'translated-post' | sort: 'title' %}
    {% for note in romanian_notes %}
    <article class="post-card">
      <p class="post-meta">{{ note.article_kind }}</p>
      <h3><a href="{{ note.url | relative_url }}">{{ note.title }}</a></h3>
      <p>{{ note.description }}</p>
    </article>
    {% endfor %}
  </div>
</section>

Nu toate textele au încă o ediție în română. Când există ambele versiuni, legătura de schimbare a limbii te duce direct la același articol. În celelalte cazuri, te duce la pagina de pornire a limbii alese. Nu folosesc redirecționări automate după limba browserului.

# AGENTS.md — Mono-Repo für Lernplattform-Kurse

Dieses Dokument ist die **kanonische Quelle der Wahrheit** für jede KI, die in diesem Repo arbeitet. Wenn andere Dokumente widersprechen, gilt AGENTS.md.

Dieses Repository ist die **Mono-Repo-Schablone** für neue Lernplattform-Kurse. Wer einen neuen Kurs anlegt, klont es via `gh repo create kirenz/<slug> --template kirenz/lernplattform-templates --clone` und ersetzt die Schablonen-Inhalte durch konkrete Inhalte. Vollständig ausgearbeitetes Beispiel-Repo: [`kirenz/n8n-grundlagen`](https://github.com/kirenz/n8n-grundlagen).

---

## Repo-Struktur — Mono-Repo

Dieses Repo enthält **drei eng verbundene Welten** in einem Repository:

```
.
├── _quarto.yml              # Buch-Build-Konfiguration (project: book)
├── AGENTS.md                # Dieses Regelwerk — Buch-Stil
├── README.md                # Mono-Repo-Beschreibung
│
│  # — Buch-Welt (kanonische Quelle) —
├── index.qmd                # Buch-Willkommen
├── introduction.qmd         # Buch-Einführung
├── <modul-slug>/            # Pro Modul ein Verzeichnis mit Lessons
│   └── *.qmd
│
│  # — Slide-Welt (aus Buch generiert + feinjustiert) —
├── slides/
│   ├── AGENTS.md            # Slide-Stilregeln (gilt für slides/ ausschließlich)
│   ├── modul-XX/<lesson>.qmd
│   └── …
│
│  # — Kursbegleitende Ressourcen —
├── infra/                   # Optional — Setup für Demo-Instanzen, z. B. Hetzner-Server
├── workflows/               # Optional — kursbegleitende Demo-Files (JSON, Code, Datasets)
└── scripts/                 # Buch → Slides Generator
```

**Welche AGENTS.md gilt wann:**

- Beim Arbeiten an Buch-Kapiteln (`*.qmd` im Repo-Root oder in den Modul-Verzeichnissen außer `slides/`): **diese Datei** gilt — Wir-Form, Callouts, Buch-Disziplin.
- Beim Arbeiten an Slide-Decks (`slides/**/*.qmd`): **`slides/AGENTS.md`** gilt — indirekte Ansprache, Pattern-Bibliothek, Stage-Choreographie.

**Wichtigster Stilwechsel beim Übertrag:** Buch-Prosa nutzt **Wir-Form** („Wir bauen…"), Slide-Text und Speaker-Notes nutzen **indirekte Ansprache** („Drei Knoten reichen…"). Wer Inhalte vom Buch in ein Slide-Deck überträgt, schaltet bewusst um.

**Buch-First-Workflow:** Pro Lesson **erst** Buch-Kapitel schreiben, **dann** Slide-Deck via `scripts/generate_slides.py` daraus erzeugen und feinjustieren. Keine Slide-Inhalte ohne entsprechendes Buch-Kapitel als Quelle.

---

## TL;DR — KI-Schnellstart

Wenn ein Curriculum übergeben wird, in dieser Reihenfolge arbeiten:

1. **Lesen**: Diese Datei komplett. Plus `_quarto.yml` (Kapitel-Reihenfolge).
2. **Lesson-Granularität festlegen**: 2–4 Lessons pro Modul, 5–15 Min Lernzeit pro Lesson, **eine Lesson = ein `.qmd`-Kapitel = ein späteres Slide-Deck**.
3. **Pro Modul ein Verzeichnis** mit `index.qmd` (Modul-Übersicht in Wir-Form) + Lesson-Kapitel.
4. **Pro Lesson ein Kapitel** mit H1-Titel, Wir-Form-Prosa, Callouts für Vertiefungen, Tabellen für Vergleiche, Code-Blöcken mit Erklärung im Folge-Callout.
5. **Erstentwurf-Marker** am Anfang jedes nicht voll ausgearbeiteten Kapitels: `::: {.callout-note title="Status — Erstentwurf"}` plus am Ende einen Block `## Was als Nächstes ausgebaut werden muss` mit konkreten Vertiefungs-TODOs.
6. **Rendern**: `quarto render`. Output in `_book/`. Errors beheben, bevor an die Generator-Pipeline weitergereicht wird.
7. **Folien generieren** (separate Aktion): `uv run python scripts/generate_slides.py` erzeugt aus jedem Buch-Kapitel ein Reveal.js-Deck.

Output an den Nutzer: nur die Buch-Kapitel. Keine Meta-Erklärungen.

---

## Verbindliche Disziplin-Regeln (gelten überall)

### 1. Sprach-Stil: Wir-Form

**In sichtbarem Buch-Text** wird durchgängig die **Wir-Form** verwendet. Das ist der bewusste Unterschied zu den Folien-Decks im Slide-Repo, wo indirekte Ansprache gilt. Im Buch wirkt die Wir-Form persönlicher und führt die Leserinnen und Leser durch die Schritte.

| Verwenden | Vermeiden |
|---|---|
| „Wir öffnen den Editor und ziehen den Trigger-Knoten…" | „Du öffnest den Editor…" / „Sie öffnen den Editor…" |
| „Wir können den Workflow als JSON exportieren." | „Man kann den Workflow exportieren." |
| „Im nächsten Schritt prüfen wir das Ergebnis." | „Im nächsten Schritt prüfst du…" |
| „Drei Knoten reichen für den Anfang." | (auch okay — beschreibend, ohne Anrede) |

**Begründung:** Die Wir-Form schafft eine kollegiale Tonalität, ohne belehrend zu wirken.

**Speaker-Notes-Stil-Regel des Slide-Repos gilt hier NICHT.** Wer Inhalte zwischen Buch und Folien überträgt, achtet bewusst auf den Stilwechsel: Buch = Wir-Form, Folien = indirekte Ansprache.

### 2. Callout-Disziplin

Drei Callout-Typen sind Standard:

- `::: {.callout-tip}` — Hinweise, Faustregeln, Analogien. Mit `collapse="true"` einklappbar, wenn die Analogie ausführlicher ist.
- `::: {.callout-note}` — neutrale Hintergrund-Information, Querverweise, Detail-Erklärungen.
- `::: {.callout-important}` — Pflicht-Aufmerksamkeit, Sicherheits-Hinweise, häufige Fallstricke.

Pro Kapitel **maximal 4–5 Callouts.** Wenn mehr Vertiefungen nötig sind, wird das Kapitel zu lang — dann lieber teilen.

**Title in Callouts ist Pflicht** bei allen `.callout-tip` und `.callout-important`. Bei `.callout-note` optional, aber empfohlen.

### 3. Analogie-Auswahl

Analogien kommen aus der **Berufsalltagswelt** der Zielgruppe (Business-Professionals, Fachkräfte, Studierende mit beruflichem Bezug):

**Geeignet:**

- Werkstatt, Werkbank, Werkzeug an der Wand
- Bibliothek, Bibliothekarin, Dossier, Regal
- Büro, Assistenz, Schreibtisch, Korrespondenz
- Küche, Rezept, Zutat, Kochutensil
- Labor, Qualitätskontrolle, Messgerät
- Kontrollraum, Cockpit, Dashboard

**Nicht geeignet** (gleiche Verbots-Liste wie im Slide-Repo):

- Märchen, Mythologie, Zauberei
- Cartoon-Tiere, anthropomorphisierte Objekte
- Kindergarten-Beispiele (Bauklötze, Ampelmännchen)
- Superhelden, Videospiele
- „cute"-Stil

Eine Analogie pro Hauptbegriff reicht. Mehrere Analogien für denselben Begriff verwirren.

### 4. Pro Lesson ein Kapitel

**Eine Lesson = ein `.qmd`-Kapitel = später ein Slide-Deck.** Das ist die strikte Granularitäts-Regel.

- Wer einen Begriff einführt und sofort drei Use-Cases zeigt, hat zwei Lessons.
- Wer ein Konzept erklärt und parallel ein zweites Konzept einführt, hat zwei Lessons.
- Pro Kapitel ein H1, mehrere H2, optional H3 für Unter-Aspekte.

**Lernzeit pro Kapitel: 5–15 Minuten.** Wer länger braucht, hat zu viel Stoff im selben Kapitel.

### 5. Erstentwurf-Workflow

Ein neues Buch entsteht in zwei Stufen:

**Stufe A — Erstentwurf aus Speaker-Notes oder Recherche.**
Pro Lesson ein Kapitel mit:

- H1-Titel (kann später angepasst werden)
- Status-Callout am Anfang:
  ```
  ::: {.callout-note title="Status — Erstentwurf"}
  Erstentwurf aus den Speaker-Notes des zugehörigen Decks. Ausbau-Punkte am Ende.
  :::
  ```
- Wir-Form-Prosa der zentralen Aussagen
- Mindestens ein Callout (tip oder important) für Vertiefung
- Am Ende: TODO-Block
  ```
  ## Was als Nächstes ausgebaut werden muss

  - Konkreter Punkt 1 (etwa: Schritt-für-Schritt-Anleitung mit Screenshots)
  - Konkreter Punkt 2 (etwa: Konfigurations-Beispiel)
  - …
  ```

**Stufe B — Vollausbau pro Lesson.**

- Status-Callout entfernen
- TODO-Punkte abarbeiten: Screenshots ergänzen, Code-Beispiele, ausführliche Anleitungen, Vergleichs-Tabellen
- Zusätzliche Callouts für Tipps, Warnungen, vertiefende Analogien
- Zwei bis drei Mal so lang wie der Erstentwurf

Der Generator strippt den Status-Callout und den TODO-Block automatisch beim Erzeugen des Slide-Decks. Beide sind also für den Folien-Output unsichtbar.

### 6. Disziplin-Verbote

- **Direkt-Anrede** (du, Sie) — das ist der Folien-Stil, nicht der Buch-Stil
- **„man"-Konstruktionen** — wirken altbacken
- **Cartoon-Emojis im Fließtext** — Ausnahme: Status-Marker in Tabellen (✅ 🟡)
- **Lange Code-Blöcke ohne Folge-Callout-Erklärung** — wer Code zeigt, erklärt ihn auch
- **Marketing-Sprache** — keine Superlative, keine „revolutionäre" oder „bahnbrechende" Tools
- **Tippfehler-konservierte Anglizismen** im sichtbaren Text — „Unlimited workflows" → „Unbegrenzte Workflows" (Anglizismus nur, wenn er der etablierte Fachbegriff ist und im selben Satz erklärt wird)

---

## Slug-Konventionen

**Modul-Verzeichnis-Slug**: kebab-case, beschreibend, kein „modul-XX"-Präfix nötig (Reihenfolge steht in `_quarto.yml`).

**Lesson-Datei-Slug**: kebab-case, beschreibt das Lesson-Thema, kein „lesson-XX"-Präfix.

Vollständige Verzeichnis-Karte siehe `README.md` im Repo-Root oder die Mono-Repo-Struktur ganz oben in dieser Datei.

---

## `_quarto.yml`-Schablone

```yaml
project:
  type: book

lang: de

execute:
  freeze: auto

book:
  title: "<Buch-Titel>"
  description: "<Untertitel oder Kernnutzen>"
  author: "Jan Kirenz"

  search:
    type: overlay
  page-footer:
    left: |
      © [Jan Kirenz](https://www.kirenz.com/), <JAHR>

  chapters:
    - index.qmd
    - introduction.qmd

    - part: <modul-1-slug>/index.qmd
      chapters:
        - <modul-1-slug>/<lesson-1>.qmd
        - <modul-1-slug>/<lesson-2>.qmd
        - …

    # … weitere Module

format:
  html:
    toc: true
    theme: cosmo
    code-copy: true
    highlight-style: github-dark
    code-overflow: wrap
    author-meta: "Jan Kirenz"
    callout-appearance: simple
```

---

## Index-Seiten — Konvention

### Top-Level `index.qmd`

- Titel `Willkommen {.unnumbered}`
- 2–3 Absätze: Wer das Buch ist, welcher Kurs damit verbunden ist, welcher Demo-Pfad sich durchzieht
- Nummerierte Liste mit Beispielen für den Einsatz des Themas
- `.callout-note` mit branchenübergreifenden Anwendungsfeldern
- `.callout-tip` mit Lernempfehlung am Ende

### `introduction.qmd`

- Titel `Einführung {.unnumbered}`
- Pro zentralen Begriff ein H2 mit zwei Sätzen Erklärung
- Reihenfolge folgt der späteren Buch-Reihenfolge

### Modul-`index.qmd`

- Titel `<Modul-Titel> {.unnumbered}`
- 1 Absatz: Worum es im Modul geht, was am Ende erreicht ist
- Aufzählung „Wir werden …": die Outcomes als Bulletpoints

---

## Generator-Schnittstelle

Das Skript `scripts/generate_slides.py` produziert aus jedem Lesson-Kapitel ein Reveal.js-Deck unter `slides/<modul>/<lesson>.qmd`. Erwartet wird:

1. **Genau ein H1** pro Kapitel (= Slide-Titel)
2. **H2-Sektionen** als Slide-Brüche (Reveal.js-Konvention)
3. **H3 wird zu H2 demoted** im Generator (wegen Reveal.js-Sektionierung)
4. **Status-Callouts** werden vom Generator gestrippt
5. **TODO-Block** am Ende wird vom Generator gestrippt
6. **Tabellen, Code-Blöcke, Listen** wandern unverändert ins Deck — werden in der Folie kondensiert sichtbar

**Konsequenz für die Schreibarbeit:** Wer ein Buch-Kapitel verfasst, hat bereits die Slide-Struktur im Kopf. Eine H2 sollte einen abgeschlossenen Gedanken tragen, der auch als eigene Folie Sinn ergibt.

---

## Was im Buch nichts zu suchen hat

- **Speaker-Notes-Blöcke** (`::: {.notes}`) — gehören ins Slide-Deck, nicht ins Buch
- **Reveal.js-spezifische Markup** wie `{.stage}`, `.fragment`, `.codewindow`, `.key-badge`
- **Bild-Profile-Kommentare** (`<!-- image: profile="..." -->`) — gehören ins Slide-Deck
- **D2-Diagramme als Inline-Code** — als gerenderte PNG/SVG ins `images/`-Verzeichnis ablegen und über `![](images/<file>)` einbinden

---

## Validierung vor Commit

```bash
quarto render
```

Errors müssen behoben sein. Warnings inhaltlich prüfen.

Optional: vor größeren Stand-Wechseln kurz die Generator-Pipeline durchlaufen lassen, um sicherzugehen, dass der Stripper noch alle Erstentwurf-Marker korrekt erkennt:

```bash
uv run python scripts/generate_slides.py
```

---

## Anbindung an die Lernplattform

Die Lernplattform (`hdm/lernplattform`) verlangt pro Lesson drei Quellen:

- `quarto_url` — Link zum HTML-Kapitel **dieses** Buches
- `slide_url` — Link zum gerenderten Reveal.js-Deck (wird vom Generator erzeugt)
- `youtube_video_id` — Videoaufzeichnung der Folien

Die Plattform spielt diese drei Quellen pro Lesson zusammen aus. Das Buch liefert den ausführlichen Lehrtext, das Deck die Verdichtung, das Video die mündliche Erklärung.

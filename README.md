# Lernplattform-Templates — Mono-Repo-Schablone

Quarto-Template-Repo für neue Kurse auf der Lernplattform. Buch und Folien-Decks leben **im selben Repository** — Buch im Root, Slides unter `slides/`. Aus einem Curriculum entstehen prosaische Buch-Kapitel (Wir-Form, Callouts, Analogien) und daraus generierte Folien-Decks (Indirekte Ansprache, Pattern-Bibliothek, Plattform-DNA-Look mit Geist-Font und Cream-Paper).

## Wann nutzen

Dieses Repo ist der **Startpunkt für jeden neuen Kurs**. Klonen, Curriculum füllen, KI das Repo + Curriculum übergeben — heraus kommen:

- Ein Online-Buch mit Kapiteln pro Lesson (kanonische Quelle, prosaisch ausführlich, mit Callouts)
- Pro Lesson ein Reveal.js-Folien-Deck (kompakt, Premium-Look, Stage/Desktop-Choreographie)
- Buch-Brücke vom Slide-Deck zurück zum Buch-Kapitel
- Speaker-Notes pro Folie, fertig für TTS-Vertonung

Vollständig ausgearbeitetes Beispiel-Repo: [`kirenz/n8n-grundlagen`](https://github.com/kirenz/n8n-grundlagen) (lokal unter `/Users/jankirenz/code/kurse/n8n-grundlagen/`).

## 5-Minuten-Quickstart

```bash
# 1. Repo aus Template anlegen
gh repo create kirenz/<kurs-slug> --template kirenz/lernplattform-templates --private --clone
cd <kurs-slug>

# 2. Slide-Verzeichnis: Python-Umgebung aufsetzen
cd slides && uv sync --group dev && cd ..

# 3. Buch-Skelett anpassen
#    - _quarto.yml: project.render und book.chapters auf konkrete Modul-Slugs
#    - index.qmd: Kurs-Willkommen schreiben
#    - introduction.qmd: Begriffs-Glossar
#    - Pro Modul: Verzeichnis anlegen mit index.qmd + Lesson-Skeletten

# 4. Buch-Kapitel modulweise ausschreiben
quarto render          # Buch in _book/

# 5. Folien generieren
uv run python scripts/generate_slides.py

# 6. Ein Slide-Deck feinjustieren (Stages, Notes, Bilder)
quarto render slides/<modul>/<lesson>.qmd
cd slides && uv run python scripts/validate_deck.py <modul>/<lesson>.qmd
```

## Repo-Struktur

```
.
├── _quarto.yml              # Buch-Build-Konfiguration (project: book)
├── AGENTS.md                # Mono-Repo + Buch-Stilregeln
├── README.md                # Diese Datei
├── book-theme.scss          # Buch-Theme im A-Look (Schwester von slides/redesign/)
├── .gitignore
│
│  # — Buch-Welt —
├── index.qmd                # Schablone: Willkommen
├── introduction.qmd         # Schablone: Begriffs-Glossar
├── beispiel-modul/          # Schablone: Modul mit Lesson
│   ├── index.qmd
│   └── beispiel-lesson.qmd
│
│  # — Slide-Welt —
├── slides/
│   ├── AGENTS.md            # Slide-Stilregeln (indirekte Ansprache)
│   ├── _metadata.yml        # Reveal.js-Defaults für alle Slide-Files
│   ├── _extensions/
│   ├── custom-new.scss
│   ├── elements.qmd         # Pattern-Bibliothek (im Default-Theme: Variante A)
│   ├── elements-redesign-a.qmd  # Pure-A-Demo (ohne custom-new.scss-Patterns)
│   ├── redesign/            # Default-Theme A (Geist, OKLch, Plattform-DNA)
│   ├── prompts/             # Bild-Generierung
│   ├── profiles/            # Image-Profile
│   ├── includes/            # D2-Diagramme, Footer, Fonts
│   ├── images/              # Slide-Bilder
│   ├── references.bib       # BibTeX
│   ├── scripts/             # validate_deck, generate_images, export_*
│   ├── tests/               # Pytest
│   ├── slide-template-*.qmd # Layout-Vorlagen
│   ├── video-template.qmd   # Schablone für komplettes Deck (Legacy)
│   ├── pyproject.toml
│   └── uv.lock
│
└── scripts/
    └── generate_slides.py   # Buch → Slides
```

## Stilwelten — bewusst getrennt

| Welt | Wo | Stil | AGENTS.md |
|---|---|---|---|
| Buch | Repo-Root + Modul-Verzeichnisse | **Wir-Form**, Callouts, Analogien | `./AGENTS.md` |
| Slides | `slides/` | **Indirekte Ansprache**, Patterns, Stages | `slides/AGENTS.md` |

Beim Übertrag von Buch zu Slide ist der Stilwechsel Pflicht.

## Buch-First-Workflow

Pro Lesson:

1. **Buch-Kapitel schreiben** im Repo-Root unter dem passenden Modul-Verzeichnis — Wir-Form, mit Callouts, Erstentwurf-Marker bei nicht ausgearbeiteten Kapiteln.
2. **Generator laufen lassen**: `uv run python scripts/generate_slides.py` — erzeugt `slides/<modul>/<lesson>.qmd` aus dem Buch-Kapitel.
3. **Slide-Deck feinjustieren**: Stage-Momente ergänzen, Speaker-Notes in indirekter Ansprache, Bild-Blöcke für Anschauung-Folien, Pattern-Disziplin gemäß `slides/AGENTS.md`.
4. **Validieren**: `cd slides && uv run python scripts/validate_deck.py <modul>/<lesson>.qmd`.

Keine Slide-Inhalte ohne entsprechendes Buch-Kapitel als Quelle.

## Bauen

### Buch

```bash
quarto render
open _book/index.html
```

Erfasst nur Pfade aus `project.render` in `_quarto.yml`. Slides werden nicht gebaut.

### Einzelnes Slide-Deck

```bash
quarto render slides/<modul>/<lesson>.qmd
```

Reveal.js-Defaults kommen aus `slides/_metadata.yml`.

### Alle Slide-Decks

```bash
cd slides
for f in <modul>-*/*.qmd; do
  quarto render "$f"
done
```

## Befehls-Cheatsheet

```bash
# Buch
quarto render

# Slide validieren (vor jedem Commit)
cd slides && uv run python scripts/validate_deck.py <deck>.qmd

# Slide rendern
quarto render slides/<modul>/<lesson>.qmd

# Slide-Bilder, Pfad A (automatisch via Gemini)
cd slides && uv run python scripts/generate_images.py <deck>.qmd

# Slide-Bilder, Pfad B (manuell via GPT-Image-2 in Codex)
cd slides && uv run python scripts/export_image_prompts.py <deck>.qmd

# Speaker Notes für TTS exportieren
cd slides && uv run python scripts/export_speaker_notes.py <deck>.qmd

# Tests
cd slides && uv run pytest -q

# Buch → Slides Generator
uv run python scripts/generate_slides.py
```

## Voraussetzungen

- **Quarto** ≥ 1.6
- **Python** ≥ 3.11 mit **uv** für Dependency-Management
- **D2** für Diagramme: `brew install d2` (oder von <https://d2lang.com>)
- Für Pfad A (Gemini): `GOOGLE_API_KEY` in `slides/.env`
- Für Pfad B (GPT-Image-2): aktiver Codex/ChatGPT-Zugang im Browser

## Kanonische Stilregel-Referenzen

- **Buch:** [`AGENTS.md`](AGENTS.md) — Wir-Form, Callouts, Analogien, Erstentwurf-Workflow
- **Slides:** [`slides/AGENTS.md`](slides/AGENTS.md) — Indirekte Ansprache, Pattern-Bibliothek, Stage-Choreographie. Default-Theme ist **Variante A — Pure Platform-Mirror** (Geist-Font, OKLch-Tokens, Cream-Paper, ruhige Editorial-Motion). Das ältere **Premium-Blueprint-Theme** (`custom-new.scss` allein) bleibt per Deck-Frontmatter-Override aktivierbar.

Buch und Slides teilen die gleiche Plattform-DNA: [`book-theme.scss`](book-theme.scss) (Buch) und [`slides/redesign/`](slides/redesign/) (Slides) nutzen identische Tokens (Geist, Cream-Paper, Ink, Ochre, Terracotta) und sehen damit nebeneinander aus wie Teile desselben Systems.

## Anbindung an die Lernplattform

Pro Lesson liefert das Repo drei Quellen:

- `quarto_url` — HTML-Kapitel des Buches (`_book/<modul>/<lesson>.html`)
- `slide_url` — Reveal.js-Deck (`slides/<modul>/<lesson>.html` nach Render)
- `youtube_video_id` — Videoaufzeichnung des Decks (manuell ergänzt)

## Mitwirken

Wenn neue Slide-Patterns oder Profile gebraucht werden:

1. Erst Diskussion (Issue / Notiz)
2. Pattern in `slides/elements.qmd` als Demo bauen
3. SCSS-Klasse in `slides/custom-new.scss`
4. Klassen-Name in `slides/scripts/qmd_utils.py` zu `ALLOWED_CLASSES` hinzufügen
5. Regel in `slides/AGENTS.md` dokumentieren

Validator (`slides/scripts/validate_deck.py`) lehnt unbekannte Klassen ab, Tests müssen grün bleiben.

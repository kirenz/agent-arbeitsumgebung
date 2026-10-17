"""Generiert Reveal.js-Folien-Decks aus den Buch-Kapiteln.

Liest jedes Lesson-Kapitel im Repo-Root (Buch-Welt) und schreibt das
abgeleitete Slide-Deck nach `slides/<modul>/<lesson>.qmd`. Strippt
Status-Callouts und „Was als Nächstes ausgebaut werden muss"-Blöcke,
demoted H3/H4 zu H2 für Reveal.js-Sektionierung.

Workflow:
    1. Liest jedes `.qmd` aus den in MODULE_DIRS aufgelisteten Verzeichnissen
    2. Entfernt die `Status — Erstentwurf`-Callouts
    3. Entfernt den TODO-Block am Ende
    4. Demoted H3/H4 zu H2 für Reveal.js-Sektionierung
    5. Hängt Reveal.js-Frontmatter an
    6. Schreibt nach `slides/<modul>/<lesson>.qmd`

Slide-Files erben das Reveal.js-Format aus `slides/_metadata.yml` —
das Frontmatter setzt nur Title, Subtitle und Author.

Aufruf:
    uv run python scripts/generate_slides.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "slides"

# Pro Modul ein Eintrag — beim Anlegen eines neuen Kurses anpassen.
# Im Template ist hier nur das Beispiel-Modul gesetzt.
MODULE_DIRS = [
    "beispiel-modul",
    # "<modul-2-slug>",
    # "<modul-3-slug>",
]

SLIDE_FRONTMATTER = """---
title: {title}
subtitle: {subtitle}
author: Jan Kirenz
---
"""

ROH_DECK_TODO = """
<!--
ROH-DECK aus dem Buch generiert. Feinjustierung gemäß slides/AGENTS.md, Phase 2:
- Stage-Opener als erste Folie (`# Hook {.stage ...}` mit background-image)
- Speaker-Notes pro Folie in indirekter Ansprache (`::: {.notes}`-Block)
- Key-Badges für Content-Folien (`[Konzept]{.key-badge}` etc.)
- Anschauung-Folien für Konzepte mit hohem Aha-Bedarf
- Closing-Beat (`{.stage .closing}`) als letzte Folie
- `## Weiter im Buch {.book-bridge}` falls book.chapter_slug im Frontmatter
- `## Literatur` mit `::: {#refs}`-Block am Ende
Diesen Kommentar nach Feinjustierung entfernen.
-->
"""

STATUS_CALLOUT_RE = re.compile(
    r":::\s*\{\.callout-note\s+title=\"Status — Erstentwurf\"\}.*?:::",
    re.DOTALL,
)
TODO_BLOCK_RE = re.compile(
    r"##\s+Was als Nächstes ausgebaut werden muss.*$",
    re.DOTALL | re.MULTILINE,
)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def process_chapter(input_path: Path, module_slug: str) -> None:
    """Liest ein Buch-Kapitel und schreibt das abgeleitete Deck."""
    text = input_path.read_text(encoding="utf-8")

    # Status-Callout und TODO-Liste raus — gehört nicht ins Deck
    text = STATUS_CALLOUT_RE.sub("", text)
    text = TODO_BLOCK_RE.sub("", text)

    # H1 als Titel extrahieren, Body danach
    h1_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if not h1_match:
        print(f"  [skip] {input_path.name}: kein H1 gefunden")
        return

    title = h1_match.group(1).strip()
    body = text[h1_match.end():].lstrip()

    # HTML-Kommentare strippen — Schablonen-Hinweise und Buch-Autor-Notizen
    # gehören nicht ins Deck. Bild-Prompt-Blöcke (`<!-- image: ... -->`) werden
    # beim Feinjustieren des Slide-Decks neu gesetzt.
    body = HTML_COMMENT_RE.sub("", body)

    # H3 → H2, H4 → H3 (Reveal.js zeigt H2 als neue Folie)
    body = re.sub(r"^####\s+", "### ", body, flags=re.MULTILINE)
    body = re.sub(r"^###\s+", "## ", body, flags=re.MULTILINE)

    # Frontmatter zusammenbauen — Reveal.js-Format kommt aus _metadata.yml.
    # Werte gequotet, weil Titel/Subtitle Doppelpunkte enthalten können.
    frontmatter = SLIDE_FRONTMATTER.format(
        title=yaml_quote(title),
        subtitle=yaml_quote(f"Modul: {module_slug}"),
    )

    # Output-Pfad
    output_dir = OUTPUT_DIR / module_slug
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / input_path.name

    output_path.write_text(frontmatter + ROH_DECK_TODO + "\n" + body, encoding="utf-8")
    print(f"  [ok]   {input_path.name} → {output_path.relative_to(ROOT)}")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    for module_slug in MODULE_DIRS:
        module_dir = ROOT / module_slug
        if not module_dir.is_dir():
            print(f"[warn] Modul-Verzeichnis fehlt: {module_slug}")
            continue

        print(f"Modul: {module_slug}")
        for qmd in sorted(module_dir.glob("*.qmd")):
            if qmd.name == "index.qmd":
                continue
            process_chapter(qmd, module_slug)

    print(f"\nFolien-Decks geschrieben nach {OUTPUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()

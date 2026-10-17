# Produktiv mit einem Agenten arbeiten

Quarto-Buch zum werkzeugneutralen Buchteil „Produktiv mit einem Agenten arbeiten“:
Projektordner, Markdown, AGENTS.md, Kontext, PDFs, laufend neue Dateien, Skills,
MCP sowie Konnektoren und Plugins.

- Buch: <https://kirenz.github.io/agent-arbeitsumgebung/>
- Lernplattform: Quellkurs `agent-arbeitsumgebung` im Repo `lernplattform`
  (Units, Konzept `docs/agent-arbeitsumgebung-konzept.md`)

## Aufbau

```
_quarto.yml              Buch dieses Repos (nur Rahmen)
index.qmd                Startseite dieses Buchs
agent-arbeitsumgebung/   DER BUCHTEIL; wird in Kursbücher eingebunden
  index.qmd, erweitern.qmd   Teil-Seiten
  *.qmd                      zehn Kapitel
  widgets/                   Muster-Agent-Szenen (generiert, nicht von Hand ändern)
  downloads/                 Beispielmaterial (preisliste-2026.pdf)
  images/                    statische Grafiken
```

Alle Pfade im Buchteil sind relativ. Darum funktionieren sie unverändert in
jedem Kursbuch, das den Ordner an derselben Stelle einbindet.

## Muster-Agent-Szenen aktualisieren

Die Szenen stammen aus dem Lernplattform-Repo
(`apps/api/app/db/units/agent-arbeitsumgebung/_widgets/szenen/`).

```bash
cd ~/code/hdm/lernplattform/apps/api
PYTHON_ENV=development uv run python scripts/build_muster_agent.py --book ~/code/kurse/agent-arbeitsumgebung/agent-arbeitsumgebung/widgets
```

Danach die Seiten `11-*` und `12-*` (kurseigene n8n-Szenen) hier löschen.

## Veröffentlichen

1. Rendern und veröffentlichen: `quarto publish gh-pages --no-prompt`
2. Branch `teil` aktualisieren (nur der Ordner `agent-arbeitsumgebung/`):

```bash
git subtree split --prefix agent-arbeitsumgebung -b teil
git push origin teil
```

## In ein Kursbuch einbinden

Voraussetzung: Das Kursbuch ist ein Quarto-Buch mit sauberem Arbeitsstand.

1. Den Teil als Subtree holen:

```bash
git subtree add --prefix agent-arbeitsumgebung https://github.com/kirenz/agent-arbeitsumgebung.git teil --squash
```

2. In `_quarto.yml` unter `project.render` die Zeile `"agent-arbeitsumgebung/*.qmd"` ergänzen.
3. Unter `project.resources` die Ordner `widgets/*`, `downloads/*` und `images/*` des Teils ergänzen.
4. Unter `book.chapters` die beiden Teile mit ihren Kapiteln eintragen (Reihenfolge wie in diesem Repo).
5. Prüfen: `quarto render` läuft ohne Fehler, die Szenen lassen sich durchklicken.

Später aktualisieren:

```bash
git subtree pull --prefix agent-arbeitsumgebung https://github.com/kirenz/agent-arbeitsumgebung.git teil --squash
```

> **Warnung:** Den Buchteil nur hier ändern, nie im eingebundenen Ordner eines Kursbuchs. Sonst entstehen Konflikte beim nächsten `subtree pull`.

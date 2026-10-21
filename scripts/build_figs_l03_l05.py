"""Lehrbilder für Kapitel 3 „Der Projektordner“, 4 „AGENTS.md“ und 5 „Kontext bereitstellen“.

Spezifikation: Rollout Gruppe A vom 2026-10-18 (Bilder A bis I).
Alle Schriften mindestens 16 px, Titel 20 px, Farben nur aus figlib.

Run: uv run python scripts/build_figs_l03_l05.py  (oder python3)
Ausgabe: agent-arbeitsumgebung/images/lektionen/l03-projektordner/, l04-agents-md/,
l05-kontext-bereitstellen/
"""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from figlib import *  # noqa: E402,F401,F403
from figlib import (  # noqa: E402
    BLUE, F, GREEN, INK, LIGHT, MUTED, PAPER, RED, RULE,
    arrow, box, glyph, path_arrow, save, svg, text, text_width, wrap_px,
)

L3 = "l03-projektordner"
L4 = "l04-agents-md"
L5 = "l05-kontext-bereitstellen"
MONO = 'font-family="ui-monospace, Menlo, monospace"'
MONO_W = 0.602  # Zeichenbreite Menlo/ui-monospace relativ zur Schriftgröße


# ---------------------------------------------------------------- Helfer (16 px)

def T(x, y, s, size=16, weight=400, fill=INK, anchor="start", mono=False):
    return text(x, y, s, size, weight, fill, anchor, mono)


def heading(cx, s, y=36):
    return text(cx, y, s, 20, 700, INK, "middle")


def multiline(x, y, s, max_w, size=16, weight=400, fill=INK, anchor="start", lh=21):
    return "".join(T(x, y + i * lh, ln, size, weight, fill, anchor)
                   for i, ln in enumerate(wrap_px(s, max_w, size, weight)))


def hs_box(x, y, w, h, head, sub=None, fill="#ffffff", stroke=RULE, hcol=INK, hsize=16, hweight=600,
           scol=MUTED, sw=1.5, lh=21):
    """Kasten mit zentriertem Kopf und optionalem, umbrochenem Untertitel (16 px)."""
    out = box(x, y, w, h, fill, stroke, sw=sw)
    subs = []
    if sub:
        for part in (sub if isinstance(sub, list) else [sub]):
            subs += wrap_px(part, w - 28, 16)
    block = hsize + len(subs) * lh
    top = y + (h - block) / 2 + hsize * 0.8
    out += T(x + w / 2, top, head, hsize, hweight, hcol, "middle")
    for i, ln in enumerate(subs):
        out += T(x + w / 2, top + (i + 1) * lh + 1, ln, 16, 400, scol, "middle")
    return out


def left_box(x, y, w, h, head, sub=None, fill="#ffffff", stroke=RULE, hcol=INK, pad=18, lh=21, sw=1.5):
    """Kasten mit linksbündigem Kopf und umbrochenem Untertitel, vertikal zentriert."""
    out = box(x, y, w, h, fill, stroke, sw=sw)
    subs = wrap_px(sub, w - 2 * pad, 16) if sub else []
    block = 16 + len(subs) * lh
    top = y + (h - block) / 2 + 13
    out += T(x + pad, top, head, 16, 600, hcol)
    for i, ln in enumerate(subs):
        out += T(x + pad, top + (i + 1) * lh + 1, ln, 16, 400, MUTED)
    return out


def pill16(x, y, label, fill=LIGHT, stroke=BLUE, tcol=BLUE, mono=False, size=16):
    w = (len(label) * size * MONO_W if mono else text_width(label, size, 600)) + 22
    h = size + 12
    return (box(x, y, w, h, fill, stroke, h / 2, 1.2)
            + text(x + w / 2, y + size + 2, label, size, 600 if not mono else 700, tcol, "middle", mono))


def badge16(cx, cy, label, r=16, fill=BLUE):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>' + T(cx, cy + 6, label, 16, 700, "#ffffff", "middle")


def note16(x, y, w, s):
    return box(x, y, w, 44, PAPER, PAPER, 8) + T(x + 18, y + 28, s, 16, 400, INK)


def mono_rich(x, y, parts, size=16, anchor="start"):
    """Monozeile aus (text, farbe, gewicht)-Teilen; Leerzeichen bleiben erhalten."""
    spans = "".join(
        f'<tspan fill="{c}" font-weight="{wt}">{escape(s)}</tspan>' for s, c, wt in parts)
    return (f'<text x="{x}" y="{y}" {MONO} font-size="{size}" text-anchor="{anchor}" '
            f'xml:space="preserve">{spans}</text>')


def line(x1, y1, x2, y2, col=RULE, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}"{d}/>'


def cross(cx, cy, col=RED):
    return (f'<circle cx="{cx}" cy="{cy}" r="14" stroke="{col}" stroke-width="2" fill="#ffffff"/>'
            f'<path d="M{cx - 6},{cy - 6} L{cx + 6},{cy + 6} M{cx + 6},{cy - 6} L{cx - 6},{cy + 6}" '
            f'stroke="{col}" stroke-width="3" fill="none"/>')


def file_card(x, y, w, h, name):
    """Datei als Karte mit grauer Kopfleiste und Dateiname."""
    return (box(x, y, w, h, "#ffffff", RULE)
            + f'<path d="M{x + 10},{y} H{x + w - 10} Q{x + w},{y} {x + w},{y + 10} V{y + 36} H{x} V{y + 10} '
              f'Q{x},{y} {x + 10},{y} Z" fill="{PAPER}" stroke="{RULE}" stroke-width="1.5"/>'
            + T(x + 18, y + 24, name, 16, 600, INK, mono=True))


# ---------------------------------------------------------------- Lektion 3

def fig_projektordner_arbeitsplatz():
    W, H = 1000, 470
    b = [heading(500, "Beispielfall: der Projektordner als Arbeitsplatz mit Ablage")]
    # Ordnerrahmen mit Reiter
    b.append(box(30, 70, 620, 330, LIGHT, BLUE, 14))
    b.append(box(30, 54, 200, 32, BLUE, BLUE, 8))
    b.append(T(130, 76, "kundenanfragen", 16, 700, "#ffffff", "middle", mono=True))
    # README
    b.append(box(60, 104, 560, 70, "#ffffff", RULE))
    b.append(glyph("doc", 92, 139))
    b.append(T(122, 133, "README.md", 16, 600, mono=True))
    b.append(T(122, 158, "Begrüßungsschreiben: wozu der Ordner da ist", 16, 400, MUTED))
    # Fach anfragen
    b.append(box(60, 192, 265, 150, "#ffffff", RULE))
    b.append(T(80, 222, "anfragen", 16, 600, mono=True))
    b.append(T(80, 246, "Fach für Anfragen", 16, 400, MUTED))
    for cx in (100, 140, 180):
        b.append(glyph("doc", cx, 298, MUTED))
    # Fach antworten
    b.append(box(355, 192, 265, 150, "#ffffff", RULE))
    b.append(T(375, 222, "antworten", 16, 600, mono=True))
    b.append(T(375, 246, "Fach für Entwürfe", 16, 400, MUTED))
    b.append(box(375, 266, 225, 58, "#ffffff", RULE, dash="6 4"))
    b.append(T(487.5, 300, "noch leer", 16, 400, MUTED, "middle"))
    # Grenze
    b.append(pill16(60, 356, "Der Agent arbeitet nur hier"))
    b.append(line(675, 70, 675, 400, RULE, 1.5, "6 4"))
    b.append(T(835, 104, "liegt woanders", 16, 600, MUTED, "middle"))
    b.append(hs_box(700, 124, 270, 74, "Buchhaltung", "anderes Vorhaben", fill=PAPER))
    b.append(hs_box(700, 222, 270, 74, "Private Dokumente", "gehört nicht zur Arbeit", fill=PAPER))
    b.append(note16(30, 416, 940, "Ein Ordner je Vorhaben, mit allem Material darin. Fremdes bleibt draußen."))
    return save(f"{L3}/projektordner-arbeitsplatz.svg", svg(W, H, b))


def fig_dateiname_aufbau():
    W, H = 1000, 440
    b = [heading(500, "So ist ein Dateiname aufgebaut")]
    size = 28
    cw = size * MONO_W
    parts = [("2026-10-05", BLUE, 700), ("-", INK, 400), ("terminwunsch", INK, 700), (".md", MUTED, 400)]
    total = sum(len(p[0]) for p in parts)
    x0 = 500 - total * cw / 2
    b.append(mono_rich(x0, 104, parts, size))
    # Mitte der drei Teile
    m_datum = x0 + 5 * cw
    m_anl = x0 + (11 + 6) * cw
    m_end = x0 + (23 + 1.5) * cw
    cards = [(30, "1", "Datum vorn", "JJJJ-MM-TT, sortiert nach Eingang"),
             (350, "2", "Anliegen", "Kleinbuchstaben, ue statt ü, Bindestrich statt Leerzeichen"),
             (670, "3", "Endung .md", "eine Markdown-Datei")]
    for (cx, _, _, _), m in zip(cards, (m_datum, m_anl, m_end)):
        mid = cx + 150
        b.append(f'<path d="M{m},{118} V{150} H{mid} V{184}" stroke="{RULE}" stroke-width="1.5" fill="none"/>')
        b.append(f'<circle cx="{m}" cy="118" r="3" fill="{MUTED}"/>')
    for cx, n, head, sub in cards:
        b.append(box(cx, 186, 300, 104, "#ffffff", RULE))
        b.append(badge16(cx + 30, 214, n))
        b.append(T(cx + 56, 220, head, 16, 600))
        b.append(multiline(cx + 20, 252, sub, 262, 16, 400, MUTED))
    # Sortierung
    b.append(box(30, 312, 940, 112, PAPER, PAPER, 8))
    b.append(T(50, 340, "Sortiert sich von selbst:", 16, 600))
    names = ["2026-10-05-terminwunsch.md", "2026-10-06-preisfrage.md", "2026-10-07-beschwerde.md"]
    for i, nm in enumerate(names):
        y = 340 + i * 28
        b.append(badge16(312, y - 6, str(i + 1), r=12, fill=MUTED))
        b.append(mono_rich(334, y, [(nm[:10], BLUE, 700), (nm[10:], INK, 400)]))
    b.append(multiline(650, 368, "Jahr, Monat, Tag: alphabetisch und zeitlich gleich", 300, 16, 400, MUTED))
    return save(f"{L3}/dateiname-aufbau.svg", svg(W, H, b))


def fig_zwei_sitzungen():
    W, H = 1000, 470
    b = [heading(500, "Zwei Sitzungen, ein Ordner")]
    # Sitzung 1
    b.append(box(30, 70, 290, 260, "#ffffff", RULE))
    b.append(T(50, 100, "Sitzung 1", 18, 700))
    b.append(T(50, 124, "gestern", 16, 400, MUTED))
    b.append(box(50, 140, 250, 44, LIGHT, LIGHT, 8))
    b.append(T(62, 168, "Lege den Projektordner an.", 16))
    b.append(T(50, 216, "› README.md angelegt", 16, 400, MUTED, mono=True))
    b.append(T(50, 242, "› 3 Anfragen angelegt", 16, 400, MUTED, mono=True))
    b.append(T(50, 308, "Ende der Sitzung", 16, 600, MUTED))
    # Sitzung 2
    b.append(box(680, 70, 290, 260, "#ffffff", RULE))
    b.append(T(700, 100, "Sitzung 2", 18, 700))
    b.append(T(700, 124, "heute, ohne Erinnerung", 16, 400, MUTED))
    b.append(box(700, 140, 250, 44, LIGHT, LIGHT, 8))
    b.append(T(712, 168, "Was liegt in diesem Ordner?", 16))
    b.append(T(700, 216, "› liest den Ordner", 16, 400, MUTED, mono=True))
    b.append(box(700, 232, 250, 76, "#ffffff", RULE, 8))
    b.append(T(712, 260, "README.md, drei Anfragen,", 16))
    b.append(T(712, 284, "antworten (leer)", 16))
    # Ordner Mitte
    b.append(box(360, 110, 280, 170, LIGHT, BLUE, 14))
    b.append(T(500, 140, "kundenanfragen", 16, 700, BLUE, "middle", mono=True))
    for i, s in enumerate(["README.md", "anfragen (3)", "antworten"]):
        y = 180 + i * 32
        b.append(glyph("doc", 398, y - 6, INK))
        b.append(T(424, y, s, 16, 400, INK, mono=True))
    b.append(T(500, 306, "bleibt liegen", 16, 600, BLUE, "middle"))
    b.append(arrow(322, 200, 356, 200, color=BLUE))
    b.append(arrow(644, 200, 678, 200, color=BLUE))
    # Trennlinie
    b.append(line(175, 362, 825, 362, MUTED, 1.5, "6 4"))
    b.append(box(395, 346, 210, 32, "#ffffff", "#ffffff", 4))
    b.append(T(500, 368, "keine Erinnerung", 16, 600, MUTED, "middle"))
    b.append(note16(30, 404, 940, "Arbeitsordner: Der gewählte Ordner begrenzt die Arbeit. Außerhalb fragt der Agent erst nach."))
    return save(f"{L3}/zwei-sitzungen-ein-ordner.svg", svg(W, H, b))


# ---------------------------------------------------------------- Lektion 4

def fig_hausordnung_aufbau():
    W, H = 1000, 490
    b = [heading(500, "AGENTS.md: die Hausordnung in zwei Teilen")]
    b.append(file_card(30, 64, 490, 350, "AGENTS.md"))
    b.append(pill16(50, 114, "Teil 1: Zweck"))
    b.append(mono_rich(50, 172, [("#", BLUE, 700), (" Kundenanfragen", INK, 400)]))
    b.append(T(50, 198, "Zwei Sätze, worum es im Ordner geht.", 16, 400, MUTED))
    b.append(pill16(50, 218, "Teil 2: Regeln"))
    b.append(mono_rich(50, 276, [("##", BLUE, 700), (" Regeln", INK, 400)]))
    rules = ["Antworte auf Deutsch.", "Nur Fakten aus dem Ordner.", "Keine Personennamen.",
             "Ergebnisse als neue Datei.", "Geänderte Dateien nennen."]
    for i, r in enumerate(rules):
        b.append(mono_rich(50, 306 + i * 24, [(f"{i + 1}.", BLUE, 700), (f" {r}", INK, 400)]))
    # rechts oben
    b.append(box(550, 64, 420, 120, LIGHT, BLUE))
    b.append(glyph("agent", 588, 124, BLUE))
    b.append(T(620, 104, "Liest der Agent zu Beginn", 16, 600, BLUE))
    b.append(T(620, 126, "jeder Sitzung", 16, 600, BLUE))
    b.append(T(620, 152, "wie ein neuer Mitarbeiter", 16, 400, MUTED))
    b.append(T(620, 174, "die Hausordnung jeden Morgen", 16, 400, MUTED))
    # rechts unten: prüfbar oder nicht (untereinander)
    b.append(box(550, 206, 420, 208, "#ffffff", RULE))
    b.append(T(570, 236, "Prüfbare Regel?", 16, 600))
    b.append(glyph("check", 586, 284))
    b.append(T(614, 280, "Beträge in EUR mit Komma", 16, 600, GREEN))
    b.append(T(614, 302, "am Ergebnis kontrollierbar", 16, 400, MUTED))
    b.append(cross(586, 362))
    b.append(T(614, 358, "Schreibe sorgfältig", 16, 600, RED))
    b.append(T(614, 380, "niemand kann es prüfen", 16, 400, MUTED))
    b.append(note16(30, 432, 940, "Fünf bis zehn kurze Regeln, nummeriert: Dann genügt im Gespräch „Regel 2“."))
    return save(f"{L4}/hausordnung-aufbau.svg", svg(W, H, b))


def fig_eine_hausordnung():
    W, H = 1000, 490
    b = [heading(500, "Eine Hausordnung, verschiedene Werkzeuge")]
    # AGENTS.md
    b.append(box(30, 90, 290, 220, LIGHT, BLUE))
    b.append(glyph("doc", 175, 134, BLUE))
    b.append(T(175, 186, "AGENTS.md", 18, 700, BLUE, "middle", mono=True))
    b.append(T(175, 214, "einziger Ort für Regeln", 16, 600, INK, "middle"))
    b.append(T(175, 250, "offenes Format:", 16, 400, MUTED, "middle"))
    b.append(T(175, 272, "Markdown mit festem Namen", 16, 400, MUTED, "middle"))
    # Verweisdatei
    b.append(box(392, 214, 160, 62, "#ffffff", MUTED, dash="6 4"))
    b.append(T(472, 239, "Verweisdatei", 16, 600, INK, "middle"))
    b.append(T(472, 263, "→ AGENTS.md", 16, 400, MUTED, "middle", mono=True))
    # Werkzeuge
    tools = [(70, "liest AGENTS.md direkt", "nichts weiter nötig"),
             (196, "erwartet eigenen Namen", "eine kleine Datei verweist"),
             (322, "weicht ab", "seine Selbstauskunft gilt")]
    for y, head, sub in tools:
        b.append(box(610, y, 360, 90, "#ffffff", RULE))
        b.append(glyph("agent", 646, y + 48))
        b.append(T(680, y + 38, "Werkzeug " + head, 16, 600))
        b.append(T(680, y + 62, sub, 16, 400, MUTED))
    b.append(arrow(608, 115, 324, 150, color=BLUE))
    b.append(arrow(608, 241, 556, 245, color=BLUE))
    b.append(arrow(390, 245, 324, 245, color=BLUE))
    b.append(note16(30, 432, 940, "Regeln stehen nur in AGENTS.md. Andere Dateien verweisen dorthin."))
    return save(f"{L4}/eine-hausordnung-viele-werkzeuge.svg", svg(W, H, b))


def fig_annahme_statt_erfinden():
    W, H = 1000, 430
    b = [heading(500, "Eine Frage ohne Antwort im Ordner")]
    steps = [(30, "Frage im Chat", "„Wie teuer ist eine Reparatur?“", LIGHT, BLUE),
             (280, "Agent sucht im Ordner", "keine Preisliste", "#ffffff", RULE),
             (530, "Nur Fakten aus Dateien", "sonst „Annahme:“", "#ffffff", RULE),
             (780, "Antwort", "„Annahme: Preisliste fehlt“", LIGHT, BLUE)]
    for x, head, sub, fl, st in steps:
        w = 190 if x == 780 else 200
        b.append(hs_box(x, 100, w, 100, head, sub, fill=fl, stroke=st))
    b.append(pill16(580, 70, "Regel 2"))
    for x1 in (230, 480, 730):
        b.append(arrow(x1 + 4, 150, x1 + 46, 150))
    b.append(box(30, 228, 940, 118, PAPER, PAPER, 8))
    b.append(T(50, 258, "Was gegriffen hat:", 16, 600))
    cols = [(66, "1", ["Antwort auf Deutsch"]),
            (346, "2", ["Lücke mit „Annahme:“", "gekennzeichnet"]),
            (656, "5", ["„Angelegt oder geändert:", "keine Dateien“"])]
    for cx, n, txt in cols:
        b.append(badge16(cx, 296, n))
        for i, s in enumerate(txt):
            b.append(T(cx + 26, 302 + i * 22, s, 16))
    b.append(note16(30, 366, 940, "Regeln senken das Risiko. Preise, Termine und Zusagen weiter gegen die Quelle prüfen."))
    return save(f"{L4}/annahme-statt-erfinden.svg", svg(W, H, b))


def fig_geltungsbereich():
    W, H = 1000, 460
    b = [heading(500, "Wo eine AGENTS.md gilt")]
    b.append(box(30, 70, 610, 320, LIGHT, BLUE, 14))
    b.append(T(50, 98, "kundenanfragen", 16, 700, BLUE, mono=True))
    b.append(box(60, 112, 550, 62, "#ffffff", BLUE))
    b.append(glyph("doc", 92, 143, BLUE))
    b.append(T(122, 138, "AGENTS.md", 16, 700, INK, mono=True))
    b.append(T(122, 162, "gilt für den Ordner und alle Unterordner", 16, 400, MUTED))
    b.append(hs_box(60, 222, 160, 150, "anfragen", "drei Anfragen"))
    b.append(hs_box(240, 222, 160, 150, "antworten", "Entwürfe"))
    b.append(box(420, 222, 190, 150, "#ffffff", RULE))
    b.append(T(515, 250, "vorlagen", 16, 600, INK, "middle"))
    b.append(box(434, 266, 162, 92, "#ffffff", BLUE, dash="6 4"))
    b.append(T(515, 292, "AGENTS.md", 16, 700, INK, "middle", mono=True))
    b.append(T(515, 316, "ergänzt Regeln", 16, 400, MUTED, "middle"))
    b.append(T(515, 338, "nur für Vorlagen", 16, 400, MUTED, "middle"))
    for tx in (140, 320, 515):
        b.append(arrow(tx, 176, tx, 218, color=BLUE))
    b.append(left_box(670, 70, 300, 140, "Anweisung im Chat", "geht den Regeln der Datei vor, etwa „Antworte diesmal auf Englisch.“"))
    b.append(left_box(670, 230, 300, 160, "Kurz bleiben", "fünf bis zehn Regeln; Abläufe mit vielen Schritten gehören in einen Skill", fill=PAPER, stroke=PAPER))
    b.append(note16(30, 404, 940, "Eine Datei oben genügt. Eine zweite in einem Unterordner ergänzt dort."))
    return save(f"{L4}/geltungsbereich.svg", svg(W, H, b))


# ---------------------------------------------------------------- Lektion 5

def fig_ablageplan():
    W, H = 1000, 470
    b = [heading(500, "UEBERSICHT.md: der Ablageplan")]
    b.append(file_card(30, 64, 570, 320, "UEBERSICHT.md"))
    cols = [(46, 300, "Datei"), (350, 120, "Inhalt"), (474, 110, "Stand")]
    for x, w, s in cols:
        b.append(box(x, 116, w, 34, PAPER, RULE, 4, 1))
        b.append(T(x + 10, 139, s, 16, 600))
    rows = [("README.md", "Zweck", "2026-10-12"), ("AGENTS.md", "Regeln", "2026-10-14"),
            ("2026-10-05-terminwunsch.md", "Termin", "2026-10-05"),
            ("2026-10-06-preisfrage.md", "Preis", "2026-10-06"),
            ("2026-10-07-beschwerde.md", "Beschwerde", "2026-10-07")]
    for i, (d, inh, st) in enumerate(rows):
        y = 182 + i * 40
        b.append(T(56, y, d, 16, 400, INK, mono=True))
        b.append(T(360, y, inh, 16))
        b.append(T(484, y, st, 16, 400, MUTED, mono=True))
        if i < len(rows) - 1:
            b.append(line(46, y + 14, 584, y + 14, RULE, 1))
    cards = [(64, "Was liegt wo", "eine Zeile je Datei, mit einem Satz", LIGHT, BLUE, BLUE),
             (174, "Spalte Stand", "ein altes Datum fällt sofort auf", "#ffffff", RULE, INK),
             (296, "Der Agent pflegt sie", "Regel 6: zu Beginn lesen, nach jedem Auftrag ergänzen", "#ffffff", RULE, INK)]
    for y, head, sub, fl, st, hc in cards:
        b.append(left_box(630, y, 340, 88, head, sub, fill=fl, stroke=st, hcol=hc))
    b.append(arrow(628, 218, 590, 150))
    b.append(note16(30, 404, 940, "README.md erklärt Menschen, worum es geht. Die Übersicht sagt, was wo liegt."))
    return save(f"{L5}/ablageplan.svg", svg(W, H, b))


def fig_kontext_drei_teile():
    W, H = 1000, 440
    b = [heading(500, "Kontext: was der Agent für einen Auftrag liest")]
    cards = [(30, "1", "Der Auftrag", "„Welche Anfrage ist", "die älteste?“", "bei jedem Auftrag", LIGHT, BLUE),
             (355, "2", "Die Anweisungsdatei", "AGENTS.md mit", "den Regeln", "zu Beginn jeder Sitzung", "#ffffff", RULE),
             (680, "3", "Dateien, die er öffnet", "etwa UEBERSICHT.md,", "später die Preisliste", "wenn er sie braucht", "#ffffff", RULE)]
    for x, n, head, l1, l2, when, fl, st in cards:
        b.append(box(x, 70, 290, 170, fl, st))
        b.append(badge16(x + 30, 102, n))
        b.append(T(x + 56, 108, head, 16, 600))
        b.append(T(x + 22, 150, l1, 16))
        b.append(T(x + 22, 172, l2, 16))
        b.append(line(x + 22, 192, x + 268, 192, RULE, 1))
        b.append(T(x + 22, 220, when, 16, 400, MUTED))
    for cx in (337.5, 662.5):
        b.append(T(cx, 164, "+", 26, 700, MUTED, "middle"))
    b.append(box(30, 266, 940, 82, PAPER, PAPER, 8))
    b.append(T(50, 298, "Nicht dabei: was der Agent in einer früheren Sitzung gelesen hat.", 16, 600))
    b.append(T(50, 326, "Was im Ordner liegt, kann er jederzeit wieder öffnen.", 16, 400, MUTED))
    b.append(box(30, 372, 940, 44, "#ffffff", RULE, 8))
    b.append(T(48, 400, "Mehr ist nicht besser: Eine alte Datei neben der neuen kann zur falschen Zahl führen.", 16))
    return save(f"{L5}/kontext-drei-teile.svg", svg(W, H, b))


# ---------------------------------------------------------------- Interview (Umbau 2026-10-21)

def fig_was_in_den_ordner_darf():
    W, H = 1000, 470
    b = [heading(500, "Was in den Projektordner darf")]
    gut = ["eigene Vorlagen", "Preislisten, Produktbeschreibungen", "Abläufe und Checklisten",
           "Kopien von Anfragen ohne Namen"]
    nein = ["Personendaten (Namen, Adressen, Telefon)", "Zugangsdaten, Verträge",
            "Gesundheits- und Finanzdaten von Personen", "vertraulich gekennzeichnete Dokumente"]
    for x, head, items, col, fill in ((30, "Geeignet", gut, GREEN, "#f0fdf4"),
                                       (515, "Nicht in den Ordner", nein, RED, "#fef2f2")):
        b.append(box(x, 62, 455, 250, fill, col, 12))
        b.append(T(x + 24, 96, head, 18, 700, col))
        for i, it in enumerate(items):
            y = 140 + i * 42
            if col == GREEN:
                b.append(f'<path d="M{x + 26},{y - 6} l6,7 l12,-13" stroke="{GREEN}" stroke-width="3" fill="none"/>')
            else:
                b.append(cross(x + 34, y - 6))
            b.append(T(x + 56, y, it))
    # Fluss zum Anbieter
    b.append(hs_box(30, 336, 300, 64, "Projektordner", "auf Ihrem Rechner"))
    b.append(arrow(340, 368, 650, 368, color=BLUE))
    b.append(T(495, 356, "Agent liest und sendet", 16, 600, BLUE, "middle"))
    b.append(hs_box(660, 336, 310, 64, "Anbieter des Sprachmodells", "verarbeitet den Inhalt"))
    b.append(note16(30, 414, 940, "Was der Agent liest, geht an den Anbieter. Namen vorher durch Rollen ersetzen."))
    return save(f"{L3}/was-in-den-ordner-darf.svg", svg(W, H, b))


def fig_interview_vorschlag_freigabe():
    W, H = 1000, 380
    b = [heading(500, "Interview, Vorschlag, Freigabe, Anlegen")]
    st = [("Interview", "eine Frage nach der anderen, höchstens sechs"),
          ("Vorschlag", "Liste: Ordner, Unterordner, README.md"),
          ("Freigabe", "Sie prüfen, ändern oder stimmen zu"),
          ("Anlegen", "nur Ordner, Unterordner und README.md")]
    w, gap = 214, 28
    for i, (hd, sb) in enumerate(st):
        x = 30 + i * (w + gap)
        hl = i == 2
        b.append(box(x, 70, w, 170, LIGHT if hl else "#ffffff", BLUE if hl else RULE, 12, 2 if hl else 1.5))
        b.append(badge16(x + 28, 100, str(i + 1)))
        b.append(T(x + 54, 106, hd, 18, 700, BLUE if hl else INK))
        b.append(multiline(x + 18, 150, sb, w - 36, 16, 400, MUTED))
        if i < 3:
            b.append(arrow(x + w + 2, 155, x + w + gap - 2, 155))
    b.append(T(30 + 2 * (w + gap) + w / 2, 272, "Ohne Freigabe entsteht nichts.", 16, 600, BLUE, "middle"))
    b.append(note16(30, 310, 940, "Ein Vorschlag lässt sich leichter korrigieren als ein fertiger Ordner."))
    return save(f"{L3}/interview-vorschlag-freigabe.svg", svg(W, H, b))


def fig_readme_fuenf_abschnitte():
    W, H = 1000, 500
    b = [heading(500, "Die README.md und wer sie weiter nutzt")]
    b.append(box(30, 62, 400, 360, "#ffffff", RULE, 12))
    b.append(glyph("doc", 62, 96))
    b.append(T(92, 102, "README.md", 18, 700, mono=True))
    rows = [("Zweck", "AGENTS.md: die Hausordnung"),
            ("Beteiligte", "MCP: Zugänge zu anderen Systemen"),
            ("Material", "Kontext, PDFs, Excel"),
            ("Wiederkehrende Aufgaben", "Skills: Abläufe, die bleiben"),
            ("Vorgesehene Regeln", "AGENTS.md: Projektregeln")]
    for i, (sec, les) in enumerate(rows):
        y = 140 + i * 56
        b.append(box(50, y, 360, 42, PAPER, PAPER, 8))
        b.append(mono_rich(66, y + 27, [("## ", BLUE, 700), (sec, INK, 600)]))
        b.append(arrow(418, y + 21, 560, y + 21, color=BLUE))
        b.append(hs_box(570, y, 400, 42, les, fill=LIGHT, stroke=BLUE, hcol=BLUE))
    b.append(note16(30, 438, 940, "Spätere Aufträge sagen „laut README.md“, deshalb passen sie zu jedem Vorhaben."))
    return save(f"{L3}/readme-fuenf-abschnitte.svg", svg(W, H, b))


FIGS = [fig_was_in_den_ordner_darf, fig_interview_vorschlag_freigabe, fig_readme_fuenf_abschnitte,
        fig_projektordner_arbeitsplatz, fig_dateiname_aufbau, fig_zwei_sitzungen,
        fig_hausordnung_aufbau, fig_eine_hausordnung, fig_annahme_statt_erfinden, fig_geltungsbereich,
        fig_ablageplan, fig_kontext_drei_teile]

if __name__ == "__main__":
    for fn in FIGS:
        print(fn())

"""Lehrbilder für Kapitel 6 „PDFs als Quellen“, 6b „Excel-Tabellen als Quelle“,
7 „Laufend neue Dateien“ und 8 „Skills: Abläufe, die bleiben“.

Je Erklärseite ein Bild (16 Stück). Schriften mindestens 16 px, Titel 20 px,
Farben nur aus figlib, Grün/Rot kommt nicht vor (keine Richtig/Falsch-Bilder).

Run: python3 scripts/build_figs_l06_l08.py
Ausgabe: agent-arbeitsumgebung/images/lektionen/l06-pdf-als-quelle/, l06b-excel-als-quelle/,
l07-laufend-neue-dateien/, l08-skills/
"""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from figlib import *  # noqa: E402,F403
from figlib import AMBER, AMBER_BG, AMBER_LINE, BLUE, INK, LIGHT, MUTED, PAPER, RULE  # noqa: E402

L6 = "l06-pdf-als-quelle"
L6B = "l06b-excel-als-quelle"
L7 = "l07-laufend-neue-dateien"
L8 = "l08-skills"
MONO = 'font-family="ui-monospace, Menlo, monospace"'
MONO_W = 0.602


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
    heads = wrap_px(head, w - 24, hsize, hweight)
    subs = []
    if sub:
        for part in (sub if isinstance(sub, list) else [sub]):
            subs += wrap_px(part, w - 24, 16)
    block = len(heads) * (hsize + 5) - 5 + len(subs) * lh
    top = y + (h - block) / 2 + hsize * 0.8
    for i, ln in enumerate(heads):
        out += T(x + w / 2, top + i * (hsize + 5), ln, hsize, hweight, hcol, "middle")
    base = top + (len(heads) - 1) * (hsize + 5)
    for i, ln in enumerate(subs):
        out += T(x + w / 2, base + (i + 1) * lh + 1, ln, 16, 400, scol, "middle")
    return out


def pill16(x, y, label, fill=LIGHT, stroke=BLUE, tcol=BLUE, mono=False, size=16):
    w = (len(label) * size * MONO_W if mono else text_width(label, size, 600)) + 22
    h = size + 12
    return (box(x, y, w, h, fill, stroke, h / 2, 1.2)
            + text(x + w / 2, y + size + 2, label, size, 600 if not mono else 700, tcol, "middle", mono)), w


def badge16(cx, cy, label, r=16, fill=BLUE):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>' + T(cx, cy + 6, label, 16, 700, "#ffffff", "middle")


def note16(x, y, w, s):
    return box(x, y, w, 44, PAPER, PAPER, 8) + T(x + 18, y + 28, s, 16, 400, INK)


def mono_rich(x, y, parts, size=16, anchor="start"):
    spans = "".join(f'<tspan fill="{c}" font-weight="{wt}">{escape(s)}</tspan>' for s, c, wt in parts)
    return f'<text x="{x}" y="{y}" {MONO} font-size="{size}" text-anchor="{anchor}" xml:space="preserve">{spans}</text>'


def M(x, y, s, size=16, fill=INK, weight=400, anchor="start"):
    return mono_rich(x, y, [(s, fill, weight)], size, anchor)


def hline(x1, x2, y, col=RULE, sw=1):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="{sw}"/>'


def vline(x, y1, y2, col=RULE, sw=1):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{col}" stroke-width="{sw}"/>'


def bracket(x1, x2, y, label, col=BLUE):
    """Klammer unter einem Textstück mit Beschriftung darunter."""
    return (f'<path d="M{x1},{y} L{x1},{y + 8} L{x2},{y + 8} L{x2},{y}" stroke="{col}" stroke-width="2" fill="none"/>'
            + vline((x1 + x2) / 2, y + 8, y + 18, col, 2))


def folder(x, y, w, h, label, fill="#ffffff", stroke=RULE, tcol=INK, weight=600, mono=True):
    """Ordnersymbol mit Reiter und Beschriftung."""
    tab = f'<path d="M{x},{y + 10} L{x},{y} L{x + w * 0.38},{y} L{x + w * 0.46},{y + 10} Z" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    body = box(x, y + 10, w, h - 10, fill, stroke, 6)
    return tab + body + text(x + w / 2, y + 10 + (h - 10) / 2 + 6, label, 16, weight, tcol, "middle", mono)


# ================================================================ Lektion 6: PDFs als Quellen

def fig_pdf_fuer_den_druck():
    W, H = 1000, 470
    b = [heading(500, "Was wir auf der Seite sehen, was das PDF speichert")]
    # links: Tabelle
    lx, ly, lw, lh = 30, 64, 455, 300
    b.append(box(lx, ly, lw, lh, "#ffffff", RULE, 12))
    b.append(T(lx + 20, ly + 34, "Auf der Seite: eine Tabelle", 17, 700))
    cols = [lx + 20, lx + 230, lx + 345]
    rows = [("Leistung", "Einheit", "Preis"), ("Kleine Reparatur", "pauschal", "45,00"),
            ("Beratung vor Ort", "je Termin", "89,00"), ("Anfahrt", "je km", "1,20")]
    ty = ly + 84
    for i, r in enumerate(rows):
        y = ty + i * 50
        if i == 0:
            b.append(box(lx + 12, y - 26, lw - 24, 40, PAPER, PAPER, 6))
        for c, s in zip(cols, r):
            b.append(T(c, y, s, 16, 600 if i == 0 else 400))
        if i:
            b.append(hline(lx + 12, lx + lw - 12, y - 30))
    b.append(T(lx + 20, ly + lh - 22, "Wir lesen Zeilen und Spalten.", 16, 400, MUTED))
    # rechts: Zeichen mit Position
    rx, rw = 515, 455
    b.append(box(rx, ly, rw, lh, LIGHT, BLUE, 12))
    b.append(T(rx + 20, ly + 34, "Im PDF gespeichert: Wörter mit Position", 17, 700, BLUE))
    chips = [("Kleine", 140), ("45,00", 410), ("Reparatur", 196), ("Anfahrt", 140),
             ("89,00", 410), ("je Termin", 300), ("1,20", 418), ("Beratung", 140)]
    for i, (s, pos) in enumerate(chips):
        cx = rx + 20 + (i % 2) * 218
        cy = ly + 64 + (i // 2) * 48
        lab = f"„{s}“ bei {pos}"
        b.append(box(cx, cy, 200, 34, "#ffffff", RULE, 6))
        b.append(T(cx + 12, cy + 23, lab, 16, 400))
    b.append(T(rx + 20, ly + lh - 22, "keine Angabe, was eine Zeile bildet", 16, 400, MUTED))
    b.append(note16(30, 392, 940, "Das PDF kennt Positionen, keine Tabellenzeilen. Darum prüfen wir die Umwandlung."))
    return save(f"{L6}/pdf-fuer-den-druck.svg", svg(W, H, b))


def mini_page(x, y, w, h, scanned=False):
    out = box(x, y, w, h, PAPER if scanned else "#ffffff", RULE, 6)
    for i in range(5):
        lw = w - 36 - (i % 2) * 30
        yy = y + 24 + i * 20
        if scanned:
            out += f'<rect x="{x + 18}" y="{yy - 5}" width="{lw}" height="8" rx="3" fill="{RULE}"/>'
        else:
            out += f'<rect x="{x + 18}" y="{yy - 5}" width="{lw}" height="8" rx="3" fill="{MUTED}" opacity=".55"/>'
    return out


def fig_textebene():
    W, H = 1000, 420
    b = [heading(500, "Lässt sich eine Zeile markieren?")]
    rows = [(70, False), (240, True)]
    for y, scanned in rows:
        b.append(box(30, y, 940, 150, "#ffffff" if not scanned else "#ffffff", RULE, 12))
        b.append(T(54, y + 34, "Gescanntes PDF" if scanned else "PDF mit Textebene", 17, 700, INK if scanned else BLUE))
        b.append(T(54, y + 60, "nur ein Bild der Seite" if scanned else "Text hinter dem Seitenbild", 16, 400, MUTED))
        px = 340
        b.append(mini_page(px, y + 18, 170, 116, scanned))
        if not scanned:
            b.append(f'<rect x="{px + 12}" y="{y + 18 + 24 + 20 - 11}" width="146" height="20" rx="3" fill="{BLUE}" opacity=".25"/>')
        b.append(T(560, y + 62, "Zeile markieren:", 16, 600))
        b.append(T(560, y + 88, "nichts wird markiert" if scanned else "Zeile wird farbig", 16, 400, MUTED))
        b.append(arrow(722, y + 75, 762, y + 75))
        b.append(hs_box(770, y + 30, 180, 90, "Textfassung", "leer oder falsch" if scanned else "vollständig",
                        AMBER_BG if scanned else LIGHT, AMBER_LINE if scanned else BLUE))
    b.append(pill16(54, 240 + 96, "zuerst Texterkennung (OCR)", AMBER_BG, AMBER_LINE, INK)[0])
    return save(f"{L6}/textebene.svg", svg(W, H, b))


def fig_original_textfassung():
    W, H = 1000, 420
    b = [heading(500, "Original und Textfassung")]
    cy, ch, cw = 70, 160, 330
    b.append(box(30, cy, cw, ch, "#ffffff", RULE, 12))
    b.append(glyph("doc", 66, cy + 44))
    b.append(T(96, cy + 40, "Original", 18, 700))
    b.append(T(96, cy + 62, "Beleg, niemand ändert es", 16, 400, MUTED))
    b.append(M(50, cy + 114, "quellen/original/", 16, MUTED))
    b.append(M(50, cy + 138, "preisliste-2026.pdf", 16, INK, 700))
    rx = 1000 - 30 - cw
    b.append(box(rx, cy, cw, ch, LIGHT, BLUE, 12))
    b.append(glyph("doc", rx + 36, cy + 44, BLUE))
    b.append(T(rx + 66, cy + 40, "Textfassung", 18, 700, BLUE))
    b.append(T(rx + 66, cy + 62, "damit arbeitet der Agent", 16, 400, MUTED))
    b.append(M(rx + 20, cy + 114, "quellen/text/", 16, MUTED))
    b.append(M(rx + 20, cy + 138, "preisliste-2026.md", 16, INK, 700))
    b.append(arrow(30 + cw + 8, cy + 80, rx - 8, cy + 80, color=BLUE))
    b.append(T(500, cy + 62, "Umwandlung", 16, 600, BLUE, "middle"))
    b.append(T(500, cy + 108, "durch den Agenten", 16, 400, MUTED, "middle"))
    b.append(T(500, 284, "Hier entstehen die meisten Fehler:", 16, 600, INK, "middle"))
    items = ["Tabellen", "Fußnoten", "zwei Textspalten"]
    xs = [180, 400, 620]
    for x, s in zip(xs, items):
        b.append(hs_box(x, 302, 200, 46, s, fill=AMBER_BG, stroke=AMBER_LINE, hweight=600))
    b.append(note16(30, 366, 940, "Gleicher Name vor der Endung: So gehören die beiden Dateien sichtbar zusammen."))
    return save(f"{L6}/original-und-textfassung.svg", svg(W, H, b))


def fig_stichprobe_vier_augen():
    W, H = 1000, 470
    b = [heading(500, "Stichprobe mit vier Augen")]
    b.append(box(30, 64, 440, 120, "#ffffff", RULE, 12))
    b.append(glyph("agent", 70, 104))
    b.append(T(104, 100, "Agent überträgt", 18, 700))
    b.append(multiline(104, 126, "Original in Textfassung, nennt Fundstellen", 340, 16, 400, MUTED))
    b.append(box(530, 64, 440, 120, LIGHT, BLUE, 12))
    b.append(glyph("person", 570, 108, BLUE))
    b.append(T(604, 100, "Wir lesen gegen", 18, 700, BLUE))
    b.append(multiline(604, 126, "an den genannten Stellen im Original", 340, 16, 400, MUTED))
    b.append(arrow(474, 124, 526, 124, color=BLUE))
    b.append(T(500, 228, "Drei Prüfstellen", 16, 600, INK, "middle"))
    items = [("Eine Tabelle", "Zeilen vollständig?"), ("Zwei Zahlen", "identisch?"), ("Eine Überschrift", "Reihenfolge erhalten?")]
    for i, (h, s) in enumerate(items):
        x = 30 + i * 320
        b.append(box(x, 246, 300, 110, "#ffffff", RULE, 12))
        b.append(badge16(x + 34, 301, str(i + 1)))
        b.append(T(x + 64, 294, h, 17, 700))
        b.append(T(x + 64, 320, s, 16, 400, MUTED))
    b.append(note16(30, 392, 940, "Drei Stellen statt des ganzen Dokuments."))
    return save(f"{L6}/stichprobe-vier-augen.svg", svg(W, H, b))


def fig_quellenliste_regel2():
    W, H = 1000, 410
    b = [heading(500, "Regel 2, Quellenliste, Antwort")]
    cw, ch, cy = 290, 260, 66
    xs = [30, 355, 680]
    # 1 Regel 2
    b.append(box(xs[0], cy, cw, ch, "#ffffff", RULE, 12))
    b.append(badge16(xs[0] + 30, cy + 32, "1"))
    b.append(T(xs[0] + 56, cy + 38, "Regel 2 der AGENTS.md", 17, 700))
    b.append(multiline(xs[0] + 20, cy + 80, "Fakten nur aus Dateien in diesem Ordner", cw - 40, 16, 400, MUTED))
    b.append(pill16(xs[0] + 20, cy + ch - 34, "woher Fakten kommen", PAPER, RULE, INK)[0])
    # 2 Quellenliste
    x = xs[1]
    b.append(box(x, cy, cw, ch, LIGHT, BLUE, 12))
    b.append(badge16(x + 30, cy + 32, "2"))
    b.append(T(x + 56, cy + 38, "Quellenliste", 17, 700, BLUE))
    b.append(M(x + 20, cy + 70, "quellen/QUELLEN.md", 16, MUTED))
    b.append(multiline(x + 20, cy + 104, "„Nur Dateien mit Prüfvermerk gelten als Quelle.“", cw - 40, 16, 600, INK))
    b.append(box(x + 20, cy + 172, cw - 40, 34, "#ffffff", RULE, 6))
    b.append(T(x + 32, cy + 195, "Preisliste: geprüft", 16, 400))
    b.append(pill16(x + 20, cy + ch - 34, "wem wir trauen", "#ffffff")[0])
    # 3 Antwort
    x = xs[2]
    b.append(box(x, cy, cw, ch, "#ffffff", RULE, 12))
    b.append(badge16(x + 30, cy + 32, "3"))
    b.append(T(x + 56, cy + 38, "Antwort im Chat", 17, 700))
    b.append(box(x + 20, cy + 64, cw - 40, 142, PAPER, RULE, 10))
    b.append(T(x + 34, cy + 94, "Kleine Reparatur:", 16, 400))
    b.append(T(x + 34, cy + 118, "45,00 EUR", 16, 600))
    b.append(T(x + 34, cy + 160, "Quelle:", 16, 400, MUTED))
    b.append(M(x + 34, cy + 186, "preisliste-2026.md", 16, INK, 700))
    b.append(pill16(x + 20, cy + ch - 34, "nachprüfbar", PAPER, RULE, INK)[0])
    for i in range(2):
        b.append(arrow(xs[i] + cw + 4, cy + ch / 2, xs[i + 1] - 4, cy + ch / 2, color=BLUE))
    b.append(note16(30, 346, 940, "Regel 2 sagt, woher Fakten kommen. Die Quellenliste sagt, welchen Dateien wir trauen."))
    return save(f"{L6}/quellenliste-und-regel-2.svg", svg(W, H, b))


# ================================================================ Lektion 6b: Excel-Tabellen als Quelle

def fig_excel_paket():
    W, H = 1000, 412
    b = [heading(500, "Eine Excel-Datei: ein Paket, Formeln und Werte")]
    # Paket
    px, py, pw, ph = 30, 66, 440, 250
    b.append(box(px, py, pw, ph, "#ffffff", RULE, 12))
    b.append(T(px + 24, py + 32, "Paket", 17, 700))
    b.append(M(px + 90, py + 32, "auftragsliste-2026.xlsx", 16, INK, 700))
    for i, s in enumerate(["Blätter", "Zellen", "Formeln", "Formate"]):
        x = px + 24 + (i % 2) * 200
        y = py + 56 + (i // 2) * 62
        b.append(hs_box(x, y, 192, 50, s, fill=PAPER, hweight=500))
    b.append(multiline(px + 24, py + 216, "Text liest der Agent direkt, das Paket nur mit einem Werkzeug.", pw - 48, 16, 400, MUTED))
    # Zelle G5
    rx = 530
    b.append(T(rx, 96, "Zelle G5, was wir sehen", 16, 600))
    b.append(box(rx, 108, 200, 52, "#ffffff", BLUE, 4, 2))
    b.append(T(rx + 186, 142, "45,00", 18, 600, INK, "end"))
    b.append(T(rx, 206, "Zelle G5, was gespeichert ist", 16, 600))
    b.append(box(rx, 218, 200, 52, LIGHT, BLUE, 4, 2))
    b.append(M(rx + 16, 252, "=D5*F5", 18, BLUE, 700))
    b.append(multiline(rx + 230, 132, "Das Tabellenprogramm rechnet beim Öffnen.", 210, 16, 400, MUTED))
    b.append(multiline(rx + 230, 242, "Die Formelzeile zeigt den Unterschied.", 210, 16, 600, BLUE))
    b.append(note16(30, 340, 940, "Wert und Formel sehen in der Zelle gleich aus: als Zahl."))
    return save(f"{L6B}/excel-paket-formel-wert.svg", svg(W, H, b))


def fig_blatt_wird_csv():
    W, H = 1000, 470
    b = [heading(500, "Aus einem Tabellenblatt wird eine CSV")]
    # links: Blatt
    lx, ly, lw = 30, 64, 410
    b.append(T(lx, ly + 18, "Blatt Aufträge im Tabellenprogramm", 16, 600))
    gy = ly + 34
    rh = 40
    rows = [("1", "Aufträge Juli bis September", True), ("2", "Beträge in EUR", True), ("3", "", True),
            ("4", None, False), ("5", None, False)]
    nw = 40
    for i, (n, s, weg) in enumerate(rows):
        y = gy + i * rh
        b.append(f'<rect x="{lx}" y="{y}" width="{nw}" height="{rh}" fill="{PAPER}" stroke="{RULE}"/>')
        b.append(T(lx + nw / 2, y + 26, n, 16, 600, MUTED, "middle"))
        b.append(f'<rect x="{lx + nw}" y="{y}" width="{lw - nw}" height="{rh}" fill="#ffffff" stroke="{RULE}"/>')
        if s is not None:
            b.append(T(lx + nw + 12, y + 26, s, 16, 600 if i == 0 else 400, MUTED if weg else INK))
    # Zeile 4 und 5: Zellen
    cells4 = ["Nr.", "Datum", "…", "Betrag"]
    cells5 = ["1", "03.07.2026", "…", "=D5*F5"]
    cws = [60, 140, 50, 120]
    for ri, cells in ((3, cells4), (4, cells5)):
        x = lx + nw
        y = gy + ri * rh
        for c, cw_ in zip(cells, cws):
            b.append(f'<rect x="{x}" y="{y}" width="{cw_}" height="{rh}" fill="{PAPER if ri == 3 else "#ffffff"}" stroke="{RULE}"/>')
            if c == "=D5*F5":
                b.append(M(x + 10, y + 26, c, 16, BLUE, 700))
            else:
                b.append(T(x + 10, y + 26, c, 16, 600 if ri == 3 else 400))
            x += cw_
    b.append(f'<rect x="{lx + nw + 2}" y="{gy + 2}" width="{lw - nw - 4}" height="{3 * rh - 4}" fill="{AMBER_BG}" opacity=".6"/>')
    b.append(T(lx + nw + 12, gy + 26, "Aufträge Juli bis September", 16, 600, MUTED))
    b.append(T(lx + nw + 12, gy + rh + 26, "Beträge in EUR", 16, 400, MUTED))
    b.append(T(lx + lw - 12, gy + 2 * rh + 26, "fällt weg", 16, 600, AMBER, "end"))
    # Pfeil
    b.append(path_arrow(f"M{lx + lw + 6},{gy + 4 * rh} C{lx + lw + 60},{gy + 4 * rh} {lx + lw + 40},{gy + 55} {lx + lw + 92},{gy + 55}", BLUE))
    b.append(T(lx + lw + 52, gy + 32, "Umwandlung", 16, 600, BLUE, "middle"))
    # rechts: CSV
    rx, rw = 560, 410
    b.append(T(rx, ly + 18, "CSV-Datei (Text)", 16, 600))
    b.append(box(rx, gy, rw, 2 * rh + 30, LIGHT, BLUE, 8))
    l1 = [("Nr.", INK, 700), (";", BLUE, 700), ("Datum", INK, 700), (";", BLUE, 700), ("…", INK, 700), (";", BLUE, 700), ("Betrag", INK, 700)]
    l2 = [("1", INK, 400), (";", BLUE, 700), ("2026-07-03", INK, 400), (";", BLUE, 700), ("…", INK, 400), (";", BLUE, 700), ("45,00", INK, 400)]
    b.append(mono_rich(rx + 16, gy + 38, l1))
    b.append(mono_rich(rx + 16, gy + 78, l2))
    notes = [("Zeile 1", "ist die Spaltenüberschrift"), ("45,00", "Wert statt Formel"),
             ("2026-07-03", "Datum als JJJJ-MM-TT"), (";", "Semikolon trennt die Spalten")]
    for i, (k, v) in enumerate(notes):
        y = gy + 2 * rh + 70 + i * 40
        b.append(pill16(rx, y - 20, k, "#ffffff", BLUE, BLUE, mono=(k != "Zeile 1"))[0])
        kw = (len(k) * 16 * MONO_W if k != "Zeile 1" else text_width(k, 16, 600)) + 22
        b.append(T(rx + kw + 12, y, v, 16, 400, INK))
    b.append(note16(30, 398, 940, "Eine CSV fasst ein Blatt. Darum entsteht je Blatt eine eigene Datei."))
    return save(f"{L6B}/blatt-wird-csv.svg", svg(W, H, b))


def fig_stichprobe_tabellen():
    W, H = 1000, 440
    b = [heading(500, "Drei Prüfstellen, drei Fallen")]
    b.append(T(86, 78, "Prüfstelle", 16, 600, MUTED))
    b.append(T(620, 78, "deckt auf", 16, 600, MUTED))
    rows = [("Datenzeilen je Blatt zählen", "ein fehlendes Blatt oder eine fehlende Zeile"),
            ("Ein Datum vergleichen", "falsche Umrechnung, etwa 46206 statt 2026-07-03"),
            ("Einen Wert aus einer Formelzelle vergleichen", "Formeln statt Werte")]
    for i, (a, t) in enumerate(rows):
        y = 94 + i * 92
        b.append(badge16(52, y + 37, str(i + 1)))
        b.append(hs_box(86, y, 470, 74, a, hweight=600))
        b.append(arrow(564, y + 37, 606, y + 37))
        b.append(hs_box(614, y, 356, 74, t, fill=AMBER_BG, stroke=AMBER_LINE, hweight=500))
    b.append(note16(30, 376, 940, "Zeile und Spalte beziehen sich auf das Original im Tabellenprogramm."))
    return save(f"{L6B}/stichprobe-tabellen.svg", svg(W, H, b))


def fig_regel_und_pruefung():
    W, H = 1000, 450
    b = [heading(500, "Regel plus Prüfung")]
    b.append(box(30, 62, 940, 120, "#ffffff", RULE, 12))
    b.append(T(54, 96, "Regel", 18, 700))
    b.append(T(54, 124, "Regel 4 der AGENTS.md:", 16, 600))
    b.append(T(54, 150, "Ergebnisse als neue Datei, bestehende Dateien nur nach Rückfrage", 16, 400, MUTED))
    b.append(pill16(690, 82, "senkt das Risiko, meist", PAPER, RULE, INK)[0])
    b.append(arrow(500, 186, 500, 214))
    b.append(box(30, 218, 940, 150, LIGHT, BLUE, 12))
    b.append(T(54, 252, "Prüfung nach jedem Auftrag in quellen/", 18, 700, BLUE))
    b.append(hs_box(54, 270, 430, 80, "Änderungsdatum des Originals", "im Chat erfragen"))
    b.append(hs_box(516, 270, 430, 80, "Eine Summe", "selbst nachrechnen"))
    b.append(note16(30, 388, 940, "Regel plus Prüfung, keine Garantie."))
    return save(f"{L6B}/regel-und-pruefung.svg", svg(W, H, b))


def fig_auswertung_neue_datei():
    W, H = 1000, 456
    b = [heading(500, "Eine Auswertung entsteht als neue Datei")]
    # geprüfte CSV
    b.append(box(30, 66, 360, 140, "#ffffff", RULE, 12))
    b.append(T(50, 98, "Geprüfte Quelle", 17, 700))
    b.append(M(50, 128, "quellen/text/", 16, MUTED))
    b.append(M(50, 152, "auftragsliste-2026-auftraege.csv", 15.5, INK, 700))
    b.append(pill16(50, 166, "Prüfvermerk", LIGHT)[0])
    # neue Datei
    b.append(box(560, 66, 410, 140, LIGHT, BLUE, 12))
    b.append(T(580, 98, "Neue Datei", 17, 700, BLUE))
    b.append(M(580, 128, "auswertungen/2026-q3-leistungen.csv", 15.5, INK, 700))
    b.append(box(580, 146, 370, 40, "#ffffff", RULE, 6))
    b.append(T(594, 172, "Kleine Reparatur: 3 Aufträge, 135,00", 16, 400))
    b.append(arrow(396, 136, 552, 136, color=BLUE))
    b.append(T(474, 124, "Agent rechnet", 16, 600, BLUE, "middle"))
    # Nachrechnung
    b.append(box(560, 236, 410, 84, PAPER, RULE, 12))
    b.append(T(580, 268, "Wir rechnen nach:", 16, 600))
    b.append(T(580, 296, "3 mal 45,00 ergibt 135,00", 16, 400))
    b.append(arrow(765, 210, 765, 232))
    # Original
    b.append(box(30, 236, 360, 136, "#ffffff", RULE, 12, dash="6 5"))
    b.append(T(50, 268, "Original", 17, 700))
    b.append(M(50, 296, "quellen/original/", 16, MUTED))
    b.append(M(50, 320, "auftragsliste-2026.xlsx", 16, INK, 700))
    b.append(pill16(50, 334, "bleibt unberührt", "#ffffff", RULE, INK)[0])
    b.append(note16(30, 392, 940, "Die Quellen in quellen/ bleiben, wie sie sind. Ergebnisse kommen in auswertungen/."))
    return save(f"{L6B}/auswertung-als-neue-datei.svg", svg(W, H, b))


# ================================================================ Lektion 7: Laufend neue Dateien

def fig_eingangsordner():
    W, H = 1000, 430
    b = [heading(500, "Der Eingangsordner als Postfach")]
    srcs = [("mail", "weitergeleitete E-Mail"), ("doc", "Export aus dem Kontaktformular"), ("doc", "PDF vom Lieferanten")]
    for i, (g, s) in enumerate(srcs):
        y = 70 + i * 96
        b.append(box(30, y, 290, 70, "#ffffff", RULE, 10))
        b.append(glyph(g, 66, y + 35))
        b.append(multiline(100, y + 30 if len(wrap_px(s, 200, 16)) > 1 else y + 41, s, 200, 16, 400))
        b.append(arrow(324, y + 35, 392, 205 + (i - 1) * 30))
    # eingang
    b.append(box(400, 120, 250, 170, LIGHT, BLUE, 12))
    b.append(folder(460, 136, 130, 56, "eingang/", "#ffffff", BLUE, BLUE, 700))
    b.append(T(525, 222, "Postfach:", 16, 700, BLUE, "middle"))
    b.append(T(525, 246, "alles Neue zuerst hierher", 16, 400, INK, "middle"))
    b.append(T(525, 270, "Namen und Format beliebig", 16, 400, MUTED, "middle"))
    # sortiert
    b.append(box(700, 70, 270, 262, "#ffffff", RULE, 12))
    b.append(T(835, 100, "sortiert", 17, 700, INK, "middle"))
    for i, s in enumerate(["anfragen/", "antworten/", "quellen/original/"]):
        b.append(folder(730, 120 + i * 66, 210, 52, s))
    b.append(note16(30, 362, 940, "Neue Dateien landen nur an einem Ort. Alles andere im Projektordner ist sortiert."))
    return save(f"{L7}/eingangsordner.svg", svg(W, H, b))


def fig_fester_ablauf_name():
    W, H = 1000, 520
    b = [heading(500, "Der Weg einer Datei und ihr neuer Name")]
    # Zeile oben
    y = 70
    b.append(box(30, y, 210, 96, "#ffffff", RULE, 10))
    b.append(T(135, y + 30, "in eingang/", 16, 400, MUTED, "middle"))
    b.append(M(135, y + 62, "Mail Mustermann.txt", 15, INK, 700, "middle"))
    b.append(arrow(246, y + 48, 300, y + 48, color=BLUE))
    b.append(T(273, y + 120, "fester Ablauf", 16, 600, BLUE, "middle"))
    # Plan
    px, pw = 306, 330
    b.append(box(px, y, pw, 96, AMBER_BG, AMBER_LINE, 10))
    b.append(T(px + 16, y + 26, "Plan vor dem Verschieben", 16, 600))
    for j, h in enumerate(["alt", "neu", "Ziel"]):
        b.append(box(px + 16 + j * 100, y + 40, 96, 40, "#ffffff", RULE, 4))
        b.append(T(px + 64 + j * 100, y + 66, h, 16, 600, INK, "middle"))
    b.append(arrow(px + pw + 6, y + 48, px + pw + 52, y + 48, color=BLUE))
    b.append(T(px + pw + 29, y + 120, "Freigabe", 16, 600, BLUE, "middle"))
    # Ergebnis
    rx = 696
    b.append(box(rx, y, 274, 96, LIGHT, BLUE, 10))
    b.append(T(rx + 137, y + 30, "anfragen/", 16, 400, MUTED, "middle"))
    b.append(M(rx + 137, y + 60, "2026-10-16-rueckruf.md", 15, INK, 700, "middle"))
    b.append(pill16(rx + 44, y + 104, "„Kundin“ statt Name", "#ffffff")[0])
    # Name zerlegt
    b.append(T(500, 270, "Der neue Name in Teilen", 17, 700, INK, "middle"))
    parts = [("2026-10-16", BLUE), ("-", MUTED), ("rueckruf", INK), (".md", MUTED)]
    size = 30
    cw = size * MONO_W
    total = sum(len(s) for s, _ in parts) * cw
    x0 = 500 - total / 2
    b.append(mono_rich(x0, 326, [(s, c, 700) for s, c in parts], size))
    xs = []
    x = x0
    for s, _ in parts:
        xs.append((x, x + len(s) * cw))
        x += len(s) * cw
    labels = [(0, "Datum des Eingangs", "aus der Datei"), (2, "Anliegen", "ein Wort"), (3, "Endung", "bleibt")]
    for idx, l1, l2 in labels:
        a, e = xs[idx]
        b.append(bracket(a + 2, e - 2, 338, ""))
        b.append(T((a + e) / 2, 380, l1, 16, 600, BLUE, "middle"))
        b.append(T((a + e) / 2, 402, l2, 16, 400, MUTED, "middle"))
    b.append(note16(30, 446, 940, "Datum des Eingangs, nicht des Einsortierens."))
    return save(f"{L7}/fester-ablauf-und-name.svg", svg(W, H, b))


def fig_sechs_schritte():
    W, H = 1000, 446
    b = [heading(500, "Der feste Ablauf in sechs Schritten")]
    steps = ["Lesen", "Art bestimmen", "Umbenennen", "Namen entfernen", "Verschieben", "Übersicht ergänzen"]
    bw, gap, y, bh = 134, 27.2, 130, 96
    xs = [30 + i * (bw + gap) for i in range(6)]
    groups = [(0, 0, "lesen"), (1, 1, "entscheiden"), (2, 4, "handeln"), (5, 5, "dokumentieren")]
    for a, e, lab in groups:
        x1, x2 = xs[a], xs[e] + bw
        b.append(f'<path d="M{x1 + 4},{y - 14} L{x1 + 4},{y - 22} L{x2 - 4},{y - 22} L{x2 - 4},{y - 14}" stroke="{BLUE}" stroke-width="2" fill="none"/>')
        b.append(T((x1 + x2) / 2, y - 32, lab, 16, 600, BLUE, "middle"))
    for i, (x, s) in enumerate(zip(xs, steps)):
        b.append(box(x, y, bw, bh, LIGHT if i == 4 else "#ffffff", BLUE if i == 4 else RULE, 10))
        b.append(badge16(x + bw / 2, y + 24, str(i + 1), r=14))
        ls = wrap_px(s, bw - 16, 16, 600)
        for j, ln in enumerate(ls):
            b.append(T(x + bw / 2, y + 62 + j * 20 - (len(ls) - 1) * 6, ln, 16, 600, INK, "middle"))
        if i < 5:
            b.append(arrow(x + bw + 2, y + bh / 2, x + bw + gap - 2, y + bh / 2))
    # Hinweis vor 5
    x5 = xs[4]
    px, py = xs[2] + 20, y + bh + 44
    b.append(box(px, py, 250, 56, AMBER_BG, AMBER_LINE, 10))
    b.append(T(px + 125, py + 22, "Plan als Tabelle,", 16, 600, INK, "middle"))
    b.append(T(px + 125, py + 44, "dann Freigabe", 16, 600, INK, "middle"))
    b.append(arrow(px + 250 + 4, py + 10, x5 + 24, y + bh + 6))
    # Abzweig unklar
    ux, uy = 800, y + bh + 44
    bx_ = x5 + bw / 2 + 14
    b.append(path_arrow(f"M{bx_},{y + bh + 2} L{bx_},{uy + 40} L{ux - 4},{uy + 40}"))
    b.append(box(ux, uy, 170, 84, "#ffffff", RULE, 10))
    b.append(T(ux + 12, uy + 26, "unklar:", 16, 700))
    b.append(T(ux + 12, uy + 48, "bleibt in eingang/,", 16, 400, MUTED))
    b.append(T(ux + 12, uy + 70, "Meldung im Chat", 16, 400, MUTED))
    b.append(note16(30, 384, 940, "Leerer Eingang: alles einsortiert, noch nichts beantwortet."))
    return save(f"{L7}/sechs-schritte.svg", svg(W, H, b))


# ================================================================ Lektion 8: Skills

def shelf(x, y, w, h, n=3, pulled=None, labels=None):
    out = box(x, y, w, h, PAPER, RULE, 8)
    out += hline(x + 8, x + w - 8, y + h - 12, MUTED, 3)
    bw = 34
    for i in range(n):
        bx = x + 24 + i * (bw + 14)
        if pulled == i:
            continue
        out += box(bx, y + 20, bw, h - 36, "#ffffff", RULE, 4)
        out += hline(bx + 8, bx + bw - 8, y + 44, MUTED, 2)
    return out


def fig_skill_aufbau():
    W, H = 1000, 500
    b = [heading(500, "Ein Skill: Ordner mit der Datei SKILL.md")]
    # Regal links
    b.append(shelf(30, 70, 190, 170, 3, pulled=2))
    b.append(box(140, 98, 240, 120, LIGHT, BLUE, 8))
    b.append(folder(160, 112, 200, 52, "eingang-einsortieren", "#ffffff", BLUE, BLUE, 700))
    b.append(T(260, 196, "Skill-Ordner", 16, 600, BLUE, "middle"))
    b.append(T(130, 278, "Arbeitsanweisung", 16, 600, INK, "middle"))
    b.append(T(130, 300, "im Regal", 16, 600, INK, "middle"))
    b.append(arrow(384, 158, 436, 158, color=BLUE))
    # SKILL.md
    fx, fw = 444, 526
    b.append(box(fx, 66, fw, 340, "#ffffff", RULE, 10))
    b.append(T(fx + 18, 94, "SKILL.md", 16, 700))
    b.append(box(fx + 12, 106, fw - 24, 132, LIGHT, LIGHT, 8))
    lines_ = [("---", BLUE, 700), None, None, ("---", BLUE, 700)]
    b.append(M(fx + 26, 132, "---", 16, BLUE, 700))
    b.append(mono_rich(fx + 26, 160, [("name: ", INK, 700), ("eingang-einsortieren", INK, 400)]))
    b.append(mono_rich(fx + 26, 186, [("description: ", INK, 700), ("Verwenden, wenn", INK, 400)]))
    b.append(M(fx + 26, 208, "Dateien in eingang/ einsortiert …", 16, INK))
    b.append(M(fx + 26, 230, "---", 16, BLUE, 700))
    for j, s in enumerate(["1. Lies jede Datei …", "2. Bestimme die Art …", "…", "6. Ergänze UEBERSICHT.md."]):
        b.append(M(fx + 26, 274 + j * 28, s, 16, INK))
    b.append(pill16(fx + fw - 236, 112, "sagt, wann er gilt")[0])
    b.append(pill16(fx + fw - 236, 252, "sagt, was zu tun ist", PAPER, RULE, INK)[0])
    b.append(note16(30, 428, 940, "Der Ordnername ist gleich dem name im Kopf: eingang-einsortieren."))
    return save(f"{L8}/skill-aufbau.svg", svg(W, H, b))


def fig_laden_in_stufen():
    W, H = 1000, 470
    b = [heading(500, "Laden in Stufen")]
    cw, ch, cy = 290, 290, 66
    xs = [30, 355, 680]
    heads = [("1", "Beginn der Sitzung"), ("2", "Ein Auftrag passt"), ("3", "Nur bei Bedarf")]
    fills = ["#ffffff", LIGHT, "#ffffff"]
    strokes = [RULE, BLUE, RULE]
    for (n, h), x, fl, st in zip(heads, xs, fills, strokes):
        b.append(box(x, cy, cw, ch, fl, st, 12))
        b.append(badge16(x + 30, cy + 32, n))
        b.append(T(x + 56, cy + 38, h, 17, 700, BLUE if fl == LIGHT else INK))
    # 1
    x = xs[0]
    b.append(multiline(x + 20, cy + 76, "Der Agent kennt von jedem Skill nur name und description.", cw - 40, 16, 400, MUTED))
    for j, s in enumerate(["eingang-einsortieren", "wochenbericht", "angebot-erstellen"]):
        b.append(box(x + 20, cy + 140 + j * 44, cw - 40, 34, PAPER, RULE, 6))
        b.append(M(x + 32, cy + 163 + j * 44, s, 15, INK))
    # 2
    x = xs[1]
    b.append(box(x + 20, cy + 64, cw - 40, 40, "#ffffff", RULE, 8))
    b.append(T(x + 34, cy + 90, "„Eingang einsortieren.“", 16, 600))
    b.append(T(x + cw / 2, cy + 128, "passt zu", 16, 400, MUTED, "middle"))
    b.append(multiline(x + 20, cy + 156, "„Verwenden, wenn Dateien in eingang/ einsortiert werden sollen“", cw - 40, 16, 400))
    b.append(arrow(x + cw / 2, cy + 206, x + cw / 2, cy + 230, color=BLUE))
    b.append(T(x + cw / 2, cy + 256, "liest die Schritte", 16, 600, BLUE, "middle"))
    b.append(T(x + cw / 2, cy + 278, "in SKILL.md", 16, 600, BLUE, "middle"))
    # 3
    x = xs[2]
    b.append(multiline(x + 20, cy + 76, "weitere Dateien im Skill-Ordner, wenn die Schritte sie verlangen", cw - 40, 16, 400, MUTED))
    b.append(folder(x + 20, cy + 150, cw - 40, 52, "vorlagen/"))
    b.append(folder(x + 20, cy + 214, cw - 40, 52, "beispiele/"))
    for i in range(2):
        b.append(arrow(xs[i] + cw + 4, cy + ch / 2, xs[i + 1] - 4, cy + ch / 2, color=BLUE))
    b.append(note16(30, 386, 940, "Skills belegen kaum Platz, solange sie nicht gebraucht werden."))
    return save(f"{L8}/laden-in-stufen.svg", svg(W, H, b))


def fig_hausordnung_regal():
    W, H = 1000, 520
    b = [heading(500, "Hausordnung und Arbeitsanweisungen")]
    # links: Aushang
    b.append(box(30, 66, 330, 330, "#ffffff", RULE, 10))
    b.append(f'<circle cx="195" cy="80" r="5" fill="{MUTED}"/>')
    b.append(M(50, 112, "AGENTS.md", 17, INK, 700))
    for i in range(6):
        b.append(badge16(62, 146 + i * 30, str(i + 1), r=11))
        b.append(f'<rect x="84" y="{140 + i * 30}" width="{230 - (i % 3) * 40}" height="10" rx="4" fill="{RULE}"/>')
    b.append(T(50, 348, "gilt bei jedem Auftrag", 16, 600))
    b.append(T(50, 372, "in jeder Sitzung ganz gelesen", 16, 400, MUTED))
    # Mitte: Agent
    b.append(glyph("agent", 500, 210))
    b.append(T(500, 250, "Agent", 16, 600, INK, "middle"))
    b.append(arrow(476, 210, 368, 210))
    b.append(arrow(524, 210, 632, 210))
    # rechts: Regal mit offenem Skill
    rx, rw = 640, 330
    b.append(box(rx, 66, rw, 330, LIGHT, BLUE, 10))
    b.append(T(rx + 20, 100, "Skills im Regal", 17, 700, BLUE))
    b.append(folder(rx + 20, 116, rw - 40, 50, "eingang-einsortieren/", "#ffffff", BLUE, BLUE, 700))
    for i, s in enumerate(["SKILL.md", "references/", "assets/", "scripts/"]):
        y = 186 + i * 36
        b.append(vline(rx + 40, 168, y - 6, MUTED, 1.5))
        b.append(hline(rx + 40, rx + 56, y - 6, MUTED, 1.5))
        b.append(M(rx + 64, y, s, 16, INK, 700 if i == 0 else 400))
    b.append(T(rx + 20, 348, "gilt bei Bedarf, darf lang sein", 16, 600))
    b.append(T(rx + 20, 372, "zuerst nur Name und Beschreibung", 16, 400, MUTED))
    b.append(note16(30, 430, 940, "Ein Skill braucht keinen Eintrag in der AGENTS.md."))
    return save(f"{L8}/hausordnung-und-regal.svg", svg(W, H, b))


def fig_eigener_skill_aus_readme():
    """Schritt 3: Aufgabe aus README.md, Vorschlag einer SKILL.md, Freigabe, Ordner <name>/SKILL.md."""
    W, H = 1000, 452
    b = [heading(500, "Aus der README.md wird ein eigener Skill")]
    y, h = 66, 300
    cols = [(30, 200), (262, 330), (624, 150), (806, 164)]
    heads = ["README.md", "Vorschlag", "Freigabe", "Anlegen"]
    fills = [("#ffffff", RULE), (LIGHT, BLUE), (AMBER_BG, AMBER_LINE), ("#ffffff", RULE)]
    for i, ((x, w), hd, (fl, st)) in enumerate(zip(cols, heads, fills)):
        b.append(box(x, y, w, h, fl, st, 12))
        b.append(badge16(x + 26, y + 30, str(i + 1), r=14))
        b.append(T(x + 48, y + 36, hd, 16, 700, BLUE if i == 1 else INK, mono=(i == 0)))
        if i < 3:
            nx = cols[i + 1][0]
            b.append(arrow(x + w + 4, y + 150, nx - 4, y + 150, color=BLUE))
    # 1 README.md: Abschnitt Wiederkehrende Aufgaben (Beispielfall)
    x, w = cols[0]
    b.append(multiline(x + 16, y + 76, "Wiederkehrende Aufgaben", w - 32, 16, 700))
    b.append(multiline(x + 16, y + 132, "• neue Anfragen einsortieren", w - 32, 16, 400, MUTED))
    b.append(T(x + 16, y + 176, "(schon ein Skill)", 16, 400, MUTED))
    b.append(box(x + 12, y + 196, w - 24, 40, "#ffffff", BLUE, 8))
    b.append(T(x + 24, y + 222, "• Wochenbericht", 16, 700, BLUE))
    b.append(multiline(x + 16, y + 266, "erste Aufgabe ohne Skill", w - 32, 16, 600, BLUE))
    # 2 Vorschlag einer SKILL.md im Chat
    x, w = cols[1]
    b.append(T(x + w - 16, y + 36, "noch nicht angelegt", 16, 400, MUTED, "end"))
    b.append(box(x + 12, y + 56, w - 24, 134, "#ffffff", RULE, 8))
    b.append(M(x + 24, y + 78, "---", 16, BLUE, 700))
    b.append(mono_rich(x + 24, y + 103, [("name: ", INK, 700), ("wochenbericht", INK, 400)]))
    b.append(mono_rich(x + 24, y + 128, [("description:", INK, 700)]))
    b.append(M(x + 24, y + 153, "Verwenden, wenn …", 16, INK))
    b.append(M(x + 24, y + 178, "---", 16, BLUE, 700))
    for j, s in enumerate(["1. Lies alle Dateien …", "…", "6. Ergänze UEBERSICHT.md."]):
        b.append(M(x + 24, y + 206 + j * 22, s, 16, INK))
    b.append(pill16(x + 16, y + 268, "höchstens sechs Schritte", "#ffffff", BLUE, BLUE)[0])
    # 3 Freigabe
    x, w = cols[2]
    b.append(multiline(x + 14, y + 80, "Sie prüfen den Vorschlag und stimmen zu oder bitten um Änderung.",
                       w - 28, 16, 400))
    # 4 Anlegen: Ordner <name>/SKILL.md
    x, w = cols[3]
    b.append(folder(x + 8, y + 64, w - 16, 52, "wochenbericht/", "#ffffff", BLUE, BLUE, 700))
    b.append(vline(x + 30, y + 118, y + 144, MUTED, 1.5))
    b.append(hline(x + 30, x + 46, y + 144, MUTED, 1.5))
    b.append(M(x + 52, y + 150, "SKILL.md", 16, INK, 700))
    b.append(multiline(x + 14, y + 196, "im Ordner für Skills, neben dem ersten Skill", w - 28, 16, 400, MUTED))
    b.append(note16(30, 388, 940, "Ohne Freigabe entsteht nichts. Der Ordnername ist gleich dem name im Kopf."))
    return save(f"{L8}/eigener-skill-aus-readme.svg", svg(W, H, b))


FIGS = [fig_pdf_fuer_den_druck, fig_textebene, fig_original_textfassung, fig_stichprobe_vier_augen,
        fig_quellenliste_regel2, fig_excel_paket, fig_blatt_wird_csv, fig_stichprobe_tabellen,
        fig_regel_und_pruefung, fig_auswertung_neue_datei, fig_eingangsordner, fig_fester_ablauf_name,
        fig_sechs_schritte, fig_skill_aufbau, fig_laden_in_stufen, fig_hausordnung_regal,
        fig_eigener_skill_aus_readme]

if __name__ == "__main__":
    for fn in FIGS:
        print(fn())

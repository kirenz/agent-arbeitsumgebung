"""Lehrbilder für Kapitel 1 „Chat oder Agent?“ und Kapitel 2 „Markdown“.

Spezifikation: Bildspezifikation L1/L2 vom 2026-10-18 (Bilder A bis E, G bis J).
Alle Schriften mindestens 16 px, Titel 20 px, Farben nur aus figlib.

Run: uv run python scripts/build_figs_l01_l02.py  (oder python3)
Ausgabe: agent-arbeitsumgebung/images/lektionen/l01-chat-oder-agent/ und l02-markdown/
"""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from figlib import (  # noqa: E402
    AMBER, AMBER_BG, AMBER_LINE, BLUE, F, GREEN, INK, LIGHT, MUTED, PAPER, RED, RULE,
    arrow, box, glyph, path_arrow, save, svg, text, text_width, wrap_px,
)

L1 = "l01-chat-oder-agent"
L2 = "l02-markdown"
MONO = 'font-family="ui-monospace, Menlo, monospace"'
MONO_W = 0.602  # Zeichenbreite Menlo/ui-monospace relativ zur Schriftgröße


# ---------------------------------------------------------------- Helfer (16 px)

def T(x, y, s, size=16, weight=400, fill=INK, anchor="start", mono=False):
    return text(x, y, s, size, weight, fill, anchor, mono)


def heading(cx, s, y=36):
    return text(cx, y, s, 20, 700, INK, "middle")


def multiline(x, y, s, max_w, size=16, weight=400, fill=INK, anchor="start", lh=21):
    out = [T(x, y + i * lh, ln, size, weight, fill, anchor) for i, ln in enumerate(wrap_px(s, max_w, size, weight))]
    return "".join(out)


def n_lines(s, max_w, size=16, weight=400):
    return len(wrap_px(s, max_w, size, weight))


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


def pill16(x, y, label, fill=LIGHT, stroke=BLUE, tcol=BLUE, mono=False, size=16):
    w = (len(label) * size * MONO_W if mono else text_width(label, size, 600)) + 22
    h = size + 12
    return (box(x, y, w, h, fill, stroke, h / 2, 1.2)
            + text(x + w / 2, y + size + 2, label, size, 600 if not mono else 700, tcol, "middle", mono)), w


def badge16(cx, cy, label, r=16, fill=BLUE):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>' + T(cx, cy + 6, label, 16, 700, "#ffffff", "middle")


def note16(x, y, w, s):
    return box(x, y, w, 44, PAPER, PAPER, 8) + T(x + 18, y + 28, s, 16, 400, INK)


def mono_rich(x, y, parts, size=16):
    """Monozeile aus (text, farbe, gewicht)-Teilen; Leerzeichen bleiben erhalten."""
    spans = "".join(
        f'<tspan fill="{c}" font-weight="{wt}">{escape(s)}</tspan>' for s, c, wt in parts)
    return f'<text x="{x}" y="{y}" {MONO} font-size="{size}" xml:space="preserve">{spans}</text>'


def mono_md(x, y, line, marks="#-|", size=16, base=INK, lead_only=False):
    """Markdown-Rohzeile: Steuerzeichen in BLUE 700, Rest in base (lead_only: nur am Zeilenanfang)."""
    parts, buf = [], ""
    for i, ch in enumerate(line):
        if ch in marks and (not lead_only or i == 0):
            if buf:
                parts.append((buf, base, 400))
                buf = ""
            parts.append((ch, BLUE, 700))
        else:
            buf += ch
    if buf:
        parts.append((buf, base, 400))
    return mono_rich(x, y, parts, size)


def bullet(x, y, s, size=16, fill=INK):
    return f'<circle cx="{x + 3}" cy="{y - 5}" r="3" fill="{INK}"/>' + T(x + 16, y, s, size, 400, fill)


def blabel(x, y, s, col=BLUE, anchor="middle"):
    return T(x, y, s, 16, 600, col, anchor)


# ---------------------------------------------------------------- Lektion 1

def fig_chat_oder_agent():
    W, H = 1000, 650
    b = [heading(500, "Derselbe Fall, zwei Wege: Chat oder Agent")]
    ct, ch = 60, 506
    # linke Karte
    b.append(box(30, ct, 455, ch, "#ffffff", RULE, 12))
    b.append(T(257.5, 95, "Chat-Assistent", 20, 700, INK, "middle"))
    b.append(T(257.5, 120, "wie ein Berater am Telefon", 16, 400, MUTED, "middle"))
    lx, lw, bh = 257.5 - 190, 380, 64
    rows = [("Beschwerde vorlesen", "Text in den Chat kopieren", "#ffffff"),
            ("Chat", "kennt nur, was im Chat steht", PAPER),
            ("Antworttext im Chat", "von Hand in eine Datei übertragen", "#ffffff")]
    ys = [150, 264, 378]
    for (hd, sb, fl), y in zip(rows, ys):
        b.append(hs_box(lx, y, lw, bh, hd, sb, fl))
    for y in ys[:-1]:
        b.append(arrow(257.5, y + bh + 4, 257.5, y + 114 - 6))
    b.append(T(257.5, 490, "kein Zugang zum Ordner", 16, 400, MUTED, "middle"))
    # rechte Karte
    b.append(box(515, ct, 455, ch, LIGHT, BLUE, 12))
    b.append(T(742.5, 95, "Agent", 20, 700, BLUE, "middle"))
    b.append(T(742.5, 120, "wie ein neuer Mitarbeiter mit Zugang zur Ablage", 16, 400, MUTED, "middle"))
    rx, rw = 542.5, 400
    b.append(hs_box(rx, 140, rw, 84, "Ziel", "Lies die Beschwerde und lege einen Antwortentwurf ab."))
    # Zeile 2: Agent <-> Ordner
    y2, h2 = 240, 124
    aw, ow = 175, 125
    b.append(hs_box(rx, y2, aw, h2, "Agent", ["beobachten,", "überlegen,", "handeln,", "wiederholen"],
                    stroke=BLUE, hcol=BLUE, hweight=700))
    ox = rx + rw - ow
    b.append(box(ox, y2, ow, h2, "#ffffff", RULE))
    b.append(glyph("doc", ox + ow / 2, y2 + 32))
    b.append(T(ox + ow / 2, y2 + 74, "Ordner", 16, 600, INK, "middle"))
    b.append(T(ox + ow / 2, y2 + 95, "Anfragen", 16, 400, MUTED, "middle"))
    b.append(T(ox + ow / 2, y2 + 115, "Antworten", 16, 400, MUTED, "middle"))
    gx1, gx2 = rx + aw + 4, ox - 4
    gm = (gx1 + gx2) / 2
    b.append(blabel(gm, y2 + 44, "Werkzeuge"))
    b.append(arrow(gx1, y2 + 60, gx2, y2 + 60, color=BLUE))
    b.append(arrow(gx2, y2 + 80, gx1, y2 + 80, color=BLUE))
    b.append(T(gm, y2 + h2 + 24, "lesen, suchen, anlegen", 16, 400, BLUE, "middle"))
    b.append(hs_box(rx, 404, rw, 64, "fragt vor Änderungen", "Erlauben oder Ablehnen im Chat",
                    AMBER_BG, AMBER_LINE))
    b.append(hs_box(rx, 482, rw, 64, "Ergebnis: Datei im Ordner", "bleibt liegen, Meldung im Chat"))
    b.append(note16(30, 584, 940, "Der Agent erinnert sich nicht an gestern. Darum liegt alles Wichtige als Datei im Ordner."))
    return save(f"{L1}/chat-oder-agent.svg", svg(W, H, b))


def fig_drei_orte():
    W, H = 1000, 400
    b = [heading(500, "Drei Orte, an denen Agenten arbeiten")]
    cy, chh, cw = 70, 256, 290
    cards = [
        (30, "In einer Chat-App im Netz", "arbeitet im Browser mit den Werkzeugen des Anbieters"),
        (355, "In einem automatischen Ablauf", "startet von selbst, etwa bei jeder neuen E-Mail"),
    ]
    for x, hd, sb in cards:
        b.append(box(x, cy, cw, chh, "#ffffff", RULE, 12))
        b.append(multiline(x + 18, cy + 40, hd, cw - 20, 18, 600, INK, lh=24))
        endy = cy + 40 + (n_lines(hd, cw - 20, 18, 600) - 1) * 24
        b.append(multiline(x + 18, endy + 30, sb, cw - 36, 16, 400, MUTED))
    x = 680
    b.append(box(x, cy, cw, chh, LIGHT, BLUE, 12))
    p, pw = pill16(0, 0, "in diesen Lektionen", "#ffffff")
    b.append(pill16(x + cw - pw - 14, cy - 14, "in diesen Lektionen", "#ffffff")[0])
    b.append(T(x + 18, cy + 40, "Auf dem eigenen Rechner", 18, 600, BLUE))
    b.append(multiline(x + 18, cy + 70, "Coding-Agent: liest, legt an und ändert Dateien in einem Ordner", cw - 36, 16, 400, MUTED))
    my, mh, mw, mw2 = cy + 140, 44, 120, 84
    b.append(hs_box(x + 18, my, mw, mh, "App mit Chat", hweight=500))
    b.append(hs_box(x + cw - 18 - mw2, my, mw2, mh, "Ordner", hweight=500))
    b.append(arrow(x + 18 + mw + 4, my + mh / 2, x + cw - 18 - mw2 - 4, my + mh / 2, color=BLUE))
    b.append(multiline(x + 18, my + mh + 28, "Aufträge, Rückfragen, Antworten: alles im Chat", cw - 36, 16, 400, MUTED))
    b.append(T(500, 365, "Die Schleife ist überall dieselbe: Ziel, beobachten, überlegen, handeln, wiederholen.",
               16, 400, MUTED, "middle"))
    return save(f"{L1}/drei-orte.svg", svg(W, H, b))


def fig_drei_anforderungen():
    W, H = 1000, 440
    b = [heading(500, "Drei Anforderungen an das Werkzeug, drei Prüfungen")]
    rows = [
        ("Dateien lesen, anlegen und ändern", "in einem Ordner auf dem eigenen Rechner",
         "Prüfung: Schritt 2", "Der Agent legt hallo.md an und zeigt sie."),
        ("Vor Änderungen nachfragen", "oder die Änderung zur Prüfung zeigen",
         "Prüfung: Schritt 2", "Rückfrage vor dem Anlegen"),
        ("Eine Anweisungsdatei lesen", "eine Datei mit Regeln im Ordner",
         "Prüfung: Schritt 3", "Der Agent nennt den Dateinamen."),
    ]
    h = 84
    for i, (h1, s1, h2, s2) in enumerate(rows):
        y = 70 + i * 100
        b.append(badge16(52, y + h / 2, str(i + 1)))
        b.append(hs_box(86, y, 560, h, h1, s1))
        b.append(arrow(654, y + h / 2, 694, y + h / 2))
        b.append(hs_box(700, y, 270, h, h2, s2, PAPER))
    b.append(note16(30, 376, 940, "Das Werkzeug ist frei wählbar. Es muss diese drei Dinge können."))
    return save(f"{L1}/drei-anforderungen.svg", svg(W, H, b))


def fig_weg_eines_auftrags():
    W, H = 1000, 960
    b = [heading(500, "Der Weg eines Auftrags: von einem Satz zur Datei")]
    cols = {"chat": 180, "agent": 500, "app": 820}
    heads = [("chat", "Chat", "Auftrag und Freigabe", PAPER, RULE, INK),
             ("agent", "Agent", "überlegt und wählt", LIGHT, BLUE, BLUE),
             ("app", "App", "führt aus und fragt", PAPER, RULE, INK)]
    for k, hd, sb, fl, st, tc in heads:
        cx = cols[k]
        b.append(box(cx - 150, 56, 300, 58, fl, st))
        b.append(T(cx, 80, hd, 16, 700, tc, "middle"))
        b.append(T(cx, 103, sb, 16, 400, MUTED, "middle"))
        b.append(f'<line x1="{cx}" y1="120" x2="{cx}" y2="886" stroke="{RULE}" stroke-width="1" stroke-dasharray="4 5"/>')
    steps = [
        ("chat", "Ziel", "Auftrag: hallo.md anlegen, vorher fragen", "#ffffff", RULE),
        ("agent", "Beobachten", "Der Ordner ist leer.", "#ffffff", RULE),
        ("agent", "Überlegen", "Inhalt: Überschrift „Test“ und Datum", "#ffffff", RULE),
        ("agent", "Handeln", "wählt das Werkzeug „Datei anlegen“", "#ffffff", RULE),
        ("app", None, "fragt: Datei anlegen? Erlauben / Ablehnen", AMBER_BG, AMBER_LINE),
        ("chat", None, "Freigabe: Erlauben", "#ffffff", RULE),
        ("app", None, "legt hallo.md an, meldet „hallo.md angelegt“", "#ffffff", BLUE),
        ("agent", "Ziel erreicht", "Fertig. Eine Datei angelegt, keine geändert.", "#ffffff", RULE),
    ]
    bw, bh, y0, step = 270, 66, 140, 96
    geo = []
    for i, (col, pl, txt, fl, st) in enumerate(steps):
        cx = cols[col]
        x, y = cx - bw / 2, y0 + i * step
        geo.append((cx, x, y))
        b.append(box(x, y, bw, bh, fl, st, sw=1.5))
        ls = wrap_px(txt, bw - 28, 16, 500)
        top = y + (bh - len(ls) * 21) / 2 + 15 + (5 if pl else 0)
        for j, ln in enumerate(ls):
            b.append(T(x + 14, top + j * 21, ln, 16, 500))
    for i, (col, pl, *_r) in enumerate(steps):
        if pl:
            cx, x, y = geo[i]
            b.append(pill16(x + 12, y - 14, pl, "#ffffff")[0])
    for i in range(len(steps) - 1):
        (c1, x1, y1), (c2, x2, y2) = geo[i], geo[i + 1]
        col = BLUE if False else None
        if c1 == c2:
            b.append(arrow(c1 + 70, y1 + bh + 2, c1 + 70, y2 - 3, color=col))
        else:
            mid = y2 + bh / 2
            ex = x2 - 3 if c2 > c1 else x2 + bw + 3
            b.append(path_arrow(f"M{c1},{y1 + bh + 2} L{c1},{mid} L{ex},{mid}", col))
    b.append(note16(30, 902, 940, "Den Text schreibt der Agent. Die Datei legt die App an, und sie fragt vorher."))
    return save(f"{L1}/weg-eines-auftrags.svg", svg(W, H, b))


def fig_wann_agent():
    W, H = 1000, 440
    b = [heading(500, "Wann lohnt sich der Agent?")]
    b.append(hs_box(30, 90, 430, 70, "Liegt das Material schon als Dateien vor?", hweight=500))
    b.append(hs_box(30, 230, 430, 70, "Soll das Ergebnis als Datei entstehen?", hweight=500))
    ax, ay, aw, ah = 590, 76, 380, 140
    b.append(box(ax, ay, aw, ah, LIGHT, BLUE))
    b.append(T(ax + 20, ay + 34, "Agent im Ordner", 18, 700, BLUE))
    b.append(multiline(ax + 20, ay + 62, "liest Dateien selbst, fragt vor Änderungen, legt das Ergebnis ab", aw - 40, 16, 400, MUTED))
    b.append(T(ax + 20, ay + 120, "etwa: drei Anfragen im Ordner sortieren", 16, 400, MUTED))
    cx_, cy_, ch_ = 590, 280, 110
    b.append(box(cx_, cy_, aw, ch_, "#ffffff", RULE))
    b.append(T(cx_ + 20, cy_ + 34, "Chat", 18, 700, INK))
    b.append(T(cx_ + 20, cy_ + 62, "eine kurze Frage ohne Material", 16, 400, MUTED))
    b.append(T(cx_ + 20, cy_ + 90, "etwa: eine Formulierung verbessern", 16, 400, MUTED))
    b.append(arrow(464, 125, 584, 125, color=BLUE))
    b.append(blabel(524, 116, "Ja"))
    b.append(arrow(464, 255, 584, 190, color=BLUE))
    b.append(blabel(516, 208, "Ja"))
    b.append(path_arrow("M245,302 L245,335 L584,335"))
    b.append(blabel(415, 326, "beides Nein", MUTED, "middle"))
    b.append(T(500, 425, "Eine Ja-Antwort genügt für den Agenten.", 16, 400, MUTED, "middle"))
    return save(f"{L1}/wann-agent-wann-chat.svg", svg(W, H, b))


# ---------------------------------------------------------------- Lektion 2

def panel(x, y, w, h, head):
    return (box(x, y, w, h, "#ffffff", RULE)
            + f'<path d="M{x + 10},{y} H{x + w - 10} Q{x + w},{y} {x + w},{y + 10} V{y + 38} H{x} V{y + 10} Q{x},{y} {x + 10},{y} Z" fill="{PAPER}"/>'
            + f'<line x1="{x}" y1="{y + 38}" x2="{x + w}" y2="{y + 38}" stroke="{RULE}" stroke-width="1"/>'
            + box(x, y, w, h, "none", RULE)
            + T(x + 18, y + 25, head, 16, 600))


def fig_rohtext_vorschau():
    W, H = 1000, 440
    b = [heading(500, "Dieselbe Datei, zwei Ansichten")]
    lx, lw, rx, rw, py, ph = 30, 385, 585, 385, 70, 290
    b.append(panel(lx, py, lw, ph, "Rohtext: so liest der Agent"))
    b.append(panel(rx, py, rw, ph, "Vorschau: so zeigt der Chat"))
    raw = ["# Terminwunsch", "", "- Datum: 2026-10-05", "- Kanal: E-Mail", "- Anliegen: Termin für eine Reparatur"]
    ys = [140 + i * 30 for i in range(5)]
    for ln, y in zip(raw, ys):
        if ln:
            b.append(mono_md(lx + 18, y, ln, "#-", lead_only=True))
    b.append(pill16(lx + 18, 300, "fester Kopf: Datum, Kanal, Anliegen")[0])
    b.append(T(rx + 22, ys[0] + 2, "Terminwunsch", 22, 700))
    for s, y in zip(["Datum: 2026-10-05", "Kanal: E-Mail", "Anliegen: Termin für eine Reparatur"], ys[2:]):
        b.append(bullet(rx + 24, y, s))
    gx1, gx2 = lx + lw + 4, rx - 4
    gm = (gx1 + gx2) / 2
    b.append(arrow(gx1, ys[0] - 5, gx2, ys[0] - 5, color=BLUE))
    b.append(blabel(gm, ys[0] - 14, "# wird Überschrift"))
    b.append(arrow(gx1, ys[2] - 5, gx2, ys[2] - 5, color=BLUE))
    b.append(blabel(gm, ys[2] - 14, "- wird Listenpunkt"))
    b.append(T(500, 410, "Der Agent liest immer den Rohtext. Die Zeichen verschwinden erst in der Vorschau.",
               16, 400, MUTED, "middle"))
    return save(f"{L2}/rohtext-und-vorschau.svg", svg(W, H, b))


def fig_tabelle_aufbau():
    W, H = 1000, 420
    b = [heading(500, "Aufbau einer Markdown-Tabelle")]
    b.append(box(30, 66, 570, 260, PAPER, RULE))
    rows = ["| Datei | Anliegen |", "|---|---|", "| hallo.md | Test |", "| terminwunsch.md | Termin für eine Reparatur |"]
    for i, (ln, bd) in enumerate(zip(rows, ["1", "2", "3", "3"])):
        y = 120 + i * 56
        b.append(badge16(62, y - 6, bd, r=15))
        b.append(mono_md(92, y, ln, "|", 17))
    cards = [("Kopfzeile", "Spaltennamen"),
             ("Trennzeile", "trennt Kopf und Inhalt; fehlt sie, keine Tabelle"),
             ("Eine Zeile je Eintrag", "hier zwei Einträge")]
    for i, (hd, sb) in enumerate(cards):
        y = 66 + i * 94
        b.append(box(630, y, 340, 80, "#ffffff", RULE))
        b.append(badge16(656, y + 40, str(i + 1), r=15))
        subs = wrap_px(sb, 270, 16)
        top = y + (80 - (16 + len(subs) * 21)) / 2 + 13
        b.append(T(684, top, hd, 16, 600))
        for j, s in enumerate(subs):
            b.append(T(684, top + (j + 1) * 21 + 1, s, 16, 400, MUTED))
    b.append(note16(30, 350, 940, "Jede Zeile hat gleich viele Spalten, hier zwei. Die Striche müssen nicht untereinander stehen."))
    return save(f"{L2}/tabelle-aufbau.svg", svg(W, H, b))


def fig_zeilenvergleich():
    W, H = 1000, 460
    b = [heading(500, "Einen Zeilenvergleich lesen")]
    b.append(box(30, 66, 550, 226, "#ffffff", RULE))
    ys = [110 + i * 38 for i in range(5)]
    cw = 16 * MONO_W
    # Bänder
    b.append(box(40, ys[1] - 22, 530, 32, AMBER_BG, AMBER_BG, 6))
    b.append(box(40, ys[2] - 22, 530, 32, LIGHT, LIGHT, 6))
    b.append(mono_rich(52, ys[0], [("  - Datum: 2026-10-05", MUTED, 400)]))
    old = "- Kanal: E-Mail"
    b.append(mono_rich(52, ys[1], [("-", AMBER, 700), (" " + old, INK, 400)]))
    sx = 52 + 2 * cw
    b.append(f'<line x1="{sx - 2}" y1="{ys[1] - 5}" x2="{sx + len(old) * cw + 2}" y2="{ys[1] - 5}" stroke="{INK}" stroke-width="1.5"/>')
    b.append(mono_rich(52, ys[2], [("+", BLUE, 700), (" - Kanal: Telefon", INK, 400)]))
    b.append(mono_rich(52, ys[3], [("  - Anliegen: Termin für eine Reparatur", MUTED, 400)]))
    b.append(mono_rich(52, ys[4], [("  - Rückruf: ja", MUTED, 400)]))
    leg = [(AMBER_BG, AMBER_LINE, "alte Zeile, fällt weg"),
           (LIGHT, BLUE, "neue Zeile, kommt hinzu"),
           ("#ffffff", RULE, "bleibt unverändert")]
    for i, (fl, st, s) in enumerate(leg):
        y = 120 + i * 56
        b.append(box(616, y - 15, 20, 20, fl, st, 4))
        b.append(T(648, y + 1, s))
    b.append(box(30, 316, 940, 116, LIGHT, BLUE))
    b.append(T(52, 354, "Prüffrage vor der Freigabe: Ist nur die eine Zeile markiert?", 16, 600))
    b.append(glyph("check", 66, 399))
    b.append(T(90, 405, "Ja: Erlauben", 16, 600, GREEN))
    b.append(T(300, 405, "✗", 18, 700, RED))
    b.append(T(324, 405, "Mehr Zeilen markiert: Ablehnen und Auftrag wiederholen", 16, 600, RED))
    return save(f"{L2}/zeilenvergleich-lesen.svg", svg(W, H, b))


def fig_fuenf_zeichen():
    W, H = 1000, 500
    b = [heading(500, "Markdown in diesem Kurs: fünf Zeichen")]
    c1, c2, c3 = 30, 200, 620
    for x, s in [(c1, "Zeichen"), (c2, "Rohtext"), (c3, "Vorschau")]:
        b.append(T(x, 72, s, 16, 600, MUTED))
    b.append(f'<line x1="30" y1="84" x2="970" y2="84" stroke="{RULE}" stroke-width="1"/>')
    base = [124 + i * 66 for i in range(5)]
    for y in base[1:]:
        b.append(f'<line x1="30" y1="{y - 38}" x2="970" y2="{y - 38}" stroke="{RULE}" stroke-width="1"/>')
    sym = ["#", "-", "|", "**fett**", "[Text](Ziel)"]
    raw = [
        [("#", BLUE, 700), (" Überschrift", INK, 400)],
        [("-", BLUE, 700), (" Listenpunkt", INK, 400)],
        [("|", BLUE, 700), (" Datei ", INK, 400), ("|", BLUE, 700), (" Anliegen ", INK, 400), ("|", BLUE, 700)],
        [("ein ", INK, 400), ("**", BLUE, 700), ("wichtiges", INK, 400), ("**", BLUE, 700), (" Wort", INK, 400)],
        [("[", BLUE, 700), ("Preisliste", INK, 400), ("](", BLUE, 700), ("preisliste-2026.md", INK, 400), (")", BLUE, 700)],
    ]
    for y, s, r in zip(base, sym, raw):
        b.append(pill16(c1, y - 20, s, mono=True)[0])
        b.append(mono_rich(c2, y, r))
    y = base
    b.append(T(c3, y[0] + 2, "Überschrift", 22, 700))
    b.append(bullet(c3, y[1], "Listenpunkt"))
    for i, s in enumerate(["Datei", "Anliegen"]):
        b.append(f'<rect x="{c3 + i * 110}" y="{y[2] - 21}" width="110" height="30" fill="{PAPER}" stroke="{RULE}" stroke-width="1"/>')
        b.append(T(c3 + i * 110 + 10, y[2], s, 16, 600))
    b.append(f'<text x="{c3}" y="{y[3]}" {F} font-size="16" fill="{INK}">ein <tspan font-weight="700">wichtiges</tspan> Wort</text>')
    lw = len("Preisliste") * 16 * 0.47
    b.append(f'<text x="{c3}" y="{y[4]}" {F} font-size="16" fill="{BLUE}" text-decoration="underline">Preisliste</text>')
    b.append(T(c3 + lw + 16, y[4], "öffnet die Datei im Ordner", 16, 400, MUTED))
    b.append(note16(30, 438, 940, "Der Agent liest den Rohtext und folgt Links auch zu anderen Dateien im Ordner."))
    return save(f"{L2}/fuenf-zeichen.svg", svg(W, H, b))


# ---------------------------------------------------------------- Lektion 1: Ordner wählen je App
# Vereinfachte Nachzeichnungen der App-Oberflächen (Stand 2026-10-21), je drei Schritte.

def folder_icon(cx, cy, col=INK):
    return (f'<path d="M{cx - 10},{cy - 7} L{cx - 3},{cy - 7} L{cx},{cy - 4} L{cx + 10},{cy - 4} '
            f'L{cx + 10},{cy + 8} L{cx - 10},{cy + 8} Z" fill="#ffffff" stroke="{col}" stroke-width="1.6"/>')


def ui_chip(x, y, label, hl=False, w=None, icon=None):
    """Bedienelement der App; hl hebt das anzuklickende Element hervor."""
    fill, stroke, col, sw = (LIGHT, BLUE, BLUE, 2.2) if hl else ("#ffffff", RULE, INK, 1.5)
    w = w or text_width(label, 16, 600) + (44 if icon else 24)
    out = box(x, y, w, 34, fill, stroke, 8, sw)
    tx = x + 12
    if icon == "folder":
        out += folder_icon(x + 20, y + 17, col)
        tx = x + 36
    elif icon == "plus":
        out += T(x + 20, y + 23, "+", 18, 700, col, "middle")
        tx = x + 34
    if label:
        out += T(tx, y + 23, label, 16, 600, col)
    return out


def app_frame(x, y, w, h):
    """Angedeutetes App-Fenster mit Titelleiste."""
    dots = "".join(f'<circle cx="{x + 16 + i * 14}" cy="{y + 14}" r="4" fill="{RULE}"/>' for i in range(3))
    return (box(x, y, w, h, "#ffffff", RULE, 10)
            + f'<line x1="{x}" y1="{y + 28}" x2="{x + w}" y2="{y + 28}" stroke="{RULE}" stroke-width="1.2"/>' + dots)


def ordner_fig(name, titel, steps, check):
    """Drei Schritt-Felder nebeneinander; steps = [(Kopf, Zeichenfunktion(x, y), Hinweis)]."""
    W, H = 1000, 452
    b = [heading(500, titel)]
    pw, ph, top = 300, 310, 60
    for i, (head, draw, hint) in enumerate(steps):
        x = 30 + i * (pw + 20)
        b.append(box(x, top, pw, ph, "#ffffff", RULE, 12))
        b.append(badge16(x + 28, top + 30, str(i + 1)))
        b.append(T(x + 54, top + 36, head, 16, 600))
        b.append(app_frame(x + 16, top + 60, pw - 32, 180))
        b.append(draw(x + 32, top + 112))
        b.append(multiline(x + pw / 2, top + 268, hint, pw - 32, 16, 400, MUTED, "middle"))
        if i < 2:
            b.append(arrow(x + pw + 2, top + ph / 2, x + pw + 18, top + ph / 2))
    b.append(note16(30, 392, 940, check))
    return save(f"{L1}/{name}.svg", svg(W, H, b))


def fig_ordner_claude():
    def s1(x, y):
        # oben rechts der Umschalter (Code hervorgehoben), unten Eingabefeld mit Umgebungsfeld
        bx, by = x + 172, y - 49
        out = (box(bx, by, 30, 21, "#ffffff", RULE, 6) + box(bx + 34, by, 30, 21, LIGHT, BLUE, 6, 2)
               + T(bx + 49, by + 15, "</>", 12, 700, BLUE, "middle", mono=True))
        out += box(x, y + 8, 236, 40, PAPER, RULE, 10) + T(x + 12, y + 33, "Beschreibe eine Aufgabe …", 16, 400, MUTED)
        out += ui_chip(x, y + 56, "Dieser Computer", hl=True, w=180)
        return out

    def s2(x, y):
        return (T(x, y - 4, "Lokal", 16, 400, MUTED) + T(x, y + 20, "Dieser Computer", 16, 400, INK)
                + f'<line x1="{x}" y1="{y + 34}" x2="{x + 236}" y2="{y + 34}" stroke="{RULE}" stroke-width="1.2"/>'
                + ui_chip(x, y + 46, "Neue Umgebung", hl=True, icon="plus", w=186))

    def s3(x, y):
        return (ui_chip(x, y - 28, "Lokal", w=66) + T(x + 76, y - 5, "Cloud  SSH", 16, 400, MUTED)
                + ui_chip(x, y + 10, "agent-test", w=236)
                + ui_chip(x, y + 48, "Hinzufügen", hl=True, icon="plus", w=146)
                + T(x + 154, y + 71, "Auswählen …", 14, 600, BLUE)
                + ui_chip(x + 46, y + 86, "Umgebung erstellen", hl=True, w=190))

    return ordner_fig("ordner-claude", "Claude-Desktop-App: Ordner als Umgebung wählen", [
        ("Umgebung öffnen", s1, "Code-Symbol oben rechts, dann Feld unter der Eingabe"),
        ("„Neue Umgebung“", s2, "unten im Menü"),
        ("Ordner hinzufügen", s3, "Reiter Lokal, Name und Ordner: agent-test"),
    ], "Prüfen: Unter dem Eingabefeld steht agent-test. Erst dann die erste Nachricht senden.")


def fig_ordner_codex():
    def s1(x, y):
        return (ui_chip(x, y - 10, "Projekt auswählen", hl=True, icon="folder", w=200)
                + box(x, y + 34, 236, 44, PAPER, RULE, 10) + T(x + 12, y + 62, "Leg einfach los", 16, 400, MUTED))

    def s2(x, y):
        return (T(x, y - 4, "rechnung-pdf", 16, 400, MUTED) + T(x, y + 20, "notes", 16, 400, MUTED)
                + f'<line x1="{x}" y1="{y + 34}" x2="{x + 236}" y2="{y + 34}" stroke="{RULE}" stroke-width="1.2"/>'
                + ui_chip(x, y + 46, "Neues Projekt", hl=True, icon="plus", w=170))

    def s3(x, y):
        return (ui_chip(x, y - 14, "agent-test", icon="folder", w=236)
                + ui_chip(x, y + 28, "Hinzufügen", hl=True, icon="folder", w=150)
                + ui_chip(x + 66, y + 70, "Projekt erstellen", hl=True, w=170))

    return ordner_fig("ordner-codex", "Codex-App: Ordner als Projekt wählen", [
        ("„Projekt auswählen“", s1, "über dem Eingabefeld; oder Button „Codex öffnen“"),
        ("„Neues Projekt“", s2, "unten in der Liste der Projekte"),
        ("Ordner hinzufügen", s3, "Projektname und Ordner: agent-test"),
    ], "Prüfen: In der Seitenleiste steht unter „Projekte“ der Eintrag agent-test.")


def fig_ordner_antigravity():
    def s1(x, y):
        return (box(x - 16, y - 23, 64, 150, PAPER, RULE, 0, 1)
                + ui_chip(x - 6, y - 10, "", hl=True, icon="folder", w=44)
                + T(x + 20, y + 4, "+", 14, 700, BLUE, "middle")
                + T(x + 60, y + 13, "New Project", 16, 600, BLUE))

    def s2(x, y):
        return (ui_chip(x, y - 10, "Add Folder", hl=True, icon="folder", w=150)
                + T(x, y + 56, "dann agent-test wählen", 16, 400, MUTED))

    def s3(x, y):
        return ui_chip(x, y - 14, "agent-test", icon="folder", w=236) + ui_chip(x + 136, y + 44, "Create", hl=True, w=100)

    return ordner_fig("ordner-antigravity", "Antigravity-App: Ordner als Projekt wählen", [
        ("„New Project“", s1, "Ordner mit Plus in der linken Seitenleiste"),
        ("„Add Folder“", s2, "im Fenster Dokumente, dann agent-test"),
        ("„Create“", s3, "legt das Projekt an"),
    ], "Prüfen: Die Seitenleiste zeigt das Projekt agent-test.")


FIGS = [fig_ordner_claude, fig_ordner_codex, fig_ordner_antigravity, fig_chat_oder_agent, fig_drei_orte, fig_drei_anforderungen, fig_weg_eines_auftrags, fig_wann_agent,
        fig_rohtext_vorschau, fig_tabelle_aufbau, fig_zeilenvergleich, fig_fuenf_zeichen]

if __name__ == "__main__":
    for fn in FIGS:
        print(fn())

"""Gemeinsame Zeichen-Helfer für die Lehrabbildungen des Agenten-Kurses (SVG, ohne Abhängigkeiten).

Stil wie im Kurs n8n-Grundlagen (scripts/build_overview_figures.py dort):
weißer Grund, Inter, Akzent #0052ff, haarfeine Linien, Grün/Rot nur für Richtig/Falsch.
Nachgezeichnete n8n-Ansichten (Canvas, Knoten-Panel) liegen in n8n_darstellung.py.

Benutzung in einem Abschnitts-Skript (scripts/build_figs_<abschnitt>.py):

    from figlib import *
    b = [title(450, "Überschrift")]
    b.append(card(30, 60, 200, 70, "Titel", "Untertitel"))
    save("agent/drafter-ablauf.svg", svg(900, 300, b))

Bilder landen unter agent-arbeitsumgebung/images/lektionen/<abschnitt>/ und sind über
https://kirenz.github.io/agent-arbeitsumgebung/agent-arbeitsumgebung/images/lektionen/<abschnitt>/<datei>.svg erreichbar.
preview(pfad) rastert ein SVG nach PNG (rsvg-convert) für die Sichtprüfung.
"""

from __future__ import annotations

import subprocess
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "agent-arbeitsumgebung" / "images" / "lektionen"
BASE_URL = "https://kirenz.github.io/agent-arbeitsumgebung/agent-arbeitsumgebung/images/lektionen"

F = 'font-family="Inter, Helvetica, Arial, sans-serif"'
INK, MUTED, RULE, BLUE, LIGHT = "#18181b", "#52525b", "#d4d4d8", "#0052ff", "#e8efff"
GREEN, RED, PAPER, AMBER = "#16a34a", "#dc2626", "#f4f4f5", "#d97706"
GREEN_BG, GREEN_LINE, RED_BG, RED_LINE = "#f0fdf4", "#bbf7d0", "#fef2f2", "#fecaca"
AMBER_BG, AMBER_LINE, VIOLET = "#fffbeb", "#fde68a", "#7c3aed"


def svg(w, h, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
        f'<marker id="ab" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker></defs>'
        f'<rect width="{w}" height="{h}" fill="#ffffff"/>' + "".join(body) + "</svg>"
    )


def text(x, y, s, size=14, weight=400, fill=INK, anchor="start", mono=False):
    fam = 'font-family="ui-monospace, Menlo, monospace"' if mono else F
    return f'<text x="{x}" y="{y}" {fam} font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(str(s))}</text>'


def title(cx, s, y=34, size=17):
    """Bildüberschrift, zentriert."""
    return text(cx, y, s, size, 700, INK, "middle")


def text_width(s, size=14, weight=400):
    """Grobe Breitenschätzung für Inter (reicht für Umbrüche und Kartenbreiten)."""
    factor = 0.56 if weight < 600 else 0.6
    return len(str(s)) * size * factor


def wrap_px(s, max_w, size=14, weight=400):
    """Bricht Text so um, dass jede Zeile höchstens max_w Pixel breit ist."""
    words, lines, cur = str(s).split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if cur and text_width(cand, size, weight) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    return lines + [cur] if cur else lines


def lines(x, y, s, max_w, size=14, weight=400, fill=INK, anchor="start", lh=None):
    """Mehrzeiliger Text mit Umbruch. Gibt (svg_teile, endy) zurück."""
    lh = lh or size * 1.4
    out = []
    for i, ln in enumerate(wrap_px(s, max_w, size, weight)):
        out.append(text(x, y + i * lh, ln, size, weight, fill, anchor))
    return "".join(out), y + max(len(out) - 1, 0) * lh


def box(x, y, w, h, fill="#ffffff", stroke=RULE, rx=10, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def arrow(x1, y1, x2, y2, label=None, dy=-8, dx=0, color=None, dash=None):
    col = color or MUTED
    mk = "ab" if color == BLUE else "a"
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2" marker-end="url(#{mk})"{d}/>'
    if label:
        out += text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, label, 13, 600, col, "middle")
    return out


def path_arrow(d, color=None, dash=None):
    """Gebogener Pfeil über einen SVG-Pfad (z. B. 'M10,10 C60,10 60,80 110,80')."""
    col = color or MUTED
    mk = "ab" if color == BLUE else "a"
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" stroke="{col}" stroke-width="2" fill="none" marker-end="url(#{mk})"{dd}/>'


def card(x, y, w, h, head, sub=None, fill="#ffffff", stroke=RULE, tcol=INK, size=15):
    """Karte mit zentriertem Titel und optionalem (umbrochenem) Untertitel."""
    out = box(x, y, w, h, fill, stroke)
    sub_lines = wrap_px(sub, w - 20, 12) if sub else []
    block = 18 + len(sub_lines) * 16
    top = y + (h - block) / 2 + 13
    out += text(x + w / 2, top, head, size, 600, tcol, "middle")
    for i, ln in enumerate(sub_lines):
        out += text(x + w / 2, top + 20 + i * 16, ln, 12, 400, MUTED if tcol == INK else tcol, "middle")
    return out


def badge(cx, cy, label, fill=BLUE, r=13):
    """Nummernkreis, z. B. für Schrittfolgen oder Zuordnungen Bild ↔ Text."""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>' + text(cx, cy + 5, label, 13, 700, "#ffffff", "middle")


def pill(x, y, label, fill=LIGHT, stroke=BLUE, tcol=BLUE, size=12):
    """Kleines Etikett (z. B. Kategorie, Tool-Name)."""
    w = text_width(label, size, 600) + 20
    return box(x, y, w, size + 12, fill, stroke, (size + 12) / 2, 1.2) + text(x + w / 2, y + size + 4, label, size, 600, tcol, "middle")


def note_bar(x, y, w, s, fill=PAPER, size=13):
    """Graue Fußleiste mit Merksatz."""
    return box(x, y, w, 40, fill, fill, 8) + text(x + 18, y + 25, s, size, 400, INK)


def falsch_richtig(title_text, falsch_title, falsch_items, richtig_title, richtig_items, width=900, row_h=34):
    """Gegenüberstellung Falsch (links, rot) und Richtig (rechts, grün).

    Jan bevorzugt Falsch/Richtig nebeneinander statt Umschaltern (Vorher/Nachher-Toggle).
    """
    n = max(len(falsch_items), len(richtig_items))
    col_w = (width - 90) / 2
    H = 110 + n * row_h + 20
    b = [title(width / 2, title_text)]
    b.append(box(30, 56, col_w, H - 76, RED_BG, RED_LINE, 12))
    b.append(box(60 + col_w, 56, col_w, H - 76, GREEN_BG, GREEN_LINE, 12))
    b.append(text(30 + col_w / 2, 86, falsch_title, 15, 700, RED, "middle"))
    b.append(text(60 + col_w * 1.5, 86, richtig_title, 15, 700, GREEN, "middle"))
    for i, item in enumerate(falsch_items):
        y = 122 + i * row_h
        b.append(text(52, y, "✗", 15, 700, RED))
        b.append(text(74, y, item, 13))
    for i, item in enumerate(richtig_items):
        y = 122 + i * row_h
        b.append(text(82 + col_w, y, "✓", 15, 700, GREEN))
        b.append(text(104 + col_w, y, item, 13))
    return svg(width, H, b)


def glyph(kind, cx, cy, col=INK):
    """Kleine Erkennungszeichen für Lernweg-Karten und Übersichten."""
    st = f'stroke="{col}" stroke-width="2" fill="#ffffff"'
    if kind == "agent":
        return f'<rect x="{cx - 16}" y="{cy - 12}" width="32" height="26" rx="7" {st}/><circle cx="{cx - 6}" cy="{cy}" r="3" fill="{col}"/><circle cx="{cx + 6}" cy="{cy}" r="3" fill="{col}"/><line x1="{cx}" y1="{cy - 12}" x2="{cx}" y2="{cy - 19}" stroke="{col}" stroke-width="2"/>'
    if kind == "tool":
        return f'<path d="M{cx - 12},{cy + 12} L{cx + 4},{cy - 4}" stroke="{col}" stroke-width="4" stroke-linecap="round"/><circle cx="{cx + 8}" cy="{cy - 8}" r="8" {st}/>'
    if kind == "doc":
        return f'<path d="M{cx - 12},{cy - 16} L{cx + 6},{cy - 16} L{cx + 12},{cy - 10} L{cx + 12},{cy + 16} L{cx - 12},{cy + 16} Z" {st}/>' + "".join(
            f'<line x1="{cx - 7}" y1="{cy - 6 + i * 7}" x2="{cx + 7}" y2="{cy - 6 + i * 7}" stroke="{col}" stroke-width="1.5"/>' for i in range(3))
    if kind == "db":
        return f'<ellipse cx="{cx}" cy="{cy - 10}" rx="14" ry="5" {st}/><path d="M{cx - 14},{cy - 10} L{cx - 14},{cy + 10} Q{cx},{cy + 17} {cx + 14},{cy + 10} L{cx + 14},{cy - 10}" {st}/>'
    if kind == "mail":
        return f'<rect x="{cx - 16}" y="{cy - 11}" width="32" height="22" rx="3" {st}/><path d="M{cx - 16},{cy - 11} L{cx},{cy + 2} L{cx + 16},{cy - 11}" stroke="{col}" stroke-width="2" fill="none"/>'
    if kind == "person":
        return f'<circle cx="{cx}" cy="{cy - 8}" r="7" {st}/><path d="M{cx - 13},{cy + 15} Q{cx - 13},{cy + 1} {cx},{cy + 1} Q{cx + 13},{cy + 1} {cx + 13},{cy + 15}" {st}/>'
    if kind == "check":
        return f'<circle cx="{cx}" cy="{cy}" r="14" {st}/><path d="M{cx - 7},{cy} L{cx - 2},{cy + 6} L{cx + 8},{cy - 6}" stroke="{GREEN}" stroke-width="3" fill="none"/>'
    if kind == "gate":
        return f'<polygon points="{cx},{cy - 15} {cx + 15},{cy} {cx},{cy + 15} {cx - 15},{cy}" {st}/>'
    if kind == "loop":
        return f'<path d="M{cx + 12},{cy - 4} A12,12 0 1,0 {cx + 4},{cy + 11}" stroke="{col}" stroke-width="2.5" fill="none"/><path d="M{cx + 7},{cy - 9} L{cx + 13},{cy - 3} L{cx + 17},{cy - 10}" stroke="{col}" stroke-width="2.5" fill="none"/>'
    if kind == "chart":
        return "".join(f'<rect x="{cx - 14 + i * 10}" y="{cy + 12 - hgt}" width="7" height="{hgt}" fill="{col}"/>' for i, hgt in enumerate((10, 18, 26)))
    if kind == "voice":
        return f'<rect x="{cx - 6}" y="{cy - 16}" width="12" height="20" rx="6" {st}/><path d="M{cx - 11},{cy} Q{cx - 11},{cy + 11} {cx},{cy + 11} Q{cx + 11},{cy + 11} {cx + 11},{cy}" stroke="{col}" stroke-width="2" fill="none"/><line x1="{cx}" y1="{cy + 11}" x2="{cx}" y2="{cy + 17}" stroke="{col}" stroke-width="2"/>'
    if kind == "shield":
        return f'<path d="M{cx},{cy - 16} L{cx + 13},{cy - 10} L{cx + 13},{cy + 2} Q{cx + 13},{cy + 12} {cx},{cy + 17} Q{cx - 13},{cy + 12} {cx - 13},{cy + 2} L{cx - 13},{cy - 10} Z" {st}/>'
    if kind == "flow":
        return (f'<rect x="{cx - 34}" y="{cy - 9}" width="18" height="18" rx="4" fill="{LIGHT}" stroke="{BLUE}" stroke-width="2"/>'
                f'<rect x="{cx - 9}" y="{cy - 9}" width="18" height="18" rx="4" fill="{LIGHT}" stroke="{BLUE}" stroke-width="2"/>'
                f'<rect x="{cx + 16}" y="{cy - 9}" width="18" height="18" rx="4" fill="{LIGHT}" stroke="{BLUE}" stroke-width="2"/>')
    return ""


def lernweg(title_text, items, cols, note, h_card=150, width=900):
    """Lernweg-Karten wie in den Kapitelübersichten des Grundlagen-Kurses.

    items: (glyph, Name, Untertitel[, Badge]) – Badge "" lässt den Nummernkreis weg.
    """
    rows = (len(items) + cols - 1) // cols
    gap = 30
    cw = (width - 60 - (cols - 1) * gap) / cols
    H = 70 + rows * (h_card + 30) + 30
    b = [title(width / 2, title_text)]
    for i, item in enumerate(items):
        g, name, sub = item[:3]
        bd = item[3] if len(item) > 3 else str(i + 1)
        r, c = divmod(i, cols)
        x, y = 30 + c * (cw + gap), 55 + r * (h_card + 30)
        b.append(box(x, y, cw, h_card, "#ffffff", RULE, 12))
        if bd:
            b.append(badge(x + 26, y + 26, bd, r=14))
        b.append(glyph(g, x + cw - 40, y + 30))
        b.append(lines(x + 18, y + 78, name, cw - 36, 15, 700)[0])
        b.append(lines(x + 18, y + 104, sub, cw - 36, 12, 400, MUTED, lh=16)[0])
        if c < cols - 1 and i < len(items) - 1:
            b.append(arrow(x + cw + 2, y + h_card / 2, x + cw + gap - 2, y + h_card / 2))
    b.append(text(width / 2, H - 14, note, 13, 400, MUTED, "middle"))
    return svg(width, H, b)


def save(rel, content):
    """Schreibt nach agent-arbeitsumgebung/images/lektionen/<rel> und gibt die öffentliche URL zurück."""
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"{BASE_URL}/{rel}"


def preview(rel, out_dir, width=1000):
    """Rastert agent-arbeitsumgebung/images/lektionen/<rel> nach out_dir/<name>.png für die Sichtprüfung."""
    src = OUT / rel
    dst = Path(out_dir) / (src.stem + ".png")
    subprocess.run(["rsvg-convert", "-w", str(width), str(src), "-o", str(dst)], check=True)
    return dst

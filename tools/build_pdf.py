"""Build Jess_Moore_CV.pdf, the printable version of index.html.

Content lives in this file, not in index.html, so update both when the CV changes.

    python3 -m pip install reportlab
    python3 tools/build_pdf.py

Fonts (Playfair Display, Source Serif 4; SIL OFL) are downloaded from
github.com/google/fonts into tools/fonts/ on first run.
"""

import pathlib
import urllib.request

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "tools" / "fonts"
OUT = ROOT / "Jess_Moore_CV.pdf"

FONTS = {
    "Playfair": "playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf",
    "Serif": "sourceserif4/SourceSerif4%5Bopsz,wght%5D.ttf",
    "Serif-Italic": "sourceserif4/SourceSerif4-Italic%5Bopsz,wght%5D.ttf",
}
FONT_BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/"

TEXT = HexColor("#1A1A1A")
MUTED = HexColor("#8A8178")
ACCENT = HexColor("#C0502E")

PAGE_W, PAGE_H = 612, 792  # US Letter
LEFT, RIGHT, INDENT = 54, 558, 62

# (title, years, company, description lines)
# company is a string, or a list of (text, font, size) runs for mixed styling.
ROLES = [
    ("Founder", "2025 · Present",
     [("Lattice Research  · ", "Serif-Italic", 7.5),
      ("latticeresearch.co", "Serif-Italic", 6.5)],
     ["Built and operate a financial analytics platform featuring live macro dashboards and geopolitical risk models.",
      "Designed structured AI research workflows with domain-specific evaluation frameworks and quality controls."]),
    ("Program Director", "2026", "Sunbury Urban Farm",
     ["Collaborated to run the Farm Chef curriculum at a summer camp on the farm.",
      "Created recipes and led 16 children aged 8–12 through the cooking process for ten weeks."]),
    ("Swim Coach", "2025 · Present", "Worthington Swim Club",
     ["Coach age group club swimmers and teach swim lessons."]),
    ("Graphics Specialist", "2011 · 2022", "American Chemical Society",
     ["Designed cover graphics for 70+ international chemistry journals, collaborating directly with scientists worldwide.",
      "Managed a large-scale digital asset library spanning thousands of images and issues."]),
    ("Farm Market Associate", "2012 · Present",
     [("Tilley Farmstead", "Serif-Italic", 7), (" 2012–Pres  ·  ", "Serif", 6),
      ("City Folks Farm Shop", "Serif-Italic", 7), (" 2024–25  ·  ", "Serif", 6),
      ("Beechwold Farm Market", "Serif-Italic", 7), (" 2023–24", "Serif", 6)],
     ["Sold local and heirloom produce at farmers markets and neighborhood farm shops for over a decade."]),
    ("Public Relations Consultant", "2011 · 2014", "Strider Sports International",
     ["Wrote and distributed press releases. Managed website and social media presence."]),
    ("Director of Communications", "2009 · 2011", "National Bicycle League",
     ["Managed print and online communications for the national BMX sanctioning body. Secured sponsorships and organized events."]),
    ("Editor & Art Director", "2005 · 2011", "BMX Today Magazine",
     ["Published monthly magazine. Solicited advertising, created content for print and web, designed marketing materials."]),
]

EDUCATION = ("BA Design", "University of Notre Dame", "2000 · 2004")

COMMUNITY = [
    ("Farmers Market Advisory Board", "2013 · 2017"),
    ("Resource Pantry Board of Directors", "2014 · 2016"),
    ("High School Ultimate Frisbee Coach", "2010 · 2012"),
]

INTERESTS = "capital markets  ·  AI systems  ·  permaculture  ·  cooking"


def register_fonts():
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    for name, path in FONTS.items():
        local = FONT_DIR / f"{name}.ttf"
        if not local.exists():
            urllib.request.urlretrieve(FONT_BASE + path, local)
        pdfmetrics.registerFont(TTFont(name, str(local)))


def build():
    register_fonts()
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Jess Moore — CV")
    c.setAuthor("Jess Moore")

    # All y values below are baselines measured from the top of the page.
    def text(x, y, s, font, size, color):
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawString(x, PAGE_H - y, s)

    def right(y, s, font, size, color=MUTED):
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawRightString(RIGHT, PAGE_H - y, s)

    text(LEFT, 50.4, "Jess Moore", "Playfair", 26, TEXT)
    text(LEFT, 66.4, "jess at moore dot lol", "Serif-Italic", 8, MUTED)
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.2)
    c.line(LEFT, PAGE_H - 79.4, LEFT + 40, PAGE_H - 79.4)

    text(LEFT, 107.4, "EXPERIENCE", "Playfair", 6.5, MUTED)
    y = 123.4
    for title, years, company, lines in ROLES:
        text(LEFT, y, title, "Playfair", 11, TEXT)
        right(y - 1, years, "Serif", 7)
        y += 9
        runs = [(company, "Serif-Italic", 7.5)] if isinstance(company, str) else company
        x = INDENT
        for s, font, size in runs:
            text(x, y, s, font, size, MUTED)
            x += pdfmetrics.stringWidth(s, font, size)
        y += 12
        for i, line in enumerate(lines):
            if i:
                y += 11.6
            text(INDENT, y, line, "Serif", 8, TEXT)
        y += 25.6

    y += 2
    text(LEFT, y, "EDUCATION", "Playfair", 6.5, MUTED)
    y += 14
    degree, school, years = EDUCATION
    text(LEFT, y, degree, "Playfair", 10, TEXT)
    text(LEFT + pdfmetrics.stringWidth(degree, "Playfair", 10) + 10, y, school, "Serif-Italic", 7.5, MUTED)
    right(y - 1, years, "Serif", 7)

    y += 20
    text(LEFT, y, "WORTHINGTON · OH", "Playfair", 6.5, MUTED)
    y += 12
    for i, (item, years) in enumerate(COMMUNITY):
        if i:
            y += 13
        text(LEFT, y, item, "Serif", 7.5, TEXT)
        right(y - 1, years, "Serif", 6.5)

    y += 25
    text(LEFT, y, INTERESTS, "Serif-Italic", 7.5, MUTED)

    c.showPage()
    c.save()
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()

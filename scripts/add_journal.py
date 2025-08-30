import os, sys, fitz  # PyMuPDF

IN_PATH  = os.getenv("PDF_PATH", "source.pdf")
OUT_DIR  = "output"
OUT_PATH = os.path.join(OUT_DIR, "journaling.pdf")

RIGHT_IN = float(os.getenv("RIGHT_MARGIN_IN", "3"))
ORIENT   = os.getenv("ORIENTATION", "portrait").lower()

# If you want the "Chapters" corner link to jump to a different page,
# set CHAPTERS_PAGE to a 0-based index via repo secret or edit here.
CHAPTERS_PAGE = int(os.getenv("CHAPTERS_PAGE", "0"))

def fail(msg):
    print("ERROR:", msg)
    sys.exit(1)

if not os.path.exists(IN_PATH):
    fail(f"Input PDF not found: {IN_PATH}")

os.makedirs(OUT_DIR, exist_ok=True)

margin = int(RIGHT_IN * 72)         # inches → points
rotate_landscape = (ORIENT == "landscape")

try:
    doc = fitz.open(IN_PATH)
except Exception as e:
    fail(f"Could not open PDF: {e}")

# Basic sanity log
print(f"Opened: {IN_PATH} ({doc.page_count} pages)")
print(f"Right margin (in): {RIGHT_IN}  →  {margin} pt")
print(f"Orientation: {ORIENT}  (rotate portrait pages? {rotate_landscape})")

for p in doc:
    # Rotate portrait pages if landscape requested (preserves links)
    if rotate_landscape and p.rect.height > p.rect.width:
        p.set_rotation(90)

    r = p.rect  # refresh after rotation
    x = r.x1 - margin

    # Vertical divider line in the margin area
    p.draw_line(fitz.Point(x, r.y0 + 12), fitz.Point(x, r.y1 - 12), width=0.6)

    # Corner “Home” (top-left) → page 1 (index 0)
    p.insert_text(
        fitz.Point(r.x0 + 18, r.y0 + 18),
        "Home",
        fontsize=8,
        color=(0, 0, 0),
    )
    p.insert_link({
        "kind": fitz.LINK_GOTO,
        "from": fitz.Rect(r.x0 + 12, r.y0 + 10, r.x0 + 70, r.y0 + 26),
        "page": 0
    })

    # Corner “Chapters” (top-right) → CHAPTERS_PAGE (default 0)
    p.insert_text(
        fitz.Point(r.x1 - 80, r.y0 + 18),
        "Chapters",
        fontsize=8,
        color=(0, 0, 0),
    )
    p.insert_link({
        "kind": fitz.LINK_GOTO,
        "from": fitz.Rect(r.x1 - 84, r.y0 + 10, r.x1 - 12, r.y0 + 26),
        "page": CHAPTERS_PAGE
    })

try:
    doc.save(OUT_PATH)
except Exception as e:
    fail(f"Could not save output PDF: {e}")

print("Saved:", OUT_PATH)

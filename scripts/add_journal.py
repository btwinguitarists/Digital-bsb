import os
import fitz  # PyMuPDF

IN_PDF = "work/base.pdf"
OUT_PDF = "work/journaling.pdf"

right_in = float(os.environ.get("RIGHT_MARGIN_IN", "3.0"))
orientation = os.environ.get("ORIENTATION", "landscape").lower()
margin = int(right_in * 72)

doc = fitz.open(IN_PDF)

# Rotate pages so the extra margin appears on the right when using landscape
if orientation == "landscape":
    for p in doc:
        if p.rect.height > p.rect.width:
            p.set_rotation(90)

for p in doc:
    r = p.rect
    x = r.x1 - margin
    # vertical divider
    p.draw_line(fitz.Point(x, r.y0 + 12), fitz.Point(x, r.y1 - 12), color=(0, 0, 0), width=0.7)
    # "Home" label + hotspot to page 1 (index 0); preserves all existing links
    p.insert_text(fitz.Point(r.x0 + 18, r.y0 + 22), "Home", fontsize=8, color=(0.3, 0.3, 0.3))
    p.insert_link({
        "kind": fitz.LINK_GOTO,
        "from": fitz.Rect(r.x0 + 12, r.y0 + 10, r.x0 + 75, r.y0 + 28),
        "page": 0
    })

doc.save(OUT_PDF)
print("Saved", OUT_PDF)

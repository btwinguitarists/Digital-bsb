# scripts/add_journal.py
# Adds a right-side journaling gutter + a thin divider + a "Home" hotspot (keeps all existing links)
import argparse, fitz

ap = argparse.ArgumentParser(description="Add true right margin (journal gutter) and divider.")
ap.add_argument("--in_pdf", required=True, help="input PDF")
ap.add_argument("--out_pdf", required=True, help="output PDF")
ap.add_argument("--right_in", dest="right_in", default="3.0", help="right margin (inches)")
args = ap.parse_args()

right = float(args.right_in)
margin = int(right * 72)  # 72pt per inch

doc = fitz.open(args.in_pdf)
for p in doc:
    r = p.rect
    x = r.x1 - margin
    # divider line 0.5pt, inset 12pt from top/bottom
    p.draw_line(fitz.Point(x, r.y0 + 12), fitz.Point(x, r.y1 - 12), color=(0, 0, 0), width=0.5)
    # "Home" label + hotspot to first page
    p.insert_text(fitz.Point(r.x0 + 18, r.y0 + 22), "Home", fontsize=8, color=(0.3, 0.3, 0.3))
    p.insert_link({
        "kind": fitz.LINK_GOTO,
        "from": fitz.Rect(r.x0 + 12, r.y0 + 10, r.x0 + 75, r.y0 + 28),
        "page": 0
    })

doc.save(args.out_pdf)
print("Wrote", args.out_pdf)

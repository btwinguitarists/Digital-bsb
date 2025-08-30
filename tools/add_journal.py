import os, sys, fitz  # PyMuPDF

src = os.environ.get("SRC_PDF", "bsb.pdf")
right_in = float(os.environ.get("RIGHT_IN", "3.0"))
add_div = os.environ.get("DIVIDER", "yes").lower() == "yes"
add_home = os.environ.get("HOME", "yes").lower() == "yes"

margin = int(round(right_in * 72))  # inches -> points

if not os.path.exists(src):
    print(f"ERROR: missing {src}", file=sys.stderr)
    sys.exit(2)

doc = fitz.open(src)

for page in doc:
    r = page.rect
    # expand media box to the RIGHT (keeps all existing links/anchors where they are)
    page.set_mediabox(fitz.Rect(r.x0, r.y0, r.x1 + margin, r.y1))

    if add_div:
        page.draw_line(fitz.Point(r.x1, r.y0 + 12), fitz.Point(r.x1, r.y1 - 12),
                       color=(0, 0, 0), width=0.5)

    if add_home:
        page.insert_text(fitz.Point(r.x0 + 18, r.y0 + 22), "Home",
                         fontsize=8, color=(0.2, 0.2, 0.2))
        page.insert_link({
            "kind": fitz.LINK_GOTO,
            "from": fitz.Rect(r.x0 + 12, r.y0 + 10, r.x0 + 64, r.y0 + 28),
            "page": 0
        })

doc.save("journaling.pdf")
print("Wrote journaling.pdf")

#!/usr/bin/env python3
import argparse, os
import fitz  # PyMuPDF

def main():
    ap = argparse.ArgumentParser(description="Add right-side journaling gutter and keep links.")
    ap.add_argument("--in",  dest="in_pdf",  required=True, help="Input PDF")
    ap.add_argument("--out", dest="out_pdf", required=True, help="Output PDF")
    ap.add_argument("--right-in", dest="right_in", default="3.0", help="Right margin (inches)")
    ap.add_argument("--orientation", dest="orientation", choices=["portrait","landscape"], default="portrait")
    args = ap.parse_args()

    right_in = float(args.right_in)
    margin_pt = int(round(right_in * 72))  # 72 pt/in

    doc = fitz.open(args.in_pdf)

    # If you want the writing space to be the "right side" in landscape, rotate pages first:
    if args.orientation == "landscape":
        for page in doc:
            # Only rotate if page is portrait-ish to keep already-landscape pages intact
            if page.rect.height > page.rect.width:
                page.set_rotation(90)

    # Draw divider and add a "Home" hotspot (back to page 1)
    for page in doc:
        r = page.rect
        x = r.x1 - margin_pt

        # Vertical divider line (slim)
        page.draw_line(fitz.Point(x, r.y0 + 12), fitz.Point(x, r.y1 - 12), color=(0, 0, 0), width=0.5)

        # "Home" label + link back to page 1 (index 0)
        page.insert_text(
            fitz.Point(r.x0 + 18, r.y0 + 22),
            "Home",
            fontsize=8,
            color=(0.3, 0.3, 0.3),
        )
        page.insert_link({
            "kind": fitz.LINK_GOTO,
            "from": fitz.Rect(r.x0 + 12, r.y0 + 10, r.x0 + 75, r.y0 + 28),
            "page": 0
        })

    os.makedirs(os.path.dirname(args.out_pdf), exist_ok=True)
    doc.save(args.out_pdf)
    print("Saved:", args.out_pdf)

if __name__ == "__main__":
    main()

# scripts/validate_epub.py
import sys, zipfile

if len(sys.argv) < 2:
    print("usage: validate_epub.py <path-to-epub>")
    sys.exit(2)

p = sys.argv[1]
try:
    with zipfile.ZipFile(p) as z:
        bad = z.testzip()
        if bad:
            print("EPUB has a corrupt member:", bad)
            sys.exit(1)
    print("EPUB OK:", p)
except Exception as e:
    print("ERROR: not a valid EPUB/ZIP:", e)
    sys.exit(1)

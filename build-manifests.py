#!/usr/bin/env python3
"""
Erzeugt die Datei-Listen (Manifeste), die die Website braucht, um Bilder aus
/gallery und Events aus /events automatisch anzuzeigen — ohne dass ihr
Dateinamen im HTML eintragen müsst.

Warum überhaupt nötig? Eine reine HTML/JS-Website kann Ordnerinhalte nicht
selbst auflisten (das verhindern Browser & GitHub Pages aus Sicherheitsgründen).
Deshalb liest dieses Skript die Ordner lokal aus und schreibt zwei kleine
JSON-Dateien, die die Website dann per fetch() lädt.

Ausführen, NACHDEM ihr Bilder in /gallery oder Events (.txt) in /events
hinzugefügt/entfernt habt — und BEVOR ihr zu GitHub pusht:

    python3 build-manifests.py
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
GALLERY_DIR = os.path.join(ROOT, "gallery")
EVENTS_DIR = os.path.join(ROOT, "events")
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

def build_gallery_manifest():
    if not os.path.isdir(GALLERY_DIR):
        print("Ordner /gallery nicht gefunden — übersprungen.")
        return
    files = sorted(
        f for f in os.listdir(GALLERY_DIR)
        if f.lower().endswith(IMAGE_EXTENSIONS)
    )
    out_path = os.path.join(GALLERY_DIR, "images.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(files, f, ensure_ascii=False, indent=2)
    print(f"gallery/images.json geschrieben ({len(files)} Bild(er)).")

def build_events_manifest():
    """
    Jedes Event besteht aus einer YYYYMMDD_NAME.txt und optional einem Plakat
    mit demselben Dateinamen (z. B. 20260912_Sommerfest.jpg). Das Plakat wird
    automatisch anhand des Namens zugeordnet — dafür muss im .txt nichts
    eingetragen werden.
    """
    if not os.path.isdir(EVENTS_DIR):
        print("Ordner /events nicht gefunden — übersprungen.")
        return
    entries = os.listdir(EVENTS_DIR)
    txt_files = sorted(f for f in entries if f.lower().endswith(".txt"))
    image_files = [f for f in entries if f.lower().endswith(IMAGE_EXTENSIONS)]

    events = []
    for txt in txt_files:
        base = os.path.splitext(txt)[0]
        plakat = next((img for img in image_files if os.path.splitext(img)[0] == base), None)
        events.append({"txt": txt, "plakat": plakat})

    out_path = os.path.join(EVENTS_DIR, "events.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    with_poster = sum(1 for e in events if e["plakat"])
    print(f"events/events.json geschrieben ({len(events)} Event(s), {with_poster} mit Plakat).")

if __name__ == "__main__":
    build_gallery_manifest()
    build_events_manifest()

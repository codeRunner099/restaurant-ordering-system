# Restaurant Sonnenteller – Bestellsystem

Ein kleines, aber realistisches Restaurant-Bestellsystem mit Flask und SQLite.

## Schnellstart

1. Virtuelle Umgebung erstellen und aktivieren
2. Abhängigkeiten installieren
3. Datenbank erstellen
4. Server starten

### Beispielbefehle

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

python3 create_db.py

python3 app.py
```

Öffne danach im Browser:

`http://localhost:5000`

## Funktionen

- Öffentliche Startseite mit Überblick
- Speisekarte mit Kategorien und Gerichten
- Warenkorb mit Mengenänderung und Leeren
- Bestellung mit Name und Tischnummer absenden
- Einfache Küchenübersicht mit Bestellliste

---

# Restaurant Sonnenteller – Ordering System

A small but realistic restaurant ordering system built with Flask and SQLite.

## Quickstart

1. Create and activate a virtual environment
2. Install dependencies
3. Create the database
4. Start the server

### Example commands

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

python3 create_db.py

python3 app.py
```

Then open in the browser:

`http://localhost:5000`

## Features

- Public landing page
- Menu with categories and items
- Cart with quantity update and clear
- Place order with name and table number
- Simple kitchen overview with order list
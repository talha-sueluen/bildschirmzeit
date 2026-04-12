# 📱 Bildschirmzeit Dashboard

Ein interaktives Dashboard zur Auswertung persönlicher Bildschirmzeit-Daten über mehrere Wochen. Visualisiert tägliche Nutzungszeiten, meistgenutzte Apps und wöchentliche Trends.

---

## Installation

```bash
pip install -r requirements.txt
```

## App starten

```bash
streamlit run app.py
```

---

## Übersicht der Inhalte

### Kennzahlen
Vier Karten am oberen Rand zeigen auf einen Blick: gesamte Bildschirmzeit, Tagesdurchschnitt, längster Tag und die meistgenutzte App — jeweils für den ausgewählten Zeitraum.

### Tägliche Bildschirmzeit
Area-Chart mit der Bildschirmzeit pro Tag über den gesamten Zeitraum. Zeigt Schwankungen und Ausreißer auf einen Blick.

### App-Aufteilung
Donut-Chart mit dem Anteil der einzelnen Apps an der Gesamtnutzung (Top 7 + Sonstige).

### Ø Bildschirmzeit pro Wochentag
Balkendiagramm mit der durchschnittlichen Bildschirmzeit je Wochentag — farblich nach Intensität abgestuft.

### Top Apps
Horizontales Balkendiagramm mit den meistgenutzten Apps nach Gesamtminuten im ausgewählten Zeitraum.

### Wochenvergleich *(nur bei „Alle")*
Kombiniertes Diagramm: Balken für die wöchentliche Gesamtzeit, Linie für den täglichen Durchschnitt je Woche.

### App-Trends nach Woche *(nur bei „Alle")*
Liniendiagramm der Top-5-Apps über alle vier Wochen — zeigt, welche Apps zu- oder abgenommen haben.

### Wochendaten
Tabellenansicht der Rohdaten, wochenweise filterbar. Zeigt Datum, Gesamtbildschirmzeit und die Top-5-Apps pro Tag.

---

## Datenformat

Die CSV-Dateien müssen im **Projektordner** liegen (nicht in einem Unterordner) und dem folgenden Namensschema entsprechen:

```
woche_1.csv
woche_2.csv
woche_3.csv
...
```

Jede Datei muss folgende Spalten enthalten:

| Spalte | Beschreibung |
|---|---|
| `datum` | Datum im Format `YYYY-MM-DD` |
| `gesamte bildschirmzeit` | Gesamtzeit in Minuten |
| `app1_adi` – `app5_adi` | Name der App (Platz 1–5) |
| `app1_sure` – `app5_sure` | Nutzungszeit der App in Minuten |

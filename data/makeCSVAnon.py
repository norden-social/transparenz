import csv
import datetime
import re
import os


# Eingabedatei öffnen
with open("norden_social.csv", "r") as f:
    reader = csv.reader(f, delimiter=";")
    
    # Überschriften auslesen
    headers = next(reader)

    # Spaltennummern der gewünschten Spalten ermitteln
    date_column = headers.index("Datum")
    purpose_column = headers.index("Name")
    amount_column = headers.index("Betrag")

    # Ausgabedatei öffnen
    with open("data.csv", "w", newline="") as g:
        writer = csv.writer(g, delimiter=';')

        # Überschriften schreiben
        writer.writerow(["Datum", "Art", "Betrag"])

        # Durch alle Zeilen iterieren
        for row in reader:

            # Wert für "Betrag" in Gleitkommazahl umwandeln
            amount = row[amount_column]
            amount = amount.replace(",", ".")
            amount = float(amount)

            # Wert für "Art" anonymisieren
            if amount > 0:
                art = "Support"
            else:
                purpose = row[purpose_column]
                if re.search(r"\bDeepl\b", purpose):
                    art = "Deepl"
                elif re.search(r"\bmailjet\b", purpose):
                    art = "Mailjet"
                else:
                    art = "Serverkosten"

            # Wert für "Datum" in gewünschtes Format konvertieren
            date = row[date_column]
            date = datetime.datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")

            # Amount als String
            amount = row[amount_column]
            amount = str(amount)
            amount = amount.replace(".", ",")

            # Zeile schreiben
            writer.writerow([date, art, amount])

# Eingabedatei löschen
os.remove("norden_social.csv")

# Description Updaten über API
# Autor: Ralph Belfiore, pro4bizz GmbH
# Stand: 21.12.2020
###########################################
import requests
import sys
import os.path

daten = []
trenner = ","

if len(sys.argv) - 1 < 2:
    print("Bitte Aufruf: qr_description.py IP Dateiname")
    sys.exit()
fname = sys.argv[2]
if not os.path.isfile(fname):
    print("Datei existiert nicht!")
    sys.exit()

#csvdatei = IDs und Description von Logsourcen als csv datei. Bei diesen IDs wird die Description aktualisiert!
csvdatei = sys.argv[2]

# Zum Lesen öffenen und in Liste speichern
file = open(csvdatei)
daten = file.readlines()
file.close()
# Ende Einlesen csv #######################

# Text-Datei id, beschreibung in QRadar-Format umbauen und in neuem String speichern
i = 0
# Ersten Eintrag vorlesen wegen curly braket am Anfang
qr_zeile = daten[i].split(',')
daten_qr = "{" + "\"" + "id\"" + ":" + qr_zeile[i] + ", " + """"description\"""" + ":" + qr_zeile[i+1] + "}" + ","
i += 1
# Bis zum Ende der Liste in String-Format für QRadar API Übergabe output schreiben
while i < len(daten):
    qr_zeile = daten[i].split(',')
    lsid = "{" + "\"" + "id\"" + ":" + qr_zeile[0] + trenner
    lsdesc = """"description\"""" + ":" + qr_zeile[1] + "}"
#    print(lsid,lsdesc)
    if i < len(daten) -1:
        daten_qr += lsid + lsdesc + trenner
    else:
        daten_qr += lsid + lsdesc
    i += 1
# Ende Daten umschreiben ########################
# Finales QRadar Datenformat als output formatieren
daten_qr = "[" + daten_qr + "]"

# Übergabe der Daten für curl- Aufruf zu QRadar
data = daten_qr
# QRadar-Vorbereitung: Übergabe-Parameter von Kommandozeile zuweisen
#qradarip = '172.16.127.208'
qradarip = sys.argv[1]
#Token für API-Zugriff
api_token = 'bce9e705-4757-49d7-805b-7dae0c096ffb'
auth_header = {'SEC':api_token, 'content-type':'application/json'}
url = 'https://' + qradarip + '/api/config/event_sources/log_source_management/log_sources'

# Curl-Aufruf
response = requests.patch(url, headers=auth_header, data=data, verify=False)    
#print(response.json())
print("Daten: " + data + " auf " + url + " erfolgreich aktualisiert!")

from music21 import stream, note, meter, tempo, metadata
import cv2
import numpy as np

def find_note_heads(image_path):
    # Lade das Bild
    image = cv2.imread(image_path)

# Konvertiere das Bild in Graustufen
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Wende den Schwellenwert an, um binäres Bild zu erhalten
    _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)

    # Finde Konturen im binären Bild
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Finde die Hauptkomponente (die größte)
    largest_contour = max(contours, key=cv2.contourArea)

    # Schätze die Linienpositionen mit der Hough-Transformation für Linien
    lines = cv2.HoughLinesP(binary_image, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    # Extrahiere die y-Koordinaten der Linien
    line_y_coordinates = [line[0][1] for line in lines]

    # Sortiere die y-Koordinaten, um die Notenlinien zu erhalten
    sorted_line_y_coordinates = sorted(line_y_coordinates)

    # Definiere einen Bereich um jede Notenlinie für die Suche nach Notenköpfen
    region_of_interest_height = 20
    note_head_regions = []

    for y_coord in sorted_line_y_coordinates:
        roi = binary_image[y_coord:y_coord + region_of_interest_height, :]
        note_head_regions.append(roi)

    # Zeige die gefundenen Note-Head-Regionen
    for idx, note_head_region in enumerate(note_head_regions):
        cv2.imshow(f'Note Head {idx + 1}', note_head_region)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def extract_melody_with_duration(image_path, output_midi_path='output.mid'):
    # Lade das Bild
    image = cv2.imread(image_path)

    # Konvertiere das Bild in Graustufen
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Wende den Schwellenwert an, um binäres Bild zu erhalten
    _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)

    # Finde Konturen im binären Bild
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Erstelle ein leeres Notenblattobjekt
    melody_score = stream.Score()

    # Füge Metadaten hinzu (optional)
    melody_score.metadata = metadata.Metadata()
    melody_score.metadata.title = 'Extracted Melody'

    # Beispielnoten hinzufügen (ersetzen Sie dies durch Ihre eigene Melodieextraktionslogik)
    melody_stream = stream.Part()
    melody_stream.append(tempo.MetronomeMark(number=120))

    # Annahme: Notenregionen wurden bereits identifiziert und analysiert
    # Ersetzen Sie die folgende Logik durch Ihre eigene Extraktionslogik
    note_data = [
        {'pitch': 'C4', 'duration': 1.0},
        {'pitch': 'D4', 'duration': 0.5},
        {'pitch': 'E4', 'duration': 0.5},
        # ... Weitere Notendaten hier ...
    ]

    for contour in contours:
        # Berechne das Begrenzungsrechteck um die Kontur
        x, y, w, h = cv2.boundingRect(contour)

        # Füge die Note zur Melodiestimme hinzu (vereinfachte Logik)
        if w > 10 and h > 10:
            note_pitch = "C4"  # Hier sollte die Logik zur Bestimmung der Note basierend auf der Position stehen
            duration = 0.5
            note_data.append({'pitch': note_pitch, 'duration': duration})

    for data in note_data:
        note_stream = note.Note(data['pitch'], quarterLength=data['duration'])
        melody_stream.append(note_stream)

    # Füge die Melodiestimme zum Notenblatt hinzu
    melody_score.insert(0, melody_stream)

    # Speichere das MIDI-Format
    melody_score.write('midi', fp=output_midi_path)

# Beispielaufruf
image_path = 'stille_nacht.jpg'
find_note_heads(image_path)

output_midi_path = 'output.mid'
extract_melody_with_duration(image_path, output_midi_path)
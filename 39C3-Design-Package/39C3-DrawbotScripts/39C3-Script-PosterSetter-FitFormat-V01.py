#!/usr/bin/env python3
"""
DrawBot Script für variable Fonts mit width axis
Berechnet die optimale width für maximale Textbreite
"""

from drawBot import *

# KONFIGURATION - HIER ANPASSEN
FONT_PATH = "~/Downloads/Kario-39C3-VariableFont/Desktop/KarioDuplexVar-Roman.ttf"  # Pfad zu deinem variablen Font
INPUT_TEXT = "Kario Variable"  # Hier deinen Text eingeben
PAPER_FORMAT = "A4"  # "A4" oder "A3"
MARGIN = 40  # Margin in Punkten
FONT_SIZE_REDUCTION = 0.9  # Faktor um Schriftgröße zu reduzieren (0.9 = 10% kleiner)
Y_SHIFT = -30  # Zusätzliche Y-Verschiebung in Punkten (negativ = nach unten)

# Typographische Metriken deines Fonts
CAP_HEIGHT = 700  # Cap Height in Font-Units
DESCENDER = -98   # Descender in Font-Units (negativ)

# Papierformate (Querformat, in Punkten)
PAPER_FORMATS = {
    "A4": (842, 595),  # A4 Querformat
    "A3": (1190, 842)  # A3 Querformat
}

# Test width-Werte
TEST_WIDTHS = [30, 50, 100, 120, 160]

def get_document_dimensions(format_name="A4", margin=50):
    """Dokument-Dimensionen berechnen"""
    width, height = PAPER_FORMATS[format_name]
    return width - 2*margin, height - 2*margin, margin

def measure_text_width(text, font_path, font_size, width_value):
    """Misst die Textbreite bei gegebener width"""
    # Font mit Variationen laden
    font(font_path)
    fontSize(font_size)
    fontVariations(wdth=width_value, wght=900, opsz=140)
    
    return textSize(text)[0]

def calculate_optimal_font_size(text, font_path, available_height, width_value=100):
    """Berechnet die optimale Schriftgröße basierend auf Cap Height und Descender"""
    # Berechne die tatsächliche typographische Höhe
    # Cap Height - Descender (Descender ist negativ, daher Subtraktion)
    typo_height_units = CAP_HEIGHT - DESCENDER  # z.B. 700 - (-98) = 798 Units
    
    # Berechne die Schriftgröße basierend auf verfügbarer Höhe
    # font_size / 1000 * typo_height_units = available_height
    optimal_size = (available_height * 1000) / typo_height_units
    
    # Reduziere die Schriftgröße um den Sicherheitsfaktor
    return optimal_size * FONT_SIZE_REDUCTION

def calculate_optimal_width(text, font_path, font_size, target_width):
    """Berechnet die optimale width für die Zielbreite"""
    # Messe Textbreiten bei verschiedenen width-Werten
    widths = []
    text_widths = []
    
    for width_val in TEST_WIDTHS:
        text_width = measure_text_width(text, font_path, font_size, width_val)
        widths.append(width_val)
        text_widths.append(text_width)
        print(f"Width {width_val}: Textbreite = {text_width:.1f}pt")
    
    # Lineare Interpolation zwischen den Messpunkten
    optimal_width = None
    
    # Finde die beiden Messpunkte, zwischen denen die Zielbreite liegt
    for i in range(len(text_widths) - 1):
        if text_widths[i] <= target_width <= text_widths[i + 1]:
            # Lineare Interpolation
            x1, y1 = text_widths[i], widths[i]
            x2, y2 = text_widths[i + 1], widths[i + 1]
            
            # y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
            optimal_width = y1 + (target_width - x1) * (y2 - y1) / (x2 - x1)
            break
    
    # Falls Zielbreite außerhalb des Bereichs liegt, verwende nächsten Punkt
    if optimal_width is None:
        if target_width < text_widths[0]:
            optimal_width = widths[0]  # Kleinste width
        else:
            optimal_width = widths[-1]  # Größte width
    
    return optimal_width, list(zip(widths, text_widths))

def create_final_layout(input_text, font_path, optimal_width, font_size, 
                       paper_format, margin):
    """Erstellt das finale Layout mit der berechneten width"""
    # Neues Dokument erstellen
    doc_width, doc_height = PAPER_FORMATS[paper_format]
    newPage(doc_width, doc_height)
    
    available_width, available_height, margin_size = get_document_dimensions(paper_format, margin)
    
    # Font mit optimaler width setzen
    font(font_path)
    fontSize(font_size)
    fontVariations(wdth=optimal_width, wght=900, opsz=140)
    
    # Berechne die tatsächliche typographische Höhe des Texts in Punkten
    typo_height_points = font_size * (CAP_HEIGHT - DESCENDER) / 1000
    
    # Textbreite für Zentrierung messen
    text_width, _ = textSize(input_text)
    
    # Text horizontal und vertikal zentriert positionieren + optionaler Y-Shift
    x = margin_size + (available_width - text_width) / 2  # Horizontal zentriert
    y = margin_size + (available_height - typo_height_points) / 2 + Y_SHIFT  # Vertikal zentriert
    
    # Verschiebe Y um die Descender-Höhe nach oben, damit Baseline korrekt sitzt
    y += font_size * abs(DESCENDER) / 1000
    
    print(f"Debug - Font Size: {font_size:.1f}pt")
    print(f"Debug - Text Width: {text_width:.1f}pt") 
    print(f"Debug - Position: x={x:.1f}, y={y:.1f}")
    print(f"Debug - Typo Height: {typo_height_points:.1f}pt")
    
    # Text zeichnen - verwende einfache text() Funktion statt textBox
    fill(0)  # Schwarz
    text(input_text, (x, y))

def main():
    """Hauptfunktion"""
    # Parameter aus Konfiguration verwenden
    input_text = INPUT_TEXT
    paper_format = PAPER_FORMAT.upper()
    margin = MARGIN
    
    if paper_format not in PAPER_FORMATS:
        print("Ungültiges Format, verwende A4")
        paper_format = "A4"
    
    print(f"Text: '{input_text}'")
    print(f"Format: {paper_format}")
    print(f"Margin: {margin}pt")
    
    # Verfügbare Dimensionen berechnen
    available_width, available_height, margin_size = get_document_dimensions(paper_format, margin)
    
    print(f"\nVerfügbare Breite: {available_width:.1f}pt")
    print(f"Verfügbare Höhe: {available_height:.1f}pt")
    
    # Optimale Schriftgröße für maximale Höhe berechnen
    optimal_font_size = calculate_optimal_font_size(input_text, FONT_PATH, 
                                                   available_height)
    print(f"Optimale Schriftgröße: {optimal_font_size:.1f}pt")
    
    # Optimale width für maximale Breite berechnen
    optimal_width, measurements = calculate_optimal_width(input_text, FONT_PATH, 
                                                         optimal_font_size, 
                                                         available_width)
    
    print(f"\nMessungen:")
    for width_val, text_width in measurements:
        print(f"  Width {width_val}: {text_width:.1f}pt")
    
    print(f"\nOptimale Width: {optimal_width:.1f}")
    
    # Finales Layout erstellen
    create_final_layout(input_text, FONT_PATH, optimal_width, 
                       optimal_font_size, paper_format, margin)
    
    # PDF speichern
    output_name = f"output_{paper_format}_margin{margin}.pdf"
    saveImage(output_name)
    print(f"PDF gespeichert: {output_name}")

if __name__ == "__main__":
    main()

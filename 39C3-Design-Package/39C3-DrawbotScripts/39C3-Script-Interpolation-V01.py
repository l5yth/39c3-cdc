# === EDITIERBARE EINSTELLUNGEN ===

fontPath = "~/Downloads/Kario-39C3-VariableFont/Desktop/KarioDuplexVar-Roman.ttf"
word = "UNIWIDTH/DUPLEX"
numLines = 7

minWeight = 10
maxWeight = 100
widthValue = 76

canvasWidth = 1000
canvasHeight = 1000
margin = 50

# <<< Text- und Hintergrundfarbe (RGB 0-1)
backgroundColor = (0,0,0)  #black
textColor = (1,1,1)             #white

# <<< Zeilenabstand (1.0 = 100% der finalen Fontgröße)
lineSpacingFactor = 0.92

# <<< Vertikaler optischer Ausgleich (in Units, nach oben verschieben)
verticalOffset = 17


# === DRAWBOT SETUP ===

newPage(canvasWidth, canvasHeight)
fill(*backgroundColor)
rect(0, 0, canvasWidth, canvasHeight)

# === HILFSFUNKTION: Textbreite für eine bestimmte Zeile mit korrektem Weight-Verlauf messen ===

def getLineWidth(text, size, lineIndex):
    font(fontPath)
    fontSize(size)
    total = 0

    midIndex = (len(text) - 1) / 2
    startWeight = maxWeight - (maxWeight - minWeight) / (numLines - 1) * lineIndex
    endWeight = minWeight + (maxWeight - minWeight) / (numLines - 1) * lineIndex

    for charIndex, char in enumerate(text):
        if lineIndex == 0:
            weight = startWeight + (endWeight - startWeight) / (len(text) - 1) * charIndex
        elif lineIndex == numLines - 1:
            weight = startWeight + (endWeight - startWeight) / (len(text) - 1) * charIndex
        else:
            baseWeight = startWeight + (endWeight - startWeight) / (len(text) - 1) * charIndex
            distToMid = abs(charIndex - midIndex)
            maxBoost = (maxWeight - minWeight) / 2
            boost = maxBoost * (1 - (distToMid / midIndex) ** 2)
            boostFactor = 1 - abs(lineIndex - (numLines - 1) / 2) / ((numLines - 1) / 2)
            weight = baseWeight + boost * boostFactor

        weight = max(minWeight, min(maxWeight, weight))

        fontVariations(wght=weight, wdth=widthValue)
        advance, _ = textSize(char)
        total += advance
    return total

# === BERECHNUNG DER SKALIERUNG UND POSITION ===

testSize = 1000  # Temporäre Schriftgröße für Messungen

# Ermittel die maximale Breite aller Zeilen (wegen unterschiedlichem Weight-Verlauf)
maxTextWidth = max(getLineWidth(word, testSize, i) for i in range(numLines))
maxTextHeight = numLines * testSize * lineSpacingFactor

usableWidth = canvasWidth - 2 * margin
usableHeight = canvasHeight - 2 * margin

scaleFactor = min(usableWidth / maxTextWidth, usableHeight / maxTextHeight)
finalFontSize = testSize * scaleFactor
lineSpacing = finalFontSize * lineSpacingFactor

textBlockHeight = numLines * lineSpacing
startY = (canvasHeight + textBlockHeight) / 2 - lineSpacing + verticalOffset


# === TEXT ZEICHNEN ===

font(fontPath)
fontSize(finalFontSize)

midIndex = (len(word) - 1) / 2

for lineIndex in range(numLines):
    y = startY - lineIndex * lineSpacing

    # Zentriere pro Zeile genau anhand der gemessenen Breite mit finaler Größe und korrektem Weight-Verlauf
    lineWidth = getLineWidth(word, finalFontSize, lineIndex)
    x = (canvasWidth - lineWidth) / 2

    startWeight = maxWeight - (maxWeight - minWeight) / (numLines - 1) * lineIndex
    endWeight = minWeight + (maxWeight - minWeight) / (numLines - 1) * lineIndex

    for charIndex, char in enumerate(word):

        if lineIndex == 0:
            weight = startWeight + (endWeight - startWeight) / (len(word) - 1) * charIndex

        elif lineIndex == numLines - 1:
            weight = startWeight + (endWeight - startWeight) / (len(word) - 1) * charIndex

        else:
            baseWeight = startWeight + (endWeight - startWeight) / (len(word) - 1) * charIndex
            distToMid = abs(charIndex - midIndex)
            maxBoost = (maxWeight - minWeight) / 2
            boost = maxBoost * (1 - (distToMid / midIndex) ** 2)
            boostFactor = 1 - abs(lineIndex - (numLines - 1) / 2) / ((numLines - 1) / 2)
            weight = baseWeight + boost * boostFactor

        weight = max(minWeight, min(maxWeight, weight))

        fontVariations(wght=weight, wdth=widthValue)
        fill(*textColor)
        text(char, (x, y))

        advance, _ = textSize(char)
        x += advance

# <<< Aktiviert den PDF-Export (Pfad oben anpassen!)
saveImage("/Users/berndvolmer/Desktop/Desktop/Interpolation.pdf")

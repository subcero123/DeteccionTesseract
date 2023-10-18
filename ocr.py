import cv2
import pytesseract
# Cargar la imagen
image = cv2.imread('imagen.png')
# Convertir la imagen a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Realizar OCR
text = pytesseract.image_to_string(gray)

# Imprimir el texto extraído
print(text)

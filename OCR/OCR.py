import cv2
import pytesseract
image = cv2.imread('imagen2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
texto = pytesseract.image_to_string(gray)
print(texto)

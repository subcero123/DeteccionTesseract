import cv2
import pytesseract
import os
image = cv2.imread('imagen2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
text = pytesseract.image_to_string(gray)
print(text)

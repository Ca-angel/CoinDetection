import cv2
import numpy as np
import math

def scale_change(frame, scale = 0.4):
	width = int(frame.shape[1] * scale)
	height = int(frame.shape[0] * scale)
	dimensiones = (width, height)
	return cv2.resize(frame, dimensiones, interpolation=cv2.INTER_AREA)
	
cantidad_objetos = 0
i = 0
moneda_50 = 0
moneda_100 = 0
moneda_200 = 0
moneda_500 = 0
moneda_1000 = 0

#Lee imagen a trabajar
image = cv2.imread('c1.jpeg')

#Ajustar tamaño
img = scale_change(image)
image_copy = img.copy()

#Cambiar a escala de grises
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Ajustar difuminado
blur = cv2.GaussianBlur(gray, (7,7), 0)

#Deteccion de bordes
canny = cv2.Canny(blur, 15, 100)

# Encontrar los contornos en la imagen
contours , _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_image = img.copy()
contour_image = cv2.drawContours(contour_image,contours, -1, (0,255,0), 1)

x_centro = [None] * len(contours)
y_centro = [None] * len(contours)
distancias = [None] * len(contours)
proporciones = [None] * (len(contours) - 1)

# Iterar sobre los contornos encontrados
for contour in contours:
    # Calcular el centroide del contorno
    M = cv2.moments(contour)
    if M["m00"] != 0:
        centroid_x = int(M["m10"] / M["m00"])
        centroid_y = int(M["m01"] / M["m00"])
        # Dibujar un círculo en el centroide del objeto
        cv2.circle(contour_image, (centroid_x, centroid_y), 5, (0, 0, 255), -1)
        x_centro[cantidad_objetos] = centroid_x
        y_centro[cantidad_objetos] = centroid_y
        distancias[cantidad_objetos] = np.sqrt( (contours[cantidad_objetos][0][0][i] - x_centro[cantidad_objetos])**2 + (contours[cantidad_objetos][0][0][i+1] - y_centro[cantidad_objetos])**2 )
        cantidad_objetos += 1
        
while i < len(contours):
	if distancias[i] > 25 and distancias[i] < 30:
		moneda_50 += 1
	elif distancias[i] > 30 and distancias[i] < 33.2:
		moneda_100 += 1
	elif distancias[i] > 33.2 and distancias[i] < 35.5:
		moneda_200 += 1
	elif distancias[i] > 35.5 and distancias[i] < 39:
		moneda_500 += 1
	elif distancias[i] > 39:
		moneda_1000 += 1
	i += 1

#print(sorted(distancias))
print('Hay ', (50*moneda_50) + (100*moneda_100) + (200*moneda_200) + (500*moneda_500) + (1000*moneda_1000), ' pesos en la imagen.')
print('Monedas de 50: ', moneda_50, '\nMonedas de 100: ', moneda_100, '\nMonedas de 200: ', moneda_200, '\nMonedas de 500: ', moneda_500, '\nMonedas de 1000: ', moneda_1000 )
# Mostrar la imagen con los contornos y los centroides
cv2.imshow('Contornos', contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

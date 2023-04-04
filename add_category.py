list_category = [
	'Accesorios para Vehículos','Agro','Alimentos y Bebidas','Licores','Regalos','Animales y Mascotas','Antigüedades y Colecciones','Arte, Papelería y Mercería','Bebés',
'Belleza y Cuidado Personal','Celulares y Teléfonos','Computación','Consolas y Videojuegos','Construcción','Deportes y Fitness','Electrodomésticos','Electrónica, Audio y Video',
'Herramientas','Hogar y Muebles','Industrias y Oficinas','Inmuebles','Instrumentos Musicales','Juegos y Juguetes','Recuerdos, Piñatería y Fiestas','Ropa y Accesorios','Salud y Equipamiento Médico',
'Servicios','Otras categorías'
]

for i in list_category:
	import requests
	import json
	url = "http://localhost:9090/inventory/Save_Category/"
	payload = json.dumps({
	  "name": str(i)
	})
	headers = {
	  'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	print(response.text)


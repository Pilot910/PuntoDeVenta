import requests  # Librería para hacer solicitudes HTTP (GET, POST, etc.) a servidores o APIs

# URL base del backend PHP (donde se alojan los archivos .php que devuelven datos)
API_URL = "http://localhost/comicsmexico/backend/"

# API Key fija, debe coincidir exactamente con la definida en config.php del servidor PHP
API_KEY = "123456"

# ------------------------------
# Función para obtener la lista de cómics desde el backend
# ------------------------------
def get_comics():
    # Encabezados HTTP que se enviarán junto con la solicitud
    # Aquí se incluye la API Key en el campo "Authorization" usando el formato "Bearer <clave>"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    try:
        # Hace una solicitud GET al archivo get_comics.php en el servidor
        response = requests.get(f"{API_URL}get_comics.php", headers=headers)

        # Muestra el código de estado HTTP (por ejemplo, 200 si todo salió bien)
        print("STATUS:", response.status_code)

        # Muestra el texto exacto devuelto por PHP (útil para depurar si hay errores)
        print("TEXT:", response.text)

        # Si la respuesta fue exitosa (HTTP 200), intenta convertir el texto a formato JSON
        if response.status_code == 200:
            return response.json()  # Convierte la respuesta en un diccionario/lista de Python
        else:
            # Si no fue 200, devuelve una lista vacía (no hay datos)
            return []
    except Exception as e:
        # Si ocurre algún error (por ejemplo, el servidor no responde o no hay conexión)
        print("Error al conectar con API:", e)
        return []  # Devuelve lista vacía para evitar que el programa se detenga

# ------------------------------
# Función para obtener las portadas (covers) de un cómic específico
# ------------------------------
def get_covers(comic_id):
    # Construye la URL con los parámetros necesarios (API Key y ID del cómic)
    url = f"{API_URL}get_covers.php?api_key={API_KEY}&comic_id={comic_id}"

    # Realiza la solicitud GET al archivo get_covers.php
    response = requests.get(url)

    # Muestra el estado HTTP de la respuesta
    print("Status: ", response.status_code)

    # Muestra el texto completo devuelto por el servidor (útil para depuración)
    print("Text:", response.text)

    # Lanza una excepción si el estado HTTP indica error (por ejemplo, 404 o 500)
    response.raise_for_status()

    # Convierte y devuelve la respuesta del servidor en formato JSON
    return response.json()

# archivo para realizar pruebas, contiene una funcion simple y una asincrona para probar ambos casos 

def resta(a, b):
    resultado = a - b
    return resultado

async def obtener_datos(url):
    print(f"Conectando a {url}")
    return None
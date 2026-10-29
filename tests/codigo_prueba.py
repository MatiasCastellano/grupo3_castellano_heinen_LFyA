#deberia ser iguales, ya que se renombraron las variables
def resta(a, b):
    resultado = a - b
    return resultado

def resta_renombrada(x, y):
    result = x -y
    return result

#verificar que funciones iguales se detecten tambien(clones tipo 1)
def resta(a, b):
    resultado = a - b
    return resultado



# otro caso positivo, es lo mismo pero con lineas reordenadas
def procesar_factura(monto, tasa_impuesto, descuento):
    subtotal = monto - descuento
    impuesto_monto = monto * tasa_impuesto
    total = subtotal + impuesto_monto
    return total

def procesar_factura_reordenada(monto, tasa_impuesto, descuento):
    # Se invierte el orden de las asignaciones de 'impuesto_monto' y 'subtotal'
    impuesto_monto = monto * tasa_impuesto
    subtotal = monto - descuento
    total = subtotal + impuesto_monto
    return total

# Negativo, funciones distintas
def procesar_remito(items_remito, deposito_destino):
    """Procesamiento con bucles for y condicionales múltiples."""
    total_items = 0
    for item in items_remito:
        if item.disponible and item.deposito == deposito_destino:
            total_items += item.cantidad
    return total_items

#Funciones de tipo clon semantico que hacen lo mismo, de diferente manera, el return total devuelve el mismo valor
def sumar_hasta_n_for(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

def sumar_hasta_n_while(n):
    total = 0
    i = 1
    while i <= n:
        total += i
        i += 1
    return total
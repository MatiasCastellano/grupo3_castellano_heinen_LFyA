def resta(a, b):
    resultado = a - b
    return resultado

def resta_segura(a, b):
    if a > b:
        resultado = a - b
        return resultado
    return 0

#esperamos que sea igual que resta
def suma(a, b):
    resultado = a + b
    return resultado

#nuevo ejemplo
def procesar_factura(monto, impuesto, descuento):
    subtotal = monto - descuento
    total = subtotal + (subtotal * impuesto)
    return total

#esperamos que sea igual que procesar factura
def procesar_factura_segura(monto, impuesto, descuento):
    if monto > 0:
        subtotal = monto - descuento
        total = subtotal + (subtotal * impuesto)
        return total
    return 0

# Deberia ser igual que procesar_factura
async def procesar_factura_async(monto, impuesto, descuento):
    subtotal = monto - descuento
    total = subtotal + (subtotal * impuesto)
    return total


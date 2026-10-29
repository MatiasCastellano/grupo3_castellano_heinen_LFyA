import os
from src.extractor import extraer_funciones_de_archivo
from src.normalizer import normalizar_ast
from src.serializer import serializar_ast, calcular_similitud_levenshtein, es_candidato_duplicado

#verifica clones de tipo 1, identicas
def test_funciones_identicas():
    ruta = os.path.join("tests", "codigo_prueba.py")
    funcs = {
        f["name"]: serializar_ast(normalizar_ast(f["ast_node"]))
        for f in extraer_funciones_de_archivo(ruta)
    }

    similitud = calcular_similitud_levenshtein(funcs["resta"], funcs["resta"])

    # Al comparar una función contra sí misma (Clon Tipo 1),
    # la distancia de Levenshtein es 0 y la similitud debe ser exacta (1.0)
    assert similitud == 1.0
    assert es_candidato_duplicado(similitud) is True

#Este test verifica que reconoce clones de tipo 2(clones renombrados)
def test_funciones_variables_renombradas():
    ruta = os.path.join("tests", "codigo_prueba.py")
    funcs = {
        f["name"]: serializar_ast(normalizar_ast(f["ast_node"])) 
        for f in extraer_funciones_de_archivo(ruta)
    }

    similitud = calcular_similitud_levenshtein(funcs["resta"], funcs["resta_renombrada"])
    assert similitud >= 0.75 
    assert es_candidato_duplicado(similitud) is True

#reconoce como se menciona en el informe, clones de tipo 3 en donde se reordenan lineas de codigo, pero no se modifican las lineas
def test_funciones_lineas_reordenadas():
    ruta = os.path.join("tests", "codigo_prueba.py")
    funcs = {
        f["name"]: serializar_ast(normalizar_ast(f["ast_node"])) 
        for f in extraer_funciones_de_archivo(ruta)
    }
    similitud = calcular_similitud_levenshtein(funcs["procesar_factura"], funcs["procesar_factura_reordenada"])
    assert similitud >= 0.75
    assert es_candidato_duplicado(similitud) is True
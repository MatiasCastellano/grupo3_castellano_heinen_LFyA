import os
from src.extractor import extraer_funciones_de_archivo
from src.normalizer import normalizar_ast
from src.serializer import serializar_ast, calcular_similitud_levenshtein, es_candidato_duplicado

def test_funciones_variables_renombradas():
    ruta = os.path.join("tests", "codigo_prueba.py")
    funcs = {
        f["name"]: serializar_ast(normalizar_ast(f["ast_node"])) 
        for f in extraer_funciones_de_archivo(ruta)
    }

    similitud = calcular_similitud_levenshtein(funcs["resta"], funcs["resta_renombrada"])
    assert similitud >= 0.75 
    assert es_candidato_duplicado(similitud) is True

def test_funciones_lineas_reordenadas():
    ruta = os.path.join("tests", "codigo_prueba.py")
    funcs = {
        f["name"]: serializar_ast(normalizar_ast(f["ast_node"])) 
        for f in extraer_funciones_de_archivo(ruta)
    }
    similitud = calcular_similitud_levenshtein(funcs["procesar_factura"], funcs["procesar_factura_reordenada"])
    assert similitud >= 0.75
    assert es_candidato_duplicado(similitud) is True
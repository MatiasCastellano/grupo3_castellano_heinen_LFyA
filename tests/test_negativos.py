import os
from src.extractor import extraer_funciones_de_archivo
from src.normalizer import normalizar_ast
from src.serializer import (
    calcular_similitud_levenshtein,
    es_candidato_duplicado,
    serializar_ast,
)


def test_funciones_distinta_estructura_y_longitud():
    ruta = os.path.join("tests", "codigo_prueba.py")
    funcs = {
        f["name"]: serializar_ast(normalizar_ast(f["ast_node"]))
        for f in extraer_funciones_de_archivo(ruta)
    }

    similitud = calcular_similitud_levenshtein(
        funcs["resta"], funcs["procesar_remito"]
    )

    assert similitud < 0.75
    assert es_candidato_duplicado(similitud) is False


def test_funciones_distintas_tareas():
    ruta = os.path.join("tests", "codigo_prueba.py")
    funcs = {
        f["name"]: serializar_ast(normalizar_ast(f["ast_node"]))
        for f in extraer_funciones_de_archivo(ruta)
    }

    similitud = calcular_similitud_levenshtein(
        funcs["procesar_factura"], funcs["procesar_remito"]
    )

    assert similitud < 0.75
    assert es_candidato_duplicado(similitud) is False
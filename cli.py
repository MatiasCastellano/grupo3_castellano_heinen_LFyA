import argparse
import ast
import copy
import os
import re
import sys
import textwrap
from typing import List, Dict, Any, Tuple

from extractor import (
    FunctionExtractor,
    extraer_funciones_de_archivo,
    extraer_funciones_de_directorio,
)
from normalizer import normalizar_ast
from serializer import (
    serializar_ast,
    calcular_similitud_levenshtein,
    es_candidato_duplicado,
)


def _error(mensaje: str):
    print(f"[Error] {mensaje}", file=sys.stderr)
    sys.exit(1)


def _tokens(funcion: Dict[str, Any]) -> List[str]:
    return serializar_ast(normalizar_ast(copy.deepcopy(funcion["ast_node"])))


def obtener_funcion_objetivo(valor: str, directorio: str) -> Dict[str, Any]:
    match = re.match(r"^(.+\.py):(\w+)$", valor.strip())

    if match:
        ruta, nombre = match.group(1), match.group(2)

        if not os.path.isfile(ruta):
            ruta = os.path.join(directorio, ruta)
        if not os.path.isfile(ruta):
            _error(f"No se encontró el archivo '{match.group(1)}'.")

        for funcion in extraer_funciones_de_archivo(ruta):
            if funcion["name"] == nombre:
                return funcion

        _error(f"No se encontró la función '{nombre}' en '{ruta}'.")

    try:
        tree = ast.parse(textwrap.dedent(valor))
    except SyntaxError as e:
        _error(f"El código ingresado tiene un error de sintaxis: {e}")

    extractor = FunctionExtractor("<código ingresado>")
    extractor.visit(tree)

    if not extractor.functions:
        _error("El código ingresado no contiene ninguna función.")

    return extractor.functions[0]


def buscar_similares(
    objetivo: Dict[str, Any], funciones: List[Dict[str, Any]], top: int
) -> List[Tuple[float, Dict[str, Any]]]:
    tokens_objetivo = _tokens(objetivo)
    ruta_objetivo = os.path.abspath(objetivo["filepath"])

    resultados = []
    for funcion in funciones:
        es_la_misma = (
            os.path.abspath(funcion["filepath"]) == ruta_objetivo
            and funcion["lineno"] == objetivo["lineno"]
        )
        if es_la_misma:
            continue

        score = calcular_similitud_levenshtein(tokens_objetivo, _tokens(funcion))
        resultados.append((score, funcion))

    resultados.sort(key=lambda r: r[0], reverse=True)
    return resultados[:top]


def imprimir_resultados(
    objetivo: Dict[str, Any], resultados: List[Tuple[float, Dict[str, Any]]]
):
    print(
        f"Función objetivo: {objetivo['filepath']}:{objetivo['lineno']} -> {objetivo['name']}"
    )
    print()

    if not resultados:
        print("No se encontraron funciones para comparar.")
        return

    for posicion, (score, funcion) in enumerate(resultados, start=1):
        ubicacion = f"{funcion['filepath']}:{funcion['lineno']} -> {funcion['name']}"
        if es_candidato_duplicado(score):
            clasificacion = "🔴 CANDIDATO A DUPLICADO"
        else:
            clasificacion = "🟢 DISTINTA"
        print(f"{posicion:>3}. {score * 100:6.2f}%  {ubicacion}  {clasificacion}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Busca las funciones más similares a una función objetivo.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "ejemplos:\n"
            "  python %(prog)s --dir ./mi_repo --funcion archivo.py:mi_funcion --top 5\n"
            "  python %(prog)s --dir ./mi_repo --funcion $'def f(a, b):\\n    return a + b'"
        ),
        add_help=False,
    )
    parametros = parser.add_argument_group("parámetros")
    parametros.add_argument(
        "--dir", required=True, help="Directorio del repositorio a analizar."
    )
    parametros.add_argument(
        "--funcion",
        required=True,
        help="archivo.py:nombre_funcion o el código de la función pegado.",
    )
    parametros.add_argument(
        "--top", type=int, default=5, help="Cantidad de resultados a mostrar (default 5)."
    )
    if not (sys.argv[1:] if argv is None else argv):
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args(argv)

    if not os.path.isdir(args.dir):
        _error(f"'{args.dir}' no es un directorio válido.")

    funciones = extraer_funciones_de_directorio(args.dir)
    objetivo = obtener_funcion_objetivo(args.funcion, args.dir)
    resultados = buscar_similares(objetivo, funciones, args.top)
    imprimir_resultados(objetivo, resultados)

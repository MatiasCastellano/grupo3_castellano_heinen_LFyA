import ast
import os
from typing import List, Dict, Any


class FunctionExtractor(ast.NodeVisitor):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.functions: List[Dict[str, Any]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functions.append({
            "name": node.name,
            "filepath": self.filepath,
            "lineno": node.lineno,
            "ast_node": node
        })
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.functions.append({
            "name": node.name,
            "filepath": self.filepath,
            "lineno": node.lineno,
            "ast_node": node
        })
        self.generic_visit(node)


def extraer_funciones_de_archivo(filepath: str) -> List[Dict[str, Any]]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        
        tree = ast.parse(code, filename=filepath)
        
        extractor = FunctionExtractor(filepath)
        extractor.visit(tree)
        return extractor.functions

    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"[Advertencia] No se pudo parsear {filepath}: {e}")
        return []


def extraer_funciones_de_directorio(directory: str) -> List[Dict[str, Any]]:
    todas_las_funciones = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                funciones = extraer_funciones_de_archivo(filepath)
                todas_las_funciones.extend(funciones)
                
    return todas_las_funciones
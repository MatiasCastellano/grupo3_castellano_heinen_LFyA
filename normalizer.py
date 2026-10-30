import ast
from typing import Dict


class ASTNormalizer(ast.NodeTransformer):
    def __init__(self):
        self.var_map: Dict[str, str] = {}
        self.var_counter: int = 1

    def _get_var_token(self, original_name: str) -> str:
        if original_name not in self.var_map:
            self.var_map[original_name] = f"VAR{self.var_counter}"
            self.var_counter += 1
        return self.var_map[original_name]

    def visit_FunctionDef(self, node: ast.FunctionDef):
        node.name = "func"
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        node.name = "func"
        self.generic_visit(node)
        return node

    def visit_arg(self, node: ast.arg):
        node.arg = self._get_var_token(node.arg)
        self.generic_visit(node)
        return node

    def visit_Name(self, node: ast.Name):
        node.id = self._get_var_token(node.id)
        self.generic_visit(node)
        return node

    def visit_Constant(self, node: ast.Constant):
        node.value = "LIT"
        return node


def normalizar_ast(node: ast.AST) -> ast.AST:
    normalizer = ASTNormalizer()
    return normalizer.visit(node)
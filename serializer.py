import ast
from typing import List


def serializar_ast(node: ast.AST) -> List[str]:
    tokens: List[str] = []

    def _pre_order(curr_node: ast.AST):
        node_type = type(curr_node).__name__

        if isinstance(curr_node, ast.Name):
            tokens.append(f"{node_type}:{curr_node.id}")
        elif isinstance(curr_node, ast.Constant):
            tokens.append(f"{node_type}:{curr_node.value}")
        elif isinstance(curr_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            tokens.append(f"{node_type}:{curr_node.name}")
        elif isinstance(curr_node, ast.arg):
            tokens.append(f"{node_type}:{curr_node.arg}")
        else:
            tokens.append(node_type)

        for child in ast.iter_child_nodes(curr_node):
            _pre_order(child)

    _pre_order(node)
    return tokens


def calcular_similitud_levenshtein(tokens1: List[str], tokens2: List[str]) -> float:
    len1, len2 = len(tokens1), len(tokens2)
    
    if len1 == 0 and len2 == 0:
        return 1.0
    if len1 == 0 or len2 == 0:
        return 0.0

    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if tokens1[i - 1] == tokens2[j - 1]:
                costo = 0
            else:
                costo = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + costo
            )

    distancia = dp[len1][len2]
    max_len = max(len1, len2)

    return 1.0 - (distancia / max_len)


def es_candidato_duplicado(similitud: float, umbral: float = 0.75) -> bool:
    return similitud >= umbral
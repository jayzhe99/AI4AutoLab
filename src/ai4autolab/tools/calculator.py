"""A deliberately small and safe arithmetic tool for the first demo."""

import ast
import operator
from typing import Any, Callable, Dict, Type

from .base import Tool, ToolError


class CalculatorTool(Tool):
    name = "calculator"
    description = "Evaluate a basic arithmetic expression using +, -, *, / and parentheses."

    _binary_operators: Dict[Type[ast.AST], Callable[[float, float], float]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }
    _unary_operators: Dict[Type[ast.AST], Callable[[float], float]] = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def validate(self, arguments: Dict[str, Any]) -> None:
        if set(arguments) != {"expression"}:
            raise ToolError("calculator requires exactly one 'expression' argument.")
        expression = arguments["expression"]
        if not isinstance(expression, str) or not expression.strip():
            raise ToolError("expression must be a non-empty string.")
        if len(expression) > 200:
            raise ToolError("expression is too long.")
        try:
            tree = ast.parse(expression, mode="eval")
            self._evaluate_node(tree.body)
        except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as exc:
            raise ToolError("invalid arithmetic expression: {}".format(exc)) from exc

    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        expression = arguments["expression"]
        result = self._evaluate_node(ast.parse(expression, mode="eval").body)
        return {"expression": expression, "result": result}

    def _evaluate_node(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in self._binary_operators:
            left = self._evaluate_node(node.left)
            right = self._evaluate_node(node.right)
            return self._binary_operators[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._unary_operators:
            return self._unary_operators[type(node.op)](self._evaluate_node(node.operand))
        raise ToolError("unsupported expression element: {}".format(type(node).__name__))


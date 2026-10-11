import ast
import operator


class Calculator:

    def calculate(self, expression):
        operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
        }

        if len(expression) > 100:
            raise ValueError("表达式过长")

        def calc(node):
            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                if abs(node.value) > 1e12:
                    raise ValueError("数字过大")
                return node.value

            if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
                value = calc(node.operand)
                return value if isinstance(node.op, ast.UAdd) else -value

            if isinstance(node, ast.BinOp) and type(node.op) in operations:
                left = calc(node.left)
                right = calc(node.right)

                result = operations[type(node.op)](left, right)

                if abs(result) > 1e12:
                    raise ValueError("结果过大")

                return result

            raise ValueError("不支持的表达式")

        tree = ast.parse(expression, mode="eval")
        return calc(tree.body)
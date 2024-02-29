import ast
import functools
import inspect
from dataclasses import dataclass


def square(n: int) -> int:
    return n * n


def TRY(arg0):
    # ...
    raise NotImplementedError()


# replace
#     TRY(expr)
# with
#     _tmpvar_ = expr
#     if isinstance(_tmpvar_, NoneType):
#         return _tmpvar_
#     _tmpvar_


def _getsource(func):
    func.__globals__[func.__name__] = func
    source_lines, _ = inspect.getsourcelines(func)
    # strip decorators from the source itself
    source_code = "".join(
        line for line in source_lines if not line.startswith("@")
    )
    return source_code


def _unique_id() -> int:
    result = _unique_id.count
    _unique_id.count += 1
    return result


_unique_id.count = 0


def propagate(ErrorType: type):
    def propagate_wrapper(func):
        source = _getsource(func)
        tree = ast.parse(source)

        func_body = tree.body[0].body
        pos: int = 0

        @dataclass
        class ReplaceName(ast.NodeTransformer):
            name_to_replace: str
            new_node: ast.AST

            def visit_Name(self, node):
                if node.id == self.name_to_replace:
                    return self.new_node
                return node

        def insert_return_stmts_into_func_body(node):
            id = _unique_id()
            tmpvar = f"_tmpvar{id}_"
            tmpexpr = f"_tmpexpr{id}_"

            return_stmts = ast.parse(
                f"{tmpvar} = {tmpexpr}\n"
                f"if isinstance({tmpvar}, {ErrorType.__name__}):\n"
                f"    return {tmpvar}\n"
            )
            return_stmts = ReplaceName(tmpexpr, node.args[0]).visit(
                return_stmts
            )
            # insert return_stmts into func_body
            nonlocal pos
            func_body[pos:pos] = return_stmts.body
            pos += len(return_stmts.body)

            name_expr = ast.parse(f"{tmpvar}")
            return name_expr.body[0].value

        class ReplaceFuncCall(ast.NodeTransformer):
            def visit_Call(self, node):
                if (
                    isinstance(node.func, ast.Name)
                    and node.func.id == "TRY"
                    and len(node.args) == 1
                ):
                    return insert_return_stmts_into_func_body(node)
                return node

        while pos < len(func_body):
            func_body[pos] = ReplaceFuncCall().visit(func_body[pos])
            pos += 1

        new_tree = ast.fix_missing_locations(tree)

        # get the compiled function
        new_func = compile(new_tree, "<ast>", "exec")
        namespace = {}
        exec(new_func, func.__globals__, namespace)
        new_func = namespace[func.__name__]

        return functools.wraps(func)(new_func)

    return propagate_wrapper

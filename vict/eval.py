""":mod:`vict.eval` --- Evaluate AST
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import vict.parse
import vict.tree
import vict.env

def evaluate(ast, env):

    if type(ast) is list:
        for item in ast:
            evaluate(item, env)

    if type(ast) is vict.tree.Program:
        for line in ast.lines:
            evaluate(line, env)

    if type(ast) is vict.tree.Identifier:
        return env.get(ast.identifier)

    if type(ast) is vict.tree.Set:
        if type(ast.left) is vict.tree.Identifier:
            env.set_(ast.left.identifier, evaluate(ast.right, env))

    if type(ast) is vict.tree.Dictionary:
        for key in ast.keys():
            ast[key] = evaluate(ast[key], env)
        return ast

    if type(ast) is vict.tree.Array:
        return vict.tree.Array(evaluate(x, env) for x in list(ast))

    literals = [vict.tree.Integer, vict.tree.Float,
                vict.tree.String, vict.tree.Boolean,
                vict.tree.None_]
    if type(ast) in literals:
        return ast

    if type(ast) is vict.tree.Method:
        return ast

if __name__ == "__main__":
    code = open("vict/test2.vict").read()
    code = unicode(' '.join(code.split('\n')))
    ast = vict.parse.program.parse(code)
    env = vict.env.built_in_env()
    evaluate(ast, env)
    print env.env

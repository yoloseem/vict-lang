""":mod:`vict.eval` --- Evaluate AST
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import vict.parse
import vict.tree
import vict.env

def evaluate(ast, env):

    if type(ast) is list:
        for item in ast:
            ret = evaluate(item, env)
        return ret

    if type(ast) is vict.tree.Program:
        for line in ast.lines:
            ret = evaluate(line, env)
        return ret

    if type(ast) is vict.tree.Identifier:
        return env.get(ast.identifier)

    if type(ast) is vict.tree.Set:
        if type(ast.left) is vict.tree.Identifier:
            env.set_(ast.left.identifier, evaluate(ast.right, env))
            return env.get(ast.left.identifier)

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

    if type(ast) is vict.tree.Call:
        func = evaluate(ast.method, env)
        if type(func) is vict.tree.Method:
            new_env = vict.env.Environment(env)
            if len(ast.arguments) != len(func.arguments):
                raise TypeError('{0!r} takes only {1} argument(s) ({2} given)'.format(ast.method, len(func.arguments), len(ast.arguments)))
            for i, x in enumerate(func.arguments):
                new_env.env.__setitem__(x.identifier, evaluate(list(ast.arguments)[i], env))
            return evaluate(func.program, new_env)
        elif type(func) is vict.tree.Function:
            return func.func(*[evaluate(x, env) for x in list(ast.arguments)]) 
        else:
            raise TypeError('{0!r} is not callable'.format(func))
 
            

if __name__ == "__main__":
    code = open("vict/test2.vict").read()
    code = unicode(' '.join(code.split('\n')))
    ast = vict.parse.program.parse(code)
    env = vict.env.built_in_env()
    ret = evaluate(ast, env)
    if ret:
        print ret

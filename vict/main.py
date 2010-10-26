import vict.parse
import vict.tree
import vict.env
import vict.eval

import sys

if __name__ == "__main__":

    if len(sys.argv) == 1 or sys.argv[1].lower() == 'repl':
        print "REPL mode"
    else:
        try:
            code = open(sys.argv[1]).read()
        except:
            print "Vict-lang: can't open file '{0}'".format(sys.argv[1])
        else:
            ast = vict.parse.program.parse(' '.join(code.split('\n')))
            env = vict.env.built_in_env()
            ret = vict.eval.evaluate(ast, env)
            if ret:
                try:
                    print ret.__vict__()
                except NameError:
                    print ret

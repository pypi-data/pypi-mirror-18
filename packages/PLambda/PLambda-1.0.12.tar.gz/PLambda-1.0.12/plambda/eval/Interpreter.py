# iam: This is needed to stop python from treating 'print' as something special; rather than 
# just a builtin. Wonder how much of this hackery is in our future?
#
from __future__ import print_function

import importlib, sys, types, inspect, collections, os

from ..util.Util import isString, isInteger

from ..util.StringBuffer import StringBuffer

from .Code import SExpression, Atom, StringLiteral, Syntax

from .SymbolTable import SymbolTable

from .PLambdaException import PLambdaException

from .Environment import Environment

from .Closure import Closure

from .Globals import pythonGlobals

from ..visitor.Parser import parseFromFile, parseFromString

from .State import State

"""
Current bugs:

Things to add:

patch the builtin problem as much as possible

ForCont mystery

"""

RECURSIVE = 0
CPS       = 1
"""
Change to RECURSIVE for recursive interpreter.
"""
CURRENT_MODE = CPS

class Interpreter(object):

    def __init__(self):
        self.definitions = {}
        self.code = {}
        self.modules = {}
        self.uid2object = {}
        self.object2uid = {}
        if CURRENT_MODE is RECURSIVE:
            self.evaluateString = self.recursive_evaluateString
            self.evaluate = self.recursive_evaluate
            self.eval = self.recursive_eval
        else:
            self.evaluateString = self.cps_evaluateString
            self.evaluate = self.cps_evaluate
            self.eval = self.cps_eval
            

    def recursive_evaluateString(self, string):
        """Parses and evaluates a string as plambda expression.
        """
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        code = parseFromString(string)
        retval = None
        for c in code:
            retval = self.evaluate(c)
        return retval
        
    def recursive_evaluate(self, exp):
        """Evaluates an Sexpression, StringLiteral, or Atom.
        """
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        return self.eval(exp, Environment())

    def recursive_eval(self, exp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        if exp is None:
            return None
        if isinstance(exp, StringLiteral):
            return exp.string
        if isinstance(exp, Atom):
            (ok, value) = self.lookup(exp, env)
            if ok:
                return value
            else:
                raise value
            #return self.lookup(exp, env)
        elif isinstance(exp, SExpression):
            return self.evalSExpression(exp, env)
        else:
            raise PLambdaException("huh? I did not grok {0}".format(exp))

    def cps_evaluateString(self, string):
        """Parses and evaluates a string as plambda expression.
        """
        code = parseFromString(string)
        retval = None
        for c in code:
            retval = self.cps_evaluate(c)
        return retval
        
    def cps_evaluate(self, exp):
        """Evaluates an Sexpression, StringLiteral, or Atom.
        """
        return self.cps_eval(exp, Environment())

    def cps_eval(self, exp, env):
        state = State(self, exp, env)
        while not state.isDone():
            state.step()
        #FIXME: we raise the uncaught exception. not sure why we need to differ from jlambda
        if state.k.excep is not None:
            raise state.k.excep
        else:
            return state.val



    def lookup(self, leaf, env):
        """See if the identifier is bound in the extended environment.

        First see if it referencing a thing in a module. Then, failing that
        look if it has a value in the current lexical environment. As a last
        resort see if it has a global definition, either in our global environment
        or in Python's. If it has a value in Python's global environment and that
        vaue is callable it retruns that. Otherwise it raises a PLambdaException.
        """

        assert(isinstance(leaf, Atom))

        name = leaf.string
        path = name.split('.')

        (ok, value) = self.mlookup(path, leaf)
        if ok:
            return (ok, value)
        (ok, value) = env.lookup(leaf)
        if ok:
            return (ok, value)
        (ok, value) = self.glookup(path, leaf)
        if ok:
            return (ok, value)
        (ok, value) = self.plookup(leaf)
        if ok:
            return (ok, value)
        return (False, PLambdaException('Unbound variable: {0}'.format(repr(leaf))))
    
        
    def getmodule(self, path):
        """Finds the longest prefix of path that is in the modules dictionary.

        If finds a prefix returns (mod, path_remainder), else (None, path).
        """
        index = len(path)
        remainder = []
        current = None
        mod = None
        while index != 0:
            current = '.'.join(path[0:index])
            mod = self.modules.get(current)
            if mod is not None:
                break
            index -= 1
            remainder.insert(0, path[index])
        if mod is not None:
            return (mod, remainder)
        else:
            return (None, path)

    def getobject(self, obj, path):
        """Follows the path from object.

        Follows the path down into the obj, which should be a class or module,
        and if what lies at the end is x returns (True, x), else, if the path
        makes no sense at some stage, returns (False, None).
        """
        if path == []:
            return (True, obj)
        if obj is None:
            return (False, None)
        elif inspect.ismodule(obj):
            d = obj.__dict__
            k = path[0]
            if k in d:
                return self.getobject(obj.__dict__.get(k), path[1:])
            else:
                return (False, None)
        else:
            if hasattr(obj, path[0]):
                nobj = getattr(obj, path[0])
            else:
                return (False, None)
            return self.getobject(nobj, path[1:])
        
        
    def mlookup(self, path, leaf):
        """Just a quick 'n dirty hack at this point.
        """
        assert(isinstance(leaf, Atom))

        (mod, remainder) = self.getmodule(path)

        return self.getobject(mod, remainder)

    def glookup(self, path, leaf):
        """Looks up the symbol in the PLambda definitions."""
        assert(isinstance(leaf, Atom))

        ok = False
        
        if len(path) > 1:
            key = path[0]
            val = self.definitions.get(key)
            if val is not None:
                (ok, val) = self.getobject(val, path[1:])
        else:
            key = leaf.string
            ok = key in self.definitions
            if ok:
                val = self.definitions[key]
        
        if ok:
            return (True, val)
        else:
            return (False, None)

    def plookup(self, leaf):
        """Looks up the symbol in the Python environment.

        This is a hack at present, as a means of looking up global functions.
        This is why we bail if the value is not callable.
        """
        assert(isinstance(leaf, Atom))
        
        try:
            val = eval(leaf.string)
            if callable(val):
                return (True, val)
        except NameError:
            pass
        return (False, None)

    def evalSeq(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        tail = sexp.spine[1:]
        retval = None
        for s in tail:
            retval = self.eval(s, env)
        return retval


    def callInvoke(self, obj, methodname, vals, location):
        
        methods = inspect.getmembers(obj, callable)

        if not methods:
            fmsg = 'Object not invokable: {0} {1}'
            emsg = fmsg.format(obj, location)
            return (False, PLambdaException(emsg))

        method = None
        
        if not isString(methodname):
            fmsg = 'Method name not a string: {0} {1}'
            emsg = fmsg.format(methodname, location)
            return (False, PLambdaException(fmsg))

        
        for (name, value) in methods:
            if name == methodname:
                method = value
                break

        if method is None:
            emsg = 'No such method: {0} {1}'.format(methodname, location)
            return (False, PLambdaException(emsg))
        

        # Ugliness under python's hood:
        # Cannot get the argspec of a builtin
        # http://stackoverflow.com/questions/3276635/how-to-get-the-number-of-args-of-a-built-in-function-in-python
        # http://stackoverflow.com/questions/990016/how-to-find-out-the-arity-of-a-method-in-python
        #
        # Can avoid using inspect for simlpe cases:
        #        def arity(obj, method):
        #          return getattr(obj.__class__, method).func_code.co_argcount - 1 # remove self
        #
        if type(method) !=  types.BuiltinFunctionType:
            argspec = inspect.getargspec(method)
            # if it is an object we have to *not* count 'self',
            # but if it is a class we need to pass all the args!
            offset = 0
            if not inspect.ismodule(obj) and not inspect.isclass(obj):
                offset = 1
                ndefaults = len(argspec.defaults)  if argspec.defaults else 0
                nargs = len(argspec.args) - offset
                nvals = len(vals)
                # my guess is that we will need to revisit this. what do we
                # do when some of the defaults are used but not others?
                if (nvals < nargs - ndefaults) or  (nargs < nvals):
                    fmsg = 'Arity of {0} args {1} does not match the argspec: {2}. defaults: {3}'
                    emsg = fmsg.format(methodname, vals, argspec.args[offset:], argspec.defaults)
                    return (False, PLambdaException(emsg))

        retval = None

        try:
            retval = method(*vals)
            return (True, retval)
        except Exception as e:
            return (False, PLambdaException('invoke {0} threw {1}'.format(location, str(e))))


    
    def evalInvoke(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        objexp = sexp.spine[1]
        obj = self.eval(objexp, env)

        methodexp = sexp.spine[2]
        methodname  = self.eval(methodexp, env)

        args = sexp.spine[3:]

        vals = []
        for a in args:
            vals.append(self.eval(a, env))

        (ok, retval) = self.callInvoke(obj, methodname, vals, sexp.spine[0].location)

        if ok:
            return retval
        else:
            raise retval

    def evalDefine(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        identifier = sexp.spine[1]
        
        assert(isinstance(identifier, Atom))
        
        val = None

        if len(sexp.spine) == 3:
            val = self.eval(sexp.spine[2], env)
        else:
            val = Closure(self, sexp.spine[2], sexp.spine[3], env, sexp.spine[0].location)

        idstr = identifier.string
        
        dot = idstr.find('.')

        if dot >= 0:
            sys.stderr.write('Bad idea to have a  "." in an identifier: {0}\n'.format(repr(identifier)))
            
        
        self.definitions[idstr] = val
        self.code[idstr] = sexp
        return identifier
    

    def evalLet(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        nenv = Environment(env)
        bindings = sexp.spine[1].spine
        body = sexp.spine[2]

        for bpair in bindings:
            var = bpair.spine[0]
            assert(isinstance(var, Atom))
            nenv.extend(var, self.eval(bpair.spine[1], nenv))

        return self.eval(body, nenv)


    def callClosure(self, fun, vals, location):
        """DEPRECATED VERSION.
        """
        retval = None
        assert(isinstance(fun, Closure))
        if len(vals) != fun.arity:
            fmsg = 'Arities at apply  {3} do not match: closure with arity {0} applied to args {1} of length {2}'
            emsg = fmsg.format(fun.arity, vals, len(vals), location)
            return (False, PLambdaException(emsg))
        else:
            try: 
                retval = fun.applyClosure(*vals)
                return (True, retval)
            except Exception as e:
                return (False, e)
        

    def callCallable(self, fun, vals, location):
        retval = None
        assert(callable(fun))
        try: 
            retval = fun(*vals)
            return (True, retval)
        except Exception as e:
            return (False, e)
            

    def callApply(self, fun, funexp, vals, location):
        """DEPRECATED VERSION.
        """
        retval = None
        if not isinstance(fun, Closure) and not callable(fun):
            fmsg = 'Cannot apply {0} which evaluated to {1}'
            emsg = fmsg.format(funexp, fun)
            return (False, PLambdaException(emsg))

        if isinstance(fun, Closure):
            return self.callClosure(fun, vals, location)
        else:
            return self.callCallable(fun, vals, location)


    def evalApply(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        funexp  = sexp.spine[1]
        argexps = sexp.spine[2:]

        fun = self.eval(funexp, env)

        vals = []
        for arg in argexps:
            vals.append(self.eval(arg, env))

        (ok, retval) = self.callApply(fun, funexp, vals,  sexp.spine[0].location)

        if ok:
            return retval
        else:
            raise retval


    def evalFor(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        identifier = sexp.spine[1]
        rangeexp = sexp.spine[2]
        body = sexp.spine[3]

        rangeval = self.eval(rangeexp, env)

        if isInteger(rangeval):
            rangeval = range(0, rangeval)  #FIXME: not very efficient for big integers
            
        if isinstance(rangeval, collections.Iterable):
            retval = None
            for v in rangeval:
                nenv = Environment(env)
                retval = self.eval(body, nenv.extend(identifier, v))
            return retval
        else:
            fmsg = 'Range is not iterable: {0} evaluated to {1}'
            emsg = fmsg.format(rangeexp, rangeval)
            raise PLambdaException(emsg)


    def evalTry(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        tryexp = sexp.spine[1]
        catchexp = sexp.spine[2]
        retval = None
        try:
            retval = self.eval(tryexp, env)
        except Exception as e:
            catchid = catchexp.spine[1]
            catchbody = catchexp.spine[2]
            catchenv = Environment(env)
            retval = self.eval(catchbody, catchenv.extend(catchid, e))
        return retval


    def callBinaryOp(self, op, val0, val1, location):
        retval = None
        try:
            if  op is SymbolTable.PLUS:
                retval =  val0 + val1
            elif op is SymbolTable.TIMES:
                retval = val0 * val1
            elif op is SymbolTable.DIVIDE:
                retval = val0 / val1
            elif op is SymbolTable.MODULO:
                retval = val0 % val1
            elif op is SymbolTable.GT:
                retval = val0 < val1
            elif op is SymbolTable.LT:
                retval = val0 > val1
            elif op is SymbolTable.GET:
                retval = self.evalGet(val0, val1, location)
            elif op is SymbolTable.GEQ:
                retval = val0 >= val1
            elif op is SymbolTable.LEQ:
                retval = val0 <= val1
            elif op is SymbolTable.EQUALS:
                retval = val0 == val1
            elif op is SymbolTable.IS:
                retval = val0 is val1
            elif op is SymbolTable.NEQ:
                retval = val0 != val1
            elif op is SymbolTable.SETUID:
                retval = self.setUID(val0, val1, location)
            else:
                fmsg = 'Unrecognized binary operation: {0} {1}'
                emsg = fmsg.format(op, location)
                return (False, PLambdaException(emsg))
        except Exception as e:
            return (False, PLambdaException('callTernaryOp {0} {1} threw {2}'.format(op, location, str(e))))
        return (True, retval)
    
    def evalBinaryOp(self, sexp, env):
        """Recursive version. Soon to be deprecated.
        """
        (uop, arg0, arg1) =  sexp.spine
        assert isinstance(uop, Atom)
        op = uop.string

        val0 = self.eval(arg0, env)
        val1 = self.eval(arg1, env)

        (ok, retval) = self.callBinaryOp(op, val0, val1, sexp.location)

        if ok:
            return retval
        else:
            raise retval
        
    def evalGet(self, val0, val1, location):
        if (isinstance(val0, list) or isinstance(val0, tuple))  and isinstance(val1, int):
            return val0[val1]
        elif isinstance(val0, dict):
            return val0.get(val1)
        else:
            fmsg = 'Bad args to \"get\": {0} {1} {2}'
            emsg = fmsg.format(val0, val1, location)
            raise PLambdaException(emsg)

    def unsetUID(self, val0):
        if val0 in self.object2uid:
            uid = self.object2uid[val0]
            self.object2uid.pop(val0)
            self.uid2object.pop(uid)
            return True
        else:
            return False
       

    def setUID(self, val0, val1, location):
        if val0 is None:
            raise PLambdaException('setuid {0}: first argument cannot be None.'.format(str(location)))                  
        elif val1 is None:
            return self.unsetUID(val0)
        elif not isString(val1):
            raise PLambdaException('setuid {0}: val1 not a string.'.format(str(location)))
        else:
            if val1 in self.uid2object or val0 in self.object2uid:
                raise PLambdaException('setuid {0}: redefiniton'.format(str(location)))
            else:
                self.object2uid[val0] = val1
                self.uid2object[val1] = val0
                return True

    def evalKWApply(self, val0, val1, val2, loc):
        if not callable(val0):
            raise PLambdaException('kwapply {0}: 1st argument not callable'.format(str(loc)))
        if not isinstance(val1, list):
            raise PLambdaException('kwapply {0}: 2nd argument not a list'.format(str(loc)))
        if not isinstance(val2, dict):
            raise PLambdaException('kwapply {0}: 3rd argument not a dict'.format(str(loc)))
        return  val0(*val1, **val2)


    def evalModify(self, val0, val1, val2, loc):
        #be brave until we need to back down...
        if isinstance(val0, dict):
            val0[val1] = val2 
        elif isinstance(val0, list):
            l0 = len(val0)
            if isinstance(val1, int) and -l0 < val1 and val1 < l0:
                val0[val1] = val2
            else:
                raise PLambdaException('modify {0}: bad index to modify of list'.format(str(loc)))
        else:
            raise PLambdaException('modify {0}: unhandled case'.format(str(loc)))
        return None




    def callTernaryOp(self, op, val0, val1, val2, location):
        retval = None
        try:
            if  op in (SymbolTable.UPDATE, SymbolTable.SUPDATE, SymbolTable.SETATTR):
                setattr(val0, val1, val2)
                retval = None
            elif op is SymbolTable.KWAPPLY:
                retval = self.evalKWApply(val0, val1, val2, location)
            elif op is SymbolTable.MODIFY:
                retval = self.evalModify(val0, val1, val2, location)
            else:
                fmsg = 'Unrecognized ternary operation: {0} {1}'
                emsg = fmsg.format(op, location)
                return (False, PLambdaException(emsg))
        except Exception as e:
            return (False, PLambdaException('callTernaryOp {0} {1} threw {2}'.format(op, location, str(e))))
        return (True, retval)
        

    def evalTernaryOp(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        (uop, arg0, arg1, arg2) =  sexp.spine
        assert isinstance(uop, Atom)
        op = uop.string

        val0 = self.eval(arg0, env)
        val1 = self.eval(arg1, env)
        val2 = self.eval(arg2, env)

        (ok, retval) = self.callTernaryOp(op, val0, val1, val2, sexp.location)
        
        if ok:
            return retval
        else:
            raise retval
        
    def evalAmbi1Op(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        uop =  sexp.spine[0]
        assert isinstance(uop, Atom)
        op = uop.string
        if op is SymbolTable.MINUS:
            if len(sexp.spine) == 3:
                return self.eval(sexp.spine[1], env) - self.eval(sexp.spine[2], env)
            else:
                return - self.eval(sexp.spine[1], env)
        else:
            fmsg = 'Unrecognized ambi1 operation: {0}'
            emsg = fmsg.format(op)
            raise PLambdaException(emsg)


    def callGetAttr(self, vals, location):
        retval = None
        try:
            retval = getattr(*vals)
            return (True, retval)
        except Exception as e:
            return (False, PLambdaException('callGetAttr {0} threw {1}'.format(location, str(e))))
        
        
    def evalAmbi2Op(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        uop =  sexp.spine[0]
        args = sexp.spine[1:]
        assert isinstance(uop, Atom)
        op = uop.string
        if op is SymbolTable.IF:
            return self.evalIf(sexp, env)
        elif op in (SymbolTable.GETATTR, SymbolTable.LOOKUP):
            vals = []
            
            for arg in args:
                vals.append(self.eval(arg, env))
            (ok, retval) = self.callGetAttr(vals, sexp.spine[0].location)
            if ok:
                return retval
            else:
                raise retval
        else:
            fmsg = 'Unrecognized ambi1 operation: {0}'
            emsg = fmsg.format(op)
            raise PLambdaException(emsg)

    def evalIf(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        testexp = sexp.spine[1]
        test = self.eval(testexp, env)
        #do we want to enforce booleaness here? JLambda does.
        if not isinstance(test, bool):
            msg = '{0} is not a boolean in conditional {1}'
            raise PLambdaException(msg.format(test, sexp.spine[0].location))
        elif test:
            return  self.eval(sexp.spine[2], env)
        if len(sexp.spine) == 4:
            return  self.eval(sexp.spine[3], env)
        else:
            return None


    def evalAnd(self, args, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        for e in args:
            if  self.eval(e, env) is False:
                return False
        return  True
        

    def evalOr(self, args, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        for e in args:
            if  self.eval(e, env):
                return True
        return  False

        
    def evalNaryOp(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        uop =  sexp.spine[0]
        assert isinstance(uop, Atom)
        op = uop.string
        args = sexp.spine[1:]
        
        if op is SymbolTable.AND:
            return self.evalAnd(args, env)
        elif op is SymbolTable.OR:
            return self.evalOr(args, env)
        elif  op is SymbolTable.CONCAT:
            return  self.evalConcat(sexp, env)
        elif op in (SymbolTable.MKTUPLE, SymbolTable.MKLIST, SymbolTable.MKDICT):
            vals = []
            for arg in args:
                vals.append(self.eval(arg, env))
            if op is SymbolTable.MKTUPLE:
                return tuple(vals)
            elif op is SymbolTable.MKLIST:
                return vals
            else:
                return dict(vals[i:i+2] for i in range(0, len(vals), 2))
        else:
            fmsg = 'Unrecognized n-ary operation {1}: {0}'
            emsg = fmsg.format(op, sexp.location)
            raise PLambdaException(emsg)

    def evalConcat(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        args = sexp.spine[1:]
        sb = StringBuffer()
        for e in args:
            sb.append(str(self.eval(e, env)))
        return  str(sb)
                               
    def evalSExpression(self, sexp, env):
        """RECURSIVE VERSION. Soon to be deprecated.
        """
        code = sexp.code
        if code is Syntax.SEQ:
            return self.evalSeq(sexp, env)
        elif code is Syntax.LET:
            return self.evalLet(sexp, env)
        elif code is Syntax.DEFINE:
            return self.evalDefine(sexp, env)
        elif code is Syntax.LAMBDA:
            spine = sexp.spine
            return Closure(self, spine[1], spine[2], env, spine[0].location)
        elif code is Syntax.INVOKE:
            return self.evalInvoke(sexp, env)
        elif code is Syntax.APPLY:
            return self.evalApply(sexp, env)
        elif code is Syntax.PRIMITIVE_DATA_OP :
            return self.evalPrimitiveDataOp(sexp, env)
        elif code is Syntax.UNARY_OP:
            return self.evalUnaryOp(sexp, env)
        elif code is Syntax.BINARY_OP:
             return self.evalBinaryOp(sexp, env)
        elif code is Syntax.TERNARY_OP:
             return self.evalTernaryOp(sexp, env)
        elif code is Syntax.AMBI1_OP:
            return self.evalAmbi1Op(sexp, env)
        elif code is Syntax.AMBI2_OP:
            return self.evalAmbi2Op(sexp, env)
        elif code is Syntax.N_ARY_OP:
            return self.evalNaryOp(sexp, env)
        elif code is Syntax.TRY:
            return self.evalTry(sexp, env)
        elif code is Syntax.FOR:
            return self.evalFor(sexp, env)
        else:
            raise PLambdaException("huh?")

    def evalPrimitiveDataOp(self, sexp, env):
        (a0, a1) = sexp.spine
        assert isinstance(a0, Atom)
        assert isinstance(a1, Atom)
        op = a0.string
        data = a1.string
        try:
            if op is SymbolTable.INT:
                return int(data)
            elif op is SymbolTable.FLOAT:
                return float(data)
            else:
                return True if data.lower() == 'true' else False
        except Exception as e:
            sys.stderr.write('evalPrimitiveDataOp: {0} {1}\n'.format(str(e), a0.location))
            return 0 if op is not SymbolTable.FLOAT else 0.0


    def importmod(self, val):
        try:
            
            if isString(val):
                module = importlib.import_module(val)
                if module is not None:
                    self.modules[val] = module
                    return True
                else:
                    sys.stderr.write('Module {0} not found'.format(val))
            return False

        except ImportError as ie:
            print(ie)
            return False


    def evalGlobal(self, val, loc):
        return pythonGlobals.get(val, None)

    def callUnaryOp(self, op, val, location):
        """Calls the unary op with argument val.

           It returns (True, op(val) if everything is OK, otherwise 
        it returns (False, Exception).
        """
        retval = None
        try:
            if  op is SymbolTable.LOAD:
                if isString(val):
                    retval = self.load(val)
                else:
                    retval = False
            elif op is SymbolTable.IMPORT:
                retval = self.importmod(val)
            elif op is SymbolTable.ISNONE:
                retval = val is None
            elif op is SymbolTable.ISINT:
                retval = isinstance(val, int)
            elif op is SymbolTable.ISFLOAT:
                retval = isinstance(val, float)
            elif op is SymbolTable.ISOBJECT:
                retval = val is not None
            elif op is SymbolTable.GLOBAL:
                retval = self.evalGlobal(val, location)
            elif op is SymbolTable.THROW:
                return (False,  val)
            elif op is SymbolTable.FETCH:
                if val in self.uid2object:
                    retval = self.uid2object[val]
                else:
                    retval = None
            elif op is SymbolTable.GETUID:
                if val in self.object2uid:
                    retval = self.object2uid[val]
                else:
                    retval = None
            elif op is SymbolTable.NOT:
                retval = True if val is False else False
            else:
                return (False, PLambdaException("Unrecognized unary op {0} {1}".format(op, location)))
        except Exception as e:
            return (False, PLambdaException('callUnaryOp {0} {1} threw {2}'.format(op, location, str(e))))

        return (True, retval)
        
    def evalUnaryOp(self, sexp, env):
        """Recursive version. Soon to be deprecated.
        """
        (uop, arg) =  sexp.spine
        assert isinstance(uop, Atom)
        op = uop.string
        val = self.eval(arg, env)

        (ok, retval) = self.callUnaryOp(op, val, sexp.location)

        if ok:
            return retval
        else:
            raise retval
        

    def load(self, filename):
        if isString(filename) and os.path.exists(filename):
            codelist = parseFromFile(filename)
            for c in codelist:
                self.evaluate(c)
            return True
        return False

    
    def showDefinitions(self, sb=None):
        """Either writes the definitions out to stderr, or the optional StringBuffer passed in.
        """
        func = sb.append if sb else sys.stderr.write
        for key, value in self.definitions.iteritems():
            func('{0}  -->  {1}\n'.format(key, value))
        return sb

    def showCode(self, sb=None):
        """Either writes the code out to stderr, or the optional StringBuffer passed in.
        """
        func = sb.append if sb else sys.stderr.write
        for key, value in self.code.iteritems():
            func('{0}  -->  {1}\n'.format(key, value))
        return sb

    def showUIDs(self, sb=None):
        """Either writes the UIDs out to stderr, or the optional StringBuffer passed in.
        """
        func = sb.append if sb else sys.stderr.write
        for key, value in self.uid2object.iteritems():
            func('{0}  -->  {1}\n'.format(key, value))
        return sb
    
            


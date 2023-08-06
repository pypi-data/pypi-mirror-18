"""
The Phi DSL is all about combining functions in useful ways, enabling a declarative approach that can improve clarity, readability and lead to shorter code. All valid expression of the DSL can be compiled to a function using `P.Make` or applied to a value using `P.Pipe`.

Phi offers the following constructs/expressions, **try to read their documentation in order**:

* **`phi.dsl.Function`**: any function of arity 1 is an element of the language
* **`phi.dsl.Composition`**: allows to sequentially compose functions
* **`phi.dsl.Branch`**: lets to create a branched computation that returns a list with the results of each branch
* **`phi.dsl.Input`**: allows you to specify an input value, compiles to a (constant) function that returns the same value no matter the input
* **`phi.dsl.With`**: lets you to specify a context manager for the expresion (uses the `with` statemente)
* **`phi.dsl.Record`**: lets to create a branched computation with named branches that returns a record-like structure with the results of each branch
* **`phi.dsl.Read` & `phi.dsl.Write`**: allow you to create a reference to the value at some point and read it latter on.F

Any expresion can appear inside any other expresion in a nested fasion. They correct way to think about this is that each sub-expression will be compiled to a function of arity 1, therefore from the parent expresion's point of view all of its elements are just functions.
"""

from utils import identity
import utils
import pprint
from abc import ABCMeta, abstractmethod
from inspect import isclass
import functools


###############################
# Helpers
###############################

class _NoValue(object):

    def __repr__(self):
        return "NoValue"

_NO_VALUE = _NoValue()

class Ref(object):
    """docstring for Ref."""
    def __init__(self, name, value=_NO_VALUE):
        super(Ref, self).__init__()
        self.name = name
        self.value = value

    def __call__(self, *optional):
        if self.value is _NO_VALUE:
            raise Exception("Trying to read Ref('{0}') before assignment".format(self.name))

        return self.value

    def set(self, x):
        self.value = x

        return x


class RefManager(object):

    CURRENT_REFS = None

    def __init__(self, next_refs={}):
        self.previous_refs = RefManager.CURRENT_REFS
        self.next_refs = next_refs

    def __enter__(self):
        RefManager.CURRENT_REFS = self.next_refs
        return RefManager.CURRENT_REFS

    def __exit__(self, *args):
        RefManager.CURRENT_REFS = self.previous_refs

    @classmethod
    def set_ref(cls, ref):
        if ref.name in cls.CURRENT_REFS:
            other_ref = cls.CURRENT_REFS[ref.name]
            # merge state: borg pattern
            other_ref.__dict__.update(ref.__dict__)
        else:
            cls.CURRENT_REFS[ref.name] = ref

    @classmethod
    def get_ref(cls, name):
        return cls.CURRENT_REFS[name]



class _RecordObject(dict):
    """docstring for DictObject."""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__ (self, attr):
        return self[attr]

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return self.__dict__.has_key(k)

    def pop(self, k, d=None):
        return self.__dict__.pop(k, d)

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict):
        return cmp(self.__dict__, dict)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))

###############################
# DSL Elements
###############################

class Node(object):
    """docstring for Node."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __compile__(self):
        pass

class Function(Node):
    """
All basic/terminal elements of this language are callables (implement `__call__`) of arity 1.

### Examples
Compiling a function just returns back the function

    Make(f) == f

and piping through a function is just the same a applying the function

    P.Pipe(x, f) == f(x)

    """
    def __init__(self, _f):
        super(Function, self).__init__()
        self._f= _f

    def __iter__(self):
        yield self

    def __compile__(self):
        return self._f

    def __str__(self):
        return "Fun({0})".format(self._f)


_Identity = Function(identity)


class Branch(Node):
    """
While `Composition` is sequential, `Branch` allows you to split the computation and get back a list with the result of each path. While the list literal should be the most incarnation of this expresion, it can actually be any iterable (implements `__iter__`) that is not a tuple and yields a valid expresion.

After compilation the expresion:

    k = [f, g]

is equivalent to

    k(x) = [ f(x), g(x) ]


In general, the following rules apply after compilation:

**General Branching**

    let fs = <some iterable of valid expressions>

is equivalent to

    k(x) = [ f(x) for f in fs ]


**Composing & Branching**

A more common scenario however is to see how braching interacts with composing. The expression

    k = (f, [g, h])

is *almost* equivalent to

    k = [ (f, g), (f, h) ]

As you see its as if `f` where distributed over the list. We say *almost* because what really happens is that the iterable is first compiled to a function and the whole sequence is then composed

     z(x) = [ g(x), h(x) ]
     k(x) = (f, z)(x) = z(f(x))

As you see `f` is only excecuted once.

### Examples

    form phi import P

    avg_word_length = P.Pipe(
        "1 22 333",
        lambda s: s.split(' '), # ['1', '22', '333']
        lambda l: map(len, l), # [1, 2, 3]
        [
            sum # 1 + 2 + 3 == 6
        ,
            len # len([1, 2, 3]) == 3
        ],
        lambda l: l[0] / l[1] # sum / len == 6 / 3 == 2
    )

    assert avg_word_length == 2

The previous could also be done more briefly like this

    form phi import P, Obj

    avg_word_length = P.Pipe(
        "1 22 333",
        Obj.split(' '), # ['1', '22', '333']
        P.map(len), # [1, 2, 3]
        [
            sum # sum([1, 2, 3]) == 6
        ,
            len # len([1, 2, 3]) == 3
        ],
        P[0] / P[1] # 6 / 3 == 2
    )

    assert avg_word_length == 2

In the example above the last expression

    P[0] / P[1]

works for a couple of reasons

1. The previous expression returns a list
2. In general the expression `P[x]` compiles to a function with the form `lambda obj: obj[x]`
3. The class `Lambda` (the class from which the object `P` inherits) overrides most operators to create functions easily. For example, the expression

    (P * 2) / (P + 1)

compile to a function of the form

    f(x) = (x * 2) / (x + 1)

Check out the documentatio for Phi [lambdas](https://cgarciae.github.io/phi/lambdas.m.html).

    """

    def __init__(self, iterable_code):
        branches = [ _parse(code) for code in iterable_code ]
        self.branches = functools.reduce(Branch._reduce_branches, branches, [])



    @staticmethod
    def _reduce_branches(branches, b):
        if len(branches) == 0:
            return [b]
        elif type(b) is not Write:
            return branches + [ b ]
        else: # type(b) is Write
            a = branches[-1]
            seq = _parse((a, b))
            return branches[:-1] + [ seq ]



    @staticmethod
    def __parse__(iterable_code):

        iterable_code = list(iterable_code)

        return Branch(iterable_code)

    def __compile__(self):
        fs = []

        for node in self.branches:
            node_f = node.__compile__()
            fs.append(node_f)

        def function(x):
            return [ f(x) for f in fs ]

        return function

    def __str__(self):
        return pprint.pformat(self.branches)


class Composition(Node):
    """
In this language tuples are used to express function composition. After compilation, the expression

    k = (f, g)

be equivalent to

    k(x) = g(f(x))

As you see, its a little different from the mathematical definition. Excecution order flow from left to right, and this makes reading and reasoning about code structured in the way more easy. This bahaviour is based upon the `|>` (pipe) operator found in languages like F#, Elixir and Elm. You can pack as many expressions as you like and they will be applied in order to the data that is passed through them when compiled an excecuted.

In general, the following rules apply after compilation:

**General Sequence**

    k = (f0, f1, ..., fn-1, fn)

is equivalent to

    k(x) = fn(fn-1(...(f1(f0(x)))))

**Single Function**

    k = (f)

is equivalent to

    k = f

**Identity**

The empty tuple

    k = ()

is equivalent to

    k(x) = x

### Examples

    from phi import P

    f = Make(
        lambda x: x * 2,
        lambda x: x + 1,
        lambda x: x ** 2
    )

    assert f(1) == 9 # ((1 * 2) + 1) ** 2

As you see, `Make`s `*args` are interpreted as a tuple which means all expressions contained are composed. The previous example using `P.Pipe`

    from phi import P

    assert 9 == P.Pipe(
        1,
        lambda x: x * 2,
        lambda x: x + 1,
        lambda x: x ** 2
    )

Again, `Pipe`'s signature is `Pipe(x, *args)` and `*args` is interpreted as a tuple which means all expressions contained are composed.

    """
    def __init__(self, left_code, right_code):
        super(Composition, self).__init__()
        self.left = _parse(left_code)
        self.right = _parse(right_code)

    @staticmethod
    def __build__(right, *prevs):
        left = prevs[0] if len(prevs) == 1 else Composition.__build__(*prevs)
        return Composition(left, right)

    @staticmethod
    def __parse__(tuple_code):
        tuple_code = list(tuple_code)

        if len(tuple_code) == 0:
            return _Identity

        if len(tuple_code) == 1:
            return _parse(tuple_code[0])

        tuple_code.reverse()

        return Composition.__build__(*tuple_code)

    def __compile__(self):
        f_left = self.left.__compile__()

        f_right = self.right.__compile__()

        f = utils.compose2(f_right, f_left)

        return f

    def __str__(self):
        return "Seq({0}, {1})".format(self.left, self.right)

class Record(Node):
    """
List or iterables in general provide you a way to branch your computation in the DSL, but access to the values of each branch are then done by index, this might be a little inconvenient because it reduces readability. Record branches provide a way to create named branches via a dictionary object where the keys are the names of the branches and the values are valid expressions representing the computation of that branch.

A special object is returned by this expression when excecuted, this object derives from `dict` and fully emulates it so you can treat it as such, however it also implements the `__getattr__` method, this lets you access a value as if it where a field if its key is a of type string.

### Examples

    from phi import P

    stats = P.Pipe(
        [1,2,3],
        dict(
            sum = sum
        ,
            len = len
        )
    )

    assert stats.sum == 6
    assert stats.len == 3

    assert stats['sum'] == 6
    assert stats['len'] == 3

Now lets image that we want to find the average value of the list, we could calculate it outside of the pipe doing something like `avg = stats.sum / stats.len`, however we could also do it inside the pipe using `P.Rec` or `phi.Rec` like this

    from phi import P, Rec

    avg = P.Pipe(
        [1,2,3],
        dict(
            sum = sum
        ,
            len = len
        ),
        Rec.sum / Rec.len
    )
    """
    def __init__(self, dict_code):
        super(Record, self).__init__()
        self.nodes_dict = { key: _parse(code) for key, code in dict_code.iteritems() }

    @staticmethod
    def __parse__(dict_code):
        return Record(dict_code)

    def __compile__(self):
        funs_dict = {}

        for key, node in self.nodes_dict.iteritems():
            f = node.__compile__()

            funs_dict[key] = f

        def function(x):
            return _RecordObject(**{key: f(x) for key, f in funs_dict.iteritems() })

        return function



class With(Node):
    """

    def With(context_manager, *body):

where

* **context_manager**: a [context manager](https://docs.python.org/2/reference/datamodel.html#context-managers) object or valid expression from the DSL that returns a context manager.
* ***body**: any valid expression of the DSL to be evaluated inside the context. `*body` is interpreted as a tuple so all expression contained are composed.

As with normal python programs you sometimes might want to create a context for a block of code. You normally give a [context manager](https://docs.python.org/2/reference/datamodel.html#context-managers) to the [with](https://docs.python.org/2/reference/compound_stmts.html#the-with-statement) statemente, in Phi you use `P.With` or `phi.With`

**Context**

Python's `with` statemente returns a context object through `as` keyword, in the DSL this object can be obtained using the `P.Context` method or the `phi.Context` function.

### Examples

    from phi import P, Obj, Context, With, Pipe

    text = Pipe(
        "text.txt",
        With( open, Context,
            Obj.read()
        )
    )

The previous is equivalent to

    with open("text.txt") as f:
        text = f.read()

    """

    GLOBAL_CONTEXT = _NO_VALUE

    def __init__(self, scope_code, *body_code):
        super(With, self).__init__()
        self.scope = _parse(scope_code, else_input=True)
        self.body = _parse(body_code)

    def __compile__(self):
        scope_f = self.scope.__compile__()
        body_fs = self.body.__compile__()

        def function(x):
            with scope_f(x) as scope:
                with self.set_scope(scope):
                    return body_fs(x)

        return function

    def set_scope(self, new_scope):
        self.new_scope = new_scope
        self.old_scope = With.GLOBAL_CONTEXT

        return self

    def __enter__(self):
        With.GLOBAL_CONTEXT = self.new_scope

    def __exit__(self, *args):
        With.GLOBAL_CONTEXT = self.old_scope


class Read(Node):
    """
Giving names and saving parts of your computation to use then latter is useful to say the least. In the DSL the expression

    {'x'}

behaves like just like the indentity except that as a side effect it creates a reference to that value which you can call latter. Here `{..}` is python's sytax for a set literal and `x` is a string with the name of the reference. To read the previous you would use the expression

    'x'

This is equivalent to a sort of function like this

    lambda z: read('x')

where the input is totally ignored and a hypothetical `read` function is given the reference name and it should return its stored value (internally its not implemented like this). As you see strings in the DSL mean read from a reference and a set with a string means write to a reference.

### Example
Lets see a common situation where you would use this

    from phi import P

    P.Pipe(
        input,
        fun_1, {'fun_1_val'}
        fun_2,
        [
            fun_4
        ,
        (
            'fun_1_val',
            fun_5
        )
        ]
    )

Here you *save* the value outputed by `fun_1` and the load it as the initial value of the second branch. In normal python the previous would be *almost* equivalent to this

    x = fun_1(input)
    fun_1_val = x
    x = fun_2(x)
    x = [
        fun_4(x)
    ,
        fun_5(fun_1_val)
    ]

    return x

### Write special case
When composing its aesthetically better to put writes in the same line as the function whos value its storing to make the intent a bit more clear:

    (
        f, {'a'},
        g
    )

Here we store the value of `f` in `'a'`, however, when you are inside a branch you will be tempted to do the following to get the same result:

    [
        f, {'a'}
    ,
        g
    ]

However, if you flatten the text you realize you actually have 3 branches instead of 2

    [ f, {'a'}, g ]

and that wont save the value of `f` in `'a'` as you intended. To avoid this possible error, the DSL rewrites the expression during parsing to

    [ ( f, {'a'} ), g ]

every time there is a write expression inside a branch expression.

    """
    def __init__(self, name):
        super(Read, self).__init__()
        self.name = name

    def __compile__(self):
        f = lambda z: RefManager.get_ref(self.name).value
        return f


class Write(Node):

    __doc__ = Read.__doc__

    def __init__(self, ref):
        super(Write, self).__init__()
        self.ref = ref

    @staticmethod
    def __parse__(code):
        if len(code) == 0:
            return _Identity

        for ref in code:
            if not isinstance(ref, (str, Ref)):
                raise Exception("Parse Error: Sets can only contain strings or Refs, get {0}".format(code))

        writes = tuple([ Write(ref) for ref in code ])
        return _parse(writes)

    def __compile__(self):

        def f(x):
            ref = Ref(self.ref, x) if type(self.ref) is str else self.ref

            ref.set(x)
            RefManager.set_ref(ref)

            return x

        return f


class Input(Node):
    """
Sometimes you might need to branch the computation but start one of the branches with a values different than the one being passed down, you could always solve it like this

    P.Pipe(
        ...,
        [
            lambda z: my_value
        ,
            ...
        ]
    )

Here we just made a lamda that took in the argument `z` but it was completely ignored and it always returns `my_value`, this is called a constant function. You could also do the same with `P.Val` or the top level function `phi.Val`

    from phi import P, Val

    P.Pipe(
        ...,
        [
            Val(my_value)
        ,
            ...
        ]
    )|
    """
    def __init__(self, value):
        super(Input, self).__init__()
        self.value = value

    def __compile__(self):
        f = lambda x: self.value
        return f




#######################
### FUNCTIONS
#######################

def Compile(code, refs, ref_manager=True):
    """
    Hola
    """
    ast = _parse(code)
    f = ast.__compile__()

    refs = { name: value if type(value) is Ref else Ref(name, value) for name, value in refs.iteritems() }

    def g(x):
        with RefManager(refs):
            return f(x)

    return g if ref_manager else f


def _parse(code, else_input=False):
    #if type(code) is tuple:
    if isinstance(code, Node):
        return code
    elif hasattr(code, '__call__') or isclass(code):
        return Function(code)
    elif type(code) is str:
        return Read(code)
    elif type(code) is set:
        return Write.__parse__(code)
    elif type(code) is tuple:
        return Composition.__parse__(code)
    elif type(code) is dict:
        return Record.__parse__(code)
    elif hasattr(code, '__iter__') and not isclass(code): #leave last
        return Branch.__parse__(code) #its iterable
    elif else_input:
        return Input(code)
    else:
        raise Exception("Parse Error: Element not part of the DSL. Got: {0} of type {1}".format(code, type(code)))

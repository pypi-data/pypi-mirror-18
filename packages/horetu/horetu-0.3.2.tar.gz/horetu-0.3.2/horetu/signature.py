import logging
import itertools
import inspect
from functools import wraps
from funmap import funmap
from triedict import triedict
from collections import namedtuple
from copy import copy
from .exceptions import HoretuShowHelp, HoretuCouldNotParse
from enum import Enum
from .util import CallableDict
from .lib import validate_param_name

logger = logging.getLogger(__name__)

class COUNT(object):
    def __init__(self):
        self.count = 0
    def __call__(self, _):
        self.count += 1
        return self.count

class LIST(object):
    def __init__(self):
        self.xs = 0
    def __call__(self, x):
        self.xs.append(x)
        return self.xs

def show_help(x):
    raise HoretuShowHelp(x)

@funmap('name', 'call', 'takes_parameter', 'supports_positional', 'default')
def Annotation(param):
    '''
    Determine the type of a parameter. For parameters that take
    arguments.

    :param inspect.Parameter param: Parameter from the function signature
    :ivar str name: Argument name
    :ivar call: Parser function that takes one str argument as input
        (Ignore the input if you don't need it.)
    :ivar bool takes_parameter: Whether the keyword argument takes a parameter
    :ivar bool supports_positional: Whether it can be used as a positional
    :ivar default: Default value, for keyword arguments (used for
        generating default configuration files)
    '''
    default_true = 'Default of True is not supported for bool arguments; consider changing param %s to no%s and setting the default to False' % (param.name, param.name)
    if param.annotation == param.empty:
        if isinstance(param.default, bool) and \
                param.default in {True, False}:
            if param.default == True:
                raise ValueError(default_true)
            y = lambda _: not param.default, False, False
        else:
            y = str, True, True
    elif param.annotation == bool:
        if param.default == True:
            raise ValueError(default_true)
        else:
            y = lambda _: not param.default, False, False
    elif isinstance(param.annotation, tuple):
        y = Factor(copy(param.annotation)), True, True
    elif param.annotation == COUNT:
        y = COUNT(), False, False
    elif param.annotation == list:
        y = LIST(), True, False
    elif hasattr(param.annotation, '__call__'):
        y = param.annotation, True, True
    elif hasattr(param.annotation, 'keys') and \
            hasattr(param.annotation, '__getitem__'):
        def f(x):
            return param.annotation[Factor(tuple(param.annotation.keys()))(x)]
        y = f, True, True
    else:
        raise ValueError('Bad input annotation: %s' % param.annotation)

    a_, b, c = y
    def a(x):
        try:
            return a_(x)
        except HoretuCouldNotParse:
            raise
        except Exception as e:
            raise HoretuCouldNotParse('Could not parse %s: %s' %
                                      (param.name, str(e)))

    return {'name': param.name, 'default': param.default,
            'call':a, 'takes_parameter':b, 'supports_positional':c}

help_annotation = Annotation.from_dict({
    'name': 'help',
    'call': show_help,
    'takes_parameter': False,
    'supports_positional': False,
    'default': None,
})

def Factor(options):
    if all(isinstance(option, str) for option in options):
        def enum(x):
            if x in options:
                return x
            else:
                raise HoretuCouldNotParse('Must be one of %s' % str(options))
        return enum
    else:
        raise ValueError('All options must be of str type.')

@funmap('positional', 'keyword1', 'var_positional', 'keyword2')
def Signature(f, with_help=True):
    '''
    Restructure the argument information.

    :ivar list positional:
    :ivar list keyword1:
    :ivar Arg var_positional:
    :ivar dict keyword2:
    '''
    x = {
        'positional': [],
        'keyword1': [],
        'var_positional': None,
        'keyword2': triedict({'help': help_annotation} if with_help else {}),
    }
    
    sig = inspect.signature(f.func if isinstance(f, CallableDict) else f)

    for param in sig.parameters.values():
        validate_param_name(param.name)
        if param.kind == inspect.Parameter.VAR_KEYWORD and \
                not isinstance(f, CallableDict):
            raise ValueError(VAR_KWARGS)

    for kind, param in kinds(sig):
        a = Annotation(param)
        if kind == Kind.positional:
            x['positional'].append(a)
        elif kind == Kind.keyword1:
            x['keyword1'].append(a)
        elif kind == Kind.var_positional:
            x['var_positional'] = a
        elif kind == Kind.keyword2:
            x['keyword2'][param.name] = a
        else:
            raise TypeError(kind)

    return x

class Kind(Enum):
    positional = 1
    keyword1 = 2
    var_positional = 3
    keyword2 = 4

    # https://docs.python.org/3/library/enum.html#orderedenum
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

KINDS = {
    Kind.positional: {
        inspect.Parameter.POSITIONAL_ONLY,
        inspect.Parameter.POSITIONAL_OR_KEYWORD
    },
    Kind.keyword1: {inspect.Parameter.POSITIONAL_OR_KEYWORD},
    Kind.var_positional: {inspect.Parameter.VAR_POSITIONAL},
    Kind.keyword2: {inspect.Parameter.KEYWORD_ONLY},
}


VAR_KWARGS = 'Variable keyword args (**kwargs) are not allowed. You may implement your own key-value parser that takes the result of variable positional args (*args).'

def kinds(sig):
    has_k2 = Kind.keyword2 in (k for k,_ in _naive_kinds(sig))
    for kind, param in _naive_kinds(sig):
        if kind == Kind.keyword1 and not has_k2:
            yield Kind.keyword2, param
        else:
            yield kind, param

def _naive_kinds(sig):
    for param in sig.parameters.values():
        if param.kind in KINDS[Kind.positional].union(KINDS[Kind.keyword1]):
            if param.default == param.empty:
                kind = Kind.positional
            else:
                kind = Kind.keyword1
        elif param.kind in KINDS[Kind.var_positional]:
            kind = Kind.var_positional
        elif param.kind in KINDS[Kind.keyword2]:
            kind = Kind.keyword2
        yield kind, param

def TOC(prog, root_section):
    for section in sorted(prog):
        if section[:len(root_section)] == root_section:
            yield section, Signature(prog[section])

def serialize_endpoint(func):
    def endpoints(prog, section):
        for args in TOC(prog, section):
            yield func(*args)
    return endpoints

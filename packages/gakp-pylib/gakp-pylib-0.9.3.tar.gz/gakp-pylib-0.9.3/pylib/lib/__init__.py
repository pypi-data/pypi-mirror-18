from datetime import datetime
import re

from pyfunk import combinators


def remove_nones(xds):
    """
    Removes values that are None from the dict
    @sig remove_nones :: {a: b} -> {a: b}
    """
    return {k: v for k, v in xds.items() if v is not None}


def remove_empty(xds):
    """
    Removes values that are either None, or empty string from the dict
    @sig remove_empty :: {a: b} -> {a: b}
    """
    return {k: v for k, v in xds.items() if v is not None and v != ''}


@combinators.curry
def merge_dict(obj1, obj2):
    """
    Create new dict that is a combination of the two dicts passed.
    Note that the new dict my not be in the order expected
    @sig merge_dict :: {a: b} -> {a: b} -> {a: b}
    """
    tmp = obj1.copy()
    tmp.update(obj2)
    return tmp


def dict_items(obj):
    """
    Create a list of tuples(key, value) of the dict
    @sig dict_items :: {a: b} -> [(a, b)]
    """
    return list(zip(obj.keys(), obj.values()))


@combinators.curry
def only(args, obj):
    '''
    Extract some properties from an object
    @sig only :: [Str] -> {a: b} -> {a: b}
    '''
    return {k: v for k, v in dict_items(obj) if k in args}


@combinators.curry
def but(args, obj):
    '''
    Extract all properties from an object except the given ones
    @sig but :: [Str] -> {a: b} -> {a: b}
    '''
    return {k: v for k, v in dict_items(obj) if k not in args}


def is_empty(obj):
    '''
    Confirm if there is a single shred of value in the dict
    @sig has_content :: {a: b} -> Bool
    '''
    return not(obj is None or len(obj) == 0 or len(remove_empty(obj)) == 0)


@combinators.curry
def attach_method(obj, methodname, fn):
    """
    Dynamically attaches a function to an object
    @sig attach_method :: a -> Str -> (* -> _) -> _
    """
    methodname = fn.__name__ if methodname is None else methodname
    setattr(obj, methodname, bind(fn, obj))


@combinators.curry
def bind(fn, obj):
    """
    Binds a function to an object.
    @sig bind :: (* -> _) -> a -> (a -> * -> _)
    """
    return fn.__get__(obj)


def maybe(fn, test=None, n=1):
    """Call fn if and only of some first n arguments pass the given test.

    The test checks if an argument is None by default.
    """
    test = test if test is not None else lambda x: x is not None

    def newFn(*args, **kwargs):
        if len(args) < n:
            return
        else:
            all_args = args[:n]
            if all(map(test, all_args)):
                return fn(*args, **kwargs)
    return newFn


def now():
    """
    Returns the current datetime in UTC timezone
    @sig now :: _ -> DateTime
    """
    return datetime.utcnow()


def now_str():
    """
    Returns the current datetime in UTC timezone
    @sig now_str :: _ -> Str
    """
    return now().isoformat()


def regex_fn(reg):
    """
    Returns a function that creates a regex object based
    on the given string and the interpolation of the argument.
    Hence `reg` must have a `%s` in it.
    @sig regex_fn :: Str -> (Str -> RegExp)
    """
    return lambda q: re.compile(reg % q)


starts_with_regex = regex_fn('^%s')
ends_with_regex = regex_fn('%s$')
middle_regex = regex_fn('.+%s.+')

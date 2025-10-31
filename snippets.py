"""
>>> from sys import version_info
>>> assert version_info >= (3, 7, 0)
"""





from inspect import currentframe
def line_no():
    """
    Returns the current line number.
    """
    return currentframe().f_back.f_lineno

def calling_line_no():
    """
    Returns the line number of the current call site
    """
    return currentframe().f_back.f_back.f_lineno



# iteration

from itertools import tee
def pairmap(fn, itr):
    """
    Map over adjacent items.
    >>> assert pairmap(lambda pair: pair[0] + pair[1], [1, 2, 3]) == [3, 5]
    """
    a, b = tee(itr)
    next(b, None)
    return map(fn, zip(a, b))

from collections import defaultdict
from itertools import count
def numbering(**kwargs):
    """
    An identifying number for hashable items.
    >>> id_map = numbering()
    >>> assert id_map['a'] == 0
    >>> assert id_map['b'] == 1
    >>> assert id_map['a'] == 0
    """
    c = count(**kwargs)
    return defaultdict(lambda: next(c))

from operator import itemgetter
def argsort(itr):
    """
    A simple argsort.
    >>> assert argsort([3, 1, 2]) == [1, 2, 0]
    """
    return [*map(itemgetter(0), sorted(enumerate(itr), key=itemgetter(1)))]


# dict

def whitelist(dirty, allow):
    """
    Return a copy of dirty with allowed keys only, if any.
    >>> assert whitelist({'a': 1, 'b': 2}, {'b', 'c'}) == {'b': 2}
    """
    return {key: dirty[key] for key in allow if key in dirty.keys()}

def blacklist(dirty, deny):
    """
    Return a copy of dirty with denied keys removed, if any.
    >>> assert blacklist({'a': 1, 'b': 2}, {'b', 'c'}) == {'a': 1}
    """
    return {key: dirty[key] for key in dirty.keys() if key not in deny}
    
def sanitize(dirty, defaults):
    """
    Return a copy of defaults updated with matching keys from dirty, if any.
    >>> assert sanitize({'a': 1, 'b': 2}, {'b': 3, 'c': 4}) == {'b': 2, 'c': 4}
    """
    return {key: dirty.get(key, defaults[key]) for key in defaults.keys()}




# time

from time import monotonic
_MONOTONIC0 = monotonic()

from datetime import datetime
from datetime import timezone
def _nowz():
    return datetime.now(tz=timezone.utc).timestamp()

_TIMESTAMP0 = _nowz()

from time import monotonic
def _timestamp():
    """
    >>> assert type(_MONOTONIC0) is float
    >>> assert type(_TIMESTAMP0) is float
    >>> assert type(_timestamp()) is float
    """
    return monotonic() - _MONOTONIC0 + _TIMESTAMP0

from datetime import datetime
from datetime import timezone
RFC3339Z_FMT = '%Y-%m-%dT%H:%M:%S.%fZ'
def rfc3339z_timestamp():
    return datetime.now(tz=timezone.utc).strftime(RFC3339Z_FMT)

from datetime import datetime
from datetime import timezone
def to_rfc3339z(t):
    """
    >>> assert RFC3339Z_FMT == '%Y-%m-%dT%H:%M:%S.%fZ'
    >>> assert to_rfc3339z(0.0) == '1970-01-01T00:00:00.000000Z'
    """
    return datetime.fromtimestamp(t, timezone.utc).strftime(RFC3339Z_FMT)

from datetime import datetime
from datetime import timezone
def from_rfc3339z(t):
    """
    >>> assert RFC3339Z_FMT == '%Y-%m-%dT%H:%M:%S.%fZ'
    >>> assert from_rfc3339z('1970-01-01T00:00:00.000000Z') == 0.0
    """
    return datetime.strptime(t, RFC3339Z_FMT).replace(tzinfo=timezone.utc).timestamp()



# JSON

from json import loads
from pathlib import Path # implied
def load_json(path):
    return loads(path.read_text())

from json import dumps
from pathlib import Path # implied
def save_json(val, path, indent=4, default=None):
    return path.write_text(dumps(val,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        indent=indent,
        default=default
    ))

from json import dumps
def to_json(val, default=None):
    return dumps(val,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        indent=4,
        default=default,
    )

from json import dumps
def to_packed_json(val, default=None):
    return dumps(val,
        ensure_ascii=False,
        separators=(',', ':'),
        allow_nan=False,
        sort_keys=True,
        default=default,
    )

from json import load
from sys import stdin
input = load(stdin)

from json import loads
from sys import stdin
for val in map(loads, stdin):
    ...



from json import loads, dumps
def _sanitize_key(key):
    return (*loads(dumps({key: None})).keys(),)[0]

def _sanitize_value(value):
    return loads(dumps(value))

class JSONDict(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(_sanitize_key(key), _sanitize_value(value))
    def __getitem__(self, key):
        return super().__getitem__(_sanitize_key(key))
    def __delitem__(self, key):
        super().__delitem__(_sanitize_key(key))
    def __contains__(self, key):
        return super().__contains__(_sanitize_key(key))


# text

from unicodedata import normalize
def nfc(s):
    return normalize('NFC', s)

from unicodedata import normalize
def nfd(s):
    return normalize('NFD', s)

def is_not_space(s):
    """
    A filter function to weed out blank strings (e.g. empty lines).
    """
    return not s.isspace()

def next_text(itr):
    """
    Step over non-empty lines.
    """
    line = next(itr)
    while True:
        if not line.isspace():
            break
        line = next(itr)
    return line

from textwrap import dedent
def pack(txt):
    return dedent(txt).strip()

from json import dumps
def __str__(self, *attrs):
    """
    A quick and dirty object __str__.
    """
    return dumps(self.__dict__,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        default=lambda val: str(type(val))
    )

def utf8(s):
    return s.encode('utf8')

def _levenshtein(a, b):
    m, n = len(a), len(b)
    if m < n:
        a, b = b, a
        m, n = n, m
    previous = list(range(n + 1))
    for i in range(1, m + 1):
        current = [i] * (n + 1)
        for j in range(1, n + 1):
            substitution_cost = 0 if a[i - 1] == b[j - 1] else 1
            deletion = previous[j] + 1
            insertion = current[j - 1] + 1
            substitution = previous[j - 1] + substitution_cost
            current[j] = min(deletion, insertion, substitution)
        previous = current
    return previous[n]

# graph

import graphlib
def topological_sort(graph):
    """
    >>> g = {'d': {'b', 'c'}, 'c: {'b', 'a'}, 'b': {'a',},}
    >>> (*topological_sort(g),)
    ('a', 'b', 'c', 'd')
    """
    return graphlib.TopologicalSorter(graph).static_order()


# subprocesses

from subprocess import Popen
from subprocess import PIPE
def cmd(*argv):
    p = Popen(argv, stdout=PIPE, stderr=PIPE, text=True)
    output = p.communicate()
    if p.returncode != 0:
        raise RuntimeError(f'{' '.join(argv)}: {p.returncode}')
    return *output,

from shlex import quote
def sh_format(tmpl, *args, **kwargs):
    args = [quote(arg) for arg in args]
    kwargs = {kw: quote(arg) for kw, arg in kwargs.items()}
    return tmpl.format(*args, **kwargs)

def sh(tmpl, *args, **kwargs):
    return cmd('/bin/sh', '-c', sh_format(tmpl, *args, **kwargs))

# argv

def parse_named(argv):
    named = {}
    for arg in argv:
        if arg.startswith('--'):
            key, value = (*arg.split('=', 1), True)[0:2]
            named[key] = value
    return named



# async

from functools import wraps
from functools import partial
def awaitable(fn):
    @wraps(fn)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = get_event_loop()
        pfn = partial(fn, *args, **kwargs)
        return await loop.run_in_executor(executor, pfn)
    return run 



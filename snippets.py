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
def count_unique(itr):
    """
    Count occurrences of hashable items.
    >>> assert count_unique([1, 2, 1, 3]) == {1: 2, 2: 1, 3: 1}
    """
    counts = defaultdict(lambda: 0)
    for val in itr:
        counts[val] += 1
    return counts

from collections import Counter

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

from itertools import starmap
def zip_with(fn, *itrs):
    """
    Zip and apply a function.
    >>> assert [*zip_with(lambda a, b: a + b, [1, 2, 3], [4, 5, 6])] == [5, 7, 9]
    """
    return starmap(fn, zip(*itrs))



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
_TIMESTAMP0 = datetime.now(tz=timezone.utc).timestamp()

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



# subprocesses

from subprocess import run
from subprocess import Popen
from subprocess import PIPE
def command(*argv, input=None, cwd=None, env=None, timeout=None):
    return Popen(argv,
        cwd=cwd,
        env=env,
        text=True,
        stdin=PIPE,
        stdout=PIPE,
    ).communicate(input=input, timeout=timeout)

def shell(cmdline):
    return ('/bin/sh', '-c', cmdline)

from shlex import quote
def shell_format(tmpl, *args, **kwargs):
    args = [quote(arg) for arg in args]
    kwargs = {kw: quote(arg) for kw, arg in kwargs.items()}
    return tmpl.format(*args, **kwargs)



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



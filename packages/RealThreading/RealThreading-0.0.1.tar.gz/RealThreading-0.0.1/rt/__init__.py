from pyil.enum.modifiable import divide as __div
from pyil.enum.variable import auto_process
from .thread import IsoThread as IsoThread
from .lock import LockVar


def pmap(func, iterable, process=auto_process) -> iter:
    """Returns a PMap object. The usage is similar to the
    map function and does the same work except that this
    one is multi-threaded."""
    if type(process) == type(pmap):
        process = process(len(iterable))
        iterable = __div(iterable, process)
    else:
        iterable = __div(iterable, process)
    temp2 = 0

    def temp(l, fun):
        return tuple(map(fun, l))

    for i in iterable:
        temp1 = IsoThread(temp, 'mappingProcess ' + str(temp2), (i, func))
        temp1.start()
        temp2 += 1
    IsoThread.join()
    for i in IsoThread.threads:
        for j in i.result():
            yield j
            i.clean()


def pfilter(func, iterable: iter, true_only=False):
    """Uses pmap() to filter the result, same as
    the built-in filter function."""
    for i in pmap(func, iterable):
        if true_only:
            if i is True:
                yield i
        else:
            if i is not False:
                yield i


class ProcessError(Exception):
    def __init__(self, msg, etype: int = 0):
        self.msg = msg
        self.t = etype

    def __str__(self):
        return "ProcessError [%s]: %s" % (self.t, self.msg)

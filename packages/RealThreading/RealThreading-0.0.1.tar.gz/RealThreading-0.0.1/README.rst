RealThreading:
    The multi-processing module for Python 3.5.

To use:
>>>import rt
>>>t=rt.IsoThread(target_function,args=arguments,kwargs=keyword arguments)
>>>t.start()
>>>t.wait()
>>>print(t.result())
>>>t.clean()

    Since the only multi-threading module in python that truly take
the advantage of multi-core computers are multi-processing and MP
can only be used when not imported; also, parallel python(pp) only
work for python 2.X. So, I developed RealThreading which works pretty
much the same way as pp and does the same job but it works for python
3.X.
    Contact me at G.Mpydev@gmail.com
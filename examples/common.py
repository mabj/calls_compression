import inspect

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def generic_call(_id, pos):
    print('ID: {:02d}, Line: {:02d}'.format(_id, pos))

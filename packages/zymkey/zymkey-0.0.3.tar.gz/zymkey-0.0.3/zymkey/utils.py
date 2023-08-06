# https://github.com/oxplot/fysom/issues/1#issue-3668262
try:
    unicode = unicode
except NameError:  # 'unicode' is undefined, must be Python 3
    def is_string(buf):
        return isinstance(buf, str)
else:  # 'unicode' exists, must be Python 2
    def is_string(buf):
        return isinstance(buf, basestring)

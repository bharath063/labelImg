import sys

def ustr(x):
    '''py2/py3 unicode helper'''

    if sys.version_info < (3, 0, 0):
        try:
            from PyQt4.QtCore import QString
            if type(x) == str:
                return x.decode('utf-8')
            if type(x) == QString:
                return unicode(x)
        except:
            # No Qt4. Qt5 automatically converts QString to string
            return unicode(x)
    else:
        return x  # py3

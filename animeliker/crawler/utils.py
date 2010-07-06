import re
def normpath(path):
    path = path.replace('\\', '/').replace('\\\\', '/')
    return path


import locale
locale.setlocale(locale.LC_ALL, '')
def guess_encoding(data):
    successful_encoding = None
    
    encodings = []
    encodings.append('latin-1')
    encodings.append('utf-8')
    try:
        encodings.append(locale.nl_langinfo(locale.CODESET))
    except AttributeError:
        pass
    try:
        encodings.append(locale.getlocale()[1])
    except (AttributeError, IndexError):
        pass
    try:
        encodings.append(locale.getdefaultlocale()[1])
    except (AttributeError, IndexError):
        pass
    
    
    for enc in encodings:
        if not enc:
            continue
        try:
            unicode(data, enc)
            successful_encoding = enc

        except (UnicodeError, LookupError):
            pass
        except TypeError:
            return 'utf-8'
        else:
            break
    if not successful_encoding:
        return False
    else:
        return successful_encoding
     
def decode(data):
    encoding = guess_encoding(data)
    if not encoding:
        print 'decoding error'
    if encoding not in ['utf-8']:
        return data.decode(encoding)
    return data

def decode_list(list):
    newlist = []
    for item in list:
        newlist.append(decode(item))
    return newlist


def read_in_chunks(file_object, chunk_size=4096):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data
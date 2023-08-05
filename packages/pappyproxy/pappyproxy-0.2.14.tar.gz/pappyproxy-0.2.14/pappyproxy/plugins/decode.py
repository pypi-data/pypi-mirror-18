import HTMLParser
import StringIO
import base64
import datetime
import gzip
import shlex
import string
import urllib

from pappyproxy.util import PappyException, hexdump, printable_data, copy_to_clipboard, clipboard_contents

def print_maybe_bin(s):
    binary = False
    for c in s:
        if c not in string.printable:
            binary = True
            break
    if binary:
        print hexdump(s)
    else:
        print s
        
def asciihex_encode_helper(s):
    return ''.join('{0:x}'.format(ord(c)) for c in s)

def asciihex_decode_helper(s):
    ret = []
    try:
        for a, b in zip(s[0::2], s[1::2]):
            c = a+b
            ret.append(chr(int(c, 16)))
        return ''.join(ret)
    except Exception as e:
        raise PappyException(e)
    
def gzip_encode_helper(s):
    out = StringIO.StringIO()
    with gzip.GzipFile(fileobj=out, mode="w") as f:
        f.write(s)
    return out.getvalue()
    
def gzip_decode_helper(s):
    dec_data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(s))
    dec_data = dec_data.read()
    return dec_data

def base64_decode_helper(s):
    try:
        return base64.b64decode(s)
    except TypeError:
        for i in range(1, 5):
            try:
                s_padded = base64.b64decode(s + '='*i)
                return s_padded
            except:
                pass
        raise PappyException("Unable to base64 decode string")

def html_encode_helper(s):
    return ''.join(['&#x{0:x};'.format(ord(c)) for c in s])

def html_decode_helper(s):
    return HTMLParser.HTMLParser().unescape(s)

def _code_helper(line, func, copy=True):
    args = shlex.split(line)
    if not args:
        s = clipboard_contents()
        print 'Will decode:'
        print printable_data(s)
        s = func(s)
        if copy:
            try:
                copy_to_clipboard(s)
            except:
                print 'Result cannot be copied to the clipboard. Result not copied.'
        return s
    else:
        s = func(args[0].strip())
        if copy:
            try:
                copy_to_clipboard(s)
            except:
                print 'Result cannot be copied to the clipboard. Result not copied.'
        return s

def base64_decode(line):
    """
    Base64 decode a string.
    If no string is given, will decode the contents of the clipboard.
    Results are copied to the clipboard.
    """
    print_maybe_bin(_code_helper(line, base64_decode_helper))

def base64_encode(line):
    """
    Base64 encode a string.
    If no string is given, will encode the contents of the clipboard.
    Results are copied to the clipboard.
    """
    print_maybe_bin(_code_helper(line, base64.b64encode))

def url_decode(line):
    """
    URL decode a string.
    If no string is given, will decode the contents of the clipboard.
    Results are copied to the clipboard.
    """
    print_maybe_bin(_code_helper(line, urllib.unquote))

def url_encode(line):
    """
    URL encode special characters in a string.
    If no string is given, will encode the contents of the clipboard.
    Results are copied to the clipboard.
    """
    print_maybe_bin(_code_helper(line, urllib.quote_plus))

def asciihex_decode(line):
    """
    Decode an ascii hex string.
    If no string is given, will decode the contents of the clipboard.
    Results are copied to the clipboard.
    """
    print_maybe_bin(_code_helper(line, asciihex_decode_helper))

def asciihex_encode(line):
    """
    Convert all the characters in a line to hex and combine them.
    If no string is given, will encode the contents of the clipboard.
    Results are copied to the clipboard.
    """
    print_maybe_bin(_code_helper(line, asciihex_encode_helper))

def html_decode(line):
    """
    Decode an html encoded string.
    If no string is given, will decode the contents of the clipboard.
    Results are copied to the clipboard.
    """
    print_maybe_bin(_code_helper(line, html_decode_helper))

def html_encode(line):
    """
    Encode a string and escape html control characters.
    If no string is given, will encode the contents of the clipboard.
    Results are copied to the clipboard.
    """
    print_maybe_bin(_code_helper(line, html_encode_helper))
    
def gzip_decode(line):
    """
    Un-gzip a string.
    If no string is given, will decompress the contents of the clipboard.
    Results are copied to the clipboard.
    """
    print_maybe_bin(_code_helper(line, gzip_decode_helper))

def gzip_encode(line):
    """
    Gzip a string.
    If no string is given, will decompress the contents of the clipboard.
    Results are NOT copied to the clipboard.
    """
    print_maybe_bin(_code_helper(line, gzip_encode_helper, copy=False))

def base64_decode_raw(line):
    """
    Same as base64_decode but the output will never be printed as a hex dump and
    results will not be copied. It is suggested you redirect the output
    to a file.
    """
    print _code_helper(line, base64_decode_helper, copy=False)

def base64_encode_raw(line):
    """
    Same as base64_encode but the output will never be printed as a hex dump and
    results will not be copied. It is suggested you redirect the output
    to a file.
    """
    print _code_helper(line, base64.b64encode, copy=False)

def url_decode_raw(line):
    """
    Same as url_decode but the output will never be printed as a hex dump and
    results will not be copied. It is suggested you redirect the output
    to a file.
    """
    print _code_helper(line, urllib.unquote, copy=False)

def url_encode_raw(line):
    """
    Same as url_encode but the output will never be printed as a hex dump and
    results will not be copied. It is suggested you redirect the output
    to a file.
    """
    print _code_helper(line, urllib.quote_plus, copy=False)

def asciihex_decode_raw(line):
    """
    Same as asciihex_decode but the output will never be printed as a hex dump and
    results will not be copied. It is suggested you redirect the output
    to a file.
    """
    print _code_helper(line, asciihex_decode_helper, copy=False)

def asciihex_encode_raw(line):
    """
    Same as asciihex_encode but the output will never be printed as a hex dump and
    results will not be copied. It is suggested you redirect the output
    to a file.
    """
    print _code_helper(line, asciihex_encode_helper, copy=False)
    
def html_decode_raw(line):
    """
    Same as html_decode but the output will never be printed as a hex dump and
    results will not be copied. It is suggested you redirect the output
    to a file.
    """
    print _code_helper(line, html_decode_helper, copy=False)

def html_encode_raw(line):
    """
    Same as html_encode but the output will never be printed as a hex dump and
    results will not be copied. It is suggested you redirect the output
    to a file.
    """
    print _code_helper(line, html_encode_helper, copy=False)

def gzip_decode_raw(line):
    """
    Same as gzip_decode but the output will never be printed as a hex dump and
    results will not be copied. It is suggested you redirect the output
    to a file.
    """
    print _code_helper(line, gzip_decode_helper, copy=False)

def gzip_encode_raw(line):
    """
    Same as gzip_encode but the output will never be printed as a hex dump and
    results will not be copied. It is suggested you redirect the output
    to a file.
    """
    print _code_helper(line, gzip_encode_helper, copy=False)
    
def unix_time_decode_helper(line):
    unix_time = int(line.strip())
    dtime = datetime.datetime.fromtimestamp(unix_time)
    return dtime.strftime('%Y-%m-%d %H:%M:%S')

def unix_time_decode(line):
    print _code_helper(line, unix_time_decode_helper)
        
def load_cmds(cmd):
    cmd.set_cmds({
        'base64_decode': (base64_decode, None),
        'base64_encode': (base64_encode, None),
        'asciihex_decode': (asciihex_decode, None),
        'asciihex_encode': (asciihex_encode, None),
        'url_decode': (url_decode, None),
        'url_encode': (url_encode, None),
        'html_decode': (html_decode, None),
        'html_encode': (html_encode, None),
        'gzip_decode': (gzip_decode, None),
        'gzip_encode': (gzip_encode, None),
        'base64_decode_raw': (base64_decode_raw, None),
        'base64_encode_raw': (base64_encode_raw, None),
        'asciihex_decode_raw': (asciihex_decode_raw, None),
        'asciihex_encode_raw': (asciihex_encode_raw, None),
        'url_decode_raw': (url_decode_raw, None),
        'url_encode_raw': (url_encode_raw, None),
        'html_decode_raw': (html_decode_raw, None),
        'html_encode_raw': (html_encode_raw, None),
        'gzip_decode_raw': (gzip_decode_raw, None),
        'gzip_encode_raw': (gzip_encode_raw, None),
        'unixtime_decode': (unix_time_decode, None),
    })
    cmd.add_aliases([
        ('base64_decode', 'b64d'),
        ('base64_encode', 'b64e'),
        ('asciihex_decode', 'ahd'),
        ('asciihex_encode', 'ahe'),
        ('url_decode', 'urld'),
        ('url_encode', 'urle'),
        ('html_decode', 'htmld'),
        ('html_encode', 'htmle'),
        ('gzip_decode', 'gzd'),
        ('gzip_encode', 'gze'),
        ('base64_decode_raw', 'b64dr'),
        ('base64_encode_raw', 'b64er'),
        ('asciihex_decode_raw', 'ahdr'),
        ('asciihex_encode_raw', 'aher'),
        ('url_decode_raw', 'urldr'),
        ('url_encode_raw', 'urler'),
        ('html_decode_raw', 'htmldr'),
        ('html_encode_raw', 'htmler'),
        ('gzip_decode_raw', 'gzdr'),
        ('gzip_encode_raw', 'gzer'),
        ('unixtime_decode', 'uxtd'),
    ])

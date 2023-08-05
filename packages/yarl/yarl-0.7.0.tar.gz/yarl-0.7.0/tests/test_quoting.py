import pytest

from yarl.quoting import _py_quote, _py_unquote, _quote, _unquote


@pytest.fixture(params=[_py_quote, _quote], ids=['py_quote', 'c_quote'])
def quote(request):
    return request.param


@pytest.fixture(params=[_py_unquote, _unquote],
                ids=['py_unquote', 'c_unquote'])
def unquote(request):
    return request.param


def hexescape(char):
    """Escape char as RFC 2396 specifies"""
    hex_repr = hex(ord(char))[2:].upper()
    if len(hex_repr) == 1:
        hex_repr = "0%s" % hex_repr
    return "%" + hex_repr


def test_quote_not_allowed(quote):
    with pytest.raises(ValueError):
        quote('%HH')


def test_quote_unfinished(quote):
    with pytest.raises(ValueError):
        quote('%F%F')


def test_quote_from_bytes(quote):
    assert quote('archaeological arcana') == 'archaeological%20arcana'
    assert quote('') == ''


def test_unquote_to_bytes(unquote):
    assert unquote('abc%20def') == 'abc def'
    assert unquote('') == ''


def test_never_quote(quote):
    # Make sure quote() does not quote letters, digits, and "_,.-"
    do_not_quote = '' .join(["ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                             "abcdefghijklmnopqrstuvwxyz",
                             "0123456789",
                             "_.-"])
    assert quote(do_not_quote) == do_not_quote
    quote(do_not_quote, plus=True) == do_not_quote


def test_safe(quote):
    # Test setting 'safe' parameter does what it should do
    quote_by_default = "<>"
    assert quote(quote_by_default, safe=quote_by_default) == quote_by_default

    ret = quote(quote_by_default, safe=quote_by_default, plus=True)
    assert ret == quote_by_default


SHOULD_QUOTE = [chr(num) for num in range(32)]
SHOULD_QUOTE.append('<>#"{}|\^[]`')
SHOULD_QUOTE.append(chr(127))  # For 0x7F
SHOULD_QUOTE = ''.join(SHOULD_QUOTE)


@pytest.mark.parametrize('char', SHOULD_QUOTE)
def test_default_quoting(char, quote):
    # Make sure all characters that should be quoted are by default sans
    # space (separate test for that).
    result = quote(char)
    assert hexescape(char) == result
    result = quote(char, plus=True)
    assert hexescape(char) == result


# TODO: should it encode percent?
def test_default_quoting_percent(quote):
    result = quote('%25')
    assert '%25' == result
    result = quote('%25', plus=True)
    assert '%25' == result


def test_default_quoting_partial(quote):
    partial_quote = "ab[]cd"
    expected = "ab%5B%5Dcd"
    result = quote(partial_quote)
    assert expected == result
    result = quote(partial_quote, plus=True)
    assert expected == result


def test_quoting_space(quote):
    # Make sure quote() and quote_plus() handle spaces as specified in
    # their unique way
    result = quote(' ')
    assert result == hexescape(' ')
    result = quote(' ', plus=True)
    assert result == '+'

    given = "a b cd e f"
    expect = given.replace(' ', hexescape(' '))
    result = quote(given)
    assert expect == result
    expect = given.replace(' ', '+')
    result = quote(given, plus=True)
    assert expect == result


def test_quoting_plus(quote):
    assert quote('alpha+beta gamma', plus=True) == 'alpha%2Bbeta+gamma'
    assert quote('alpha+beta gamma', safe='+', plus=True) == 'alpha+beta+gamma'


def test_quote_with_unicode(quote):
    # Characters in Latin-1 range, encoded by default in UTF-8
    given = "\xa2\xd8ab\xff"
    expect = "%C2%A2%C3%98ab%C3%BF"
    result = quote(given)
    assert expect == result
    # Characters in BMP, encoded by default in UTF-8
    given = "\u6f22\u5b57"              # "Kanji"
    expect = "%E6%BC%A2%E5%AD%97"
    result = quote(given)
    assert expect == result


def test_quote_plus_with_unicode(quote):
    # Characters in Latin-1 range, encoded by default in UTF-8
    given = "\xa2\xd8ab\xff"
    expect = "%C2%A2%C3%98ab%C3%BF"
    result = quote(given, plus=True)
    assert expect == result
    # Characters in BMP, encoded by default in UTF-8
    given = "\u6f22\u5b57"              # "Kanji"
    expect = "%E6%BC%A2%E5%AD%97"
    result = quote(given, plus=True)
    assert expect == result


@pytest.mark.parametrize('num', list(range(128)))
def test_unquoting(num, unquote):
    # Make sure unquoting of all ASCII values works
    given = hexescape(chr(num))
    expect = chr(num)
    result = unquote(given)
    assert expect == result
    result = unquote(given, plus=True)
    assert expect == result


@pytest.mark.xfail
def test_unquoting_badpercent(unquote):
    # Test unquoting on bad percent-escapes
    given = '%xab'
    expect = given
    result = unquote(given)
    assert expect == result


@pytest.mark.xfail
def test_unquoting_badpercent2(unquote):
    given = '%x'
    expect = given
    result = unquote(given)
    assert expect == result


@pytest.mark.xfail
def test_unquoting_badpercent3(unquote):
    given = '%'
    expect = given
    result = unquote(given)
    assert expect == result


@pytest.mark.xfail
def test_unquoting_mixed_case(unquote):
    # Test unquoting on mixed-case hex digits in the percent-escapes
    given = '%Ab%eA'
    expect = '\xab\xea'
    result = unquote(given)
    assert expect == result


def test_unquoting_parts(unquote):
    # Make sure unquoting works when have non-quoted characters
    # interspersed
    given = 'ab%sd' % hexescape('c')
    expect = "abcd"
    result = unquote(given)
    assert expect == result
    result = unquote(given, plus=True)
    assert expect == result


def test_quote_None(quote):
    assert quote(None) is None


def test_unquote_None(unquote):
    assert unquote(None) is None


def test_quote_empty_string(quote):
    assert quote('') == ''


def test_unempty_string(unquote):
    assert unquote('') == ''


def test_quote_bad_types(quote):
    with pytest.raises(TypeError):
        quote(123)


def test_unquote_bad_types(unquote):
    with pytest.raises(TypeError):
        unquote(123)


def test_quote_lowercase(quote):
    assert quote('%d1%84') == '%D1%84'


def test_quote_unquoted(quote):
    assert quote('%41') == 'A'


def test_unquote_unsafe(unquote):
    assert unquote('%26', unsafe='&') == '%26'


def test_unquote_unsafe2(unquote):
    assert unquote('%26abc', unsafe='&') == '%26abc'


def test_unquote_non_ascii(unquote):
    assert unquote('%F8') == '%F8'


def test_unquote_non_ascii_non_tailing(unquote):
    assert unquote('%F8ab') == '%F8ab'


def test_quote_non_ascii(quote):
    assert quote('%F8') == '%F8'


def test_quote_non_ascii2(quote):
    assert quote('a%F8b') == 'a%F8b'

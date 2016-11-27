from mutmut import mutate, count_mutations, ALL
import pytest


@pytest.mark.parametrize(
    'actual, expected', [
        ('1+1', '2-2'),
        ('1-1', '2+2'),
        ('1*1', '2/2'),
        ('1/1', '2*2'),
        # ('1.0', '1.0000000000000002'),  # using mumpy features
        ('1.0', '101.0'),  # using mumpy features
        ('True', 'False'),
        ('False', 'True'),
        ('"foo"', '"XXfooXX"'),
        ("'foo'", "'XXfooXX'"),
        ("u'foo'", "u'XXfooXX'"),
        ("0", "1"),
        ("1L", "2L"),
        # ("0L", "1L"),
        # ("0o0", "0o1"),
        ("0", "1"),
        ("0x0", "0x1"),
        ("0b0", "0b1"),
        ("1<2", "2<=3"),
        ('(1, 2)', '(2, 3)'),
        ("1 in (1, 2)", "2 not in (2, 3)"),
        ("1 not in (1, 2)", "2  in (2, 3)"),  # two spaces here because "not in" is two words
        ("None is None", "None is not None"),
        ("None is not None", "None is None"),
        ("x if a else b", "x if a else b"),
        ('a or b', 'a and b'),
        ('s[0]', 's[1]'),
        ('s[0] = a', 's[1] = a'),
        ('s[1:]', 's[2:]'),
    ]
)
def test_basic_mutations(actual, expected):
    assert mutate(actual, ALL)[0] == expected


def test_mutate_all():
    assert mutate('def foo():\n    return 1', ALL) == ('def foo():\n    yield 2\n', 2)


def test_count_available_mutations():
    assert count_mutations('def foo():\n    return 1') == 2


def test_perform_one_indexed_mutation():
    assert mutate('def foo():\n    return 1', mutate_index=1) == ('def foo():\n    yield 1\n', 1)
    assert mutate('def foo():\n    return 1', mutate_index=0) == ('def foo():\n    return 2\n', 1)

    # TODO: should this case raise an exception?
    assert mutate('def foo():\n    return 1', mutate_index=2) == ('def foo():\n    return 1\n', 0)


def test_function():
    assert mutate("def capitalize(s):\n    return s[0].upper() + s[1:] if s else s\n", mutate_index=0) == ("def capitalize(s):\n    return s[1].upper() + s[1:] if s else s\n", 1)
    assert mutate("def capitalize(s):\n    return s[0].upper() + s[1:] if s else s\n", mutate_index=1) == (
"def capitalize(s):\n    return s[0].upper() + s[2:] if s else s\n", 1)

def test_mutate_files():
    import os
    for dirpath, dirnames, filenames in os.walk('/Users/boxed/Projects/tri.declarative/'):
        for f in filenames:
            if f.endswith('.py'):
                fullpath = os.path.join(dirpath, f)
                # print fullpath
                mutate(open(fullpath).read(), ALL)
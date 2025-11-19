"""Единственный тест для CI который всегда проходит"""

def test_always_passes():
    """Тест который всегда проходит"""
    assert 1 + 1 == 2

def test_basic_math():
    """Еще один простой тест"""
    assert 2 * 2 == 4

def test_boolean():
    """Булевый тест"""
    assert True is True

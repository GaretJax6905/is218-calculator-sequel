import pytest
from calculator.calculation import Add
from calculator.history import History


def test_history_starts_empty():
    h = History()
    assert len(h.get_history()) == 0


def test_history_add():
    h = History()
    h.add(Add(10, 5))
    assert len(h.get_history()) == 1


def test_history_add_invalid():
    h = History()
    with pytest.raises(TypeError):
        h.add("invalid")


def test_history_shallow_copy():
    h = History()
    h.add(Add(10, 5))
    snapshot = h.get_history()
    snapshot.clear()
    assert len(h.get_history()) == 1


def test_history_remove():
    h = History()
    item = Add(10, 5)
    h.add(item)
    removed = h.remove(0)
    assert removed is item
    assert len(h.get_history()) == 0


def test_history_remove_negative_index():
    h = History()
    h.add(Add(10, 5))
    with pytest.raises(IndexError):
        h.remove(-1)


def test_history_remove_out_of_bounds():
    h = History()
    h.add(Add(10, 5))
    with pytest.raises(IndexError):
        h.remove(2)


# Stage 3 Independent Test:
def test_remove_from_empty_history():
    h = History()
    with pytest.raises(IndexError):
        h.remove(0)
    assert len(h.get_history()) == 0
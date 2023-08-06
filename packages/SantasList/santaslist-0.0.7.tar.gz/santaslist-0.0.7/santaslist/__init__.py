# __init__.py
import random


__author__ = 'Jeffrey Hann'
__version__ = '0.0.7'

_people = []
_pairs = []


class Pairs(list):
    _pairs = []

    def __init__(self, data: list) -> None:
        """
        Load a list of People and pair them

        :param people:
        :rtype: None
        """
        assert isinstance(data, list)

        while len(data) > 0:
            a = self._pop_list(data)
            b = self._pop_list(data)

            self._pairs.append((a, b))

        list.__init__(self, self._pairs)

    def __str__(self) -> str:
        """
        Return all pairs in a string

        :rtype: str
        """
        return '\n'.join(self._print_pair(x) for x in self._pairs)

    @staticmethod
    def _print_pair(pair: tuple) -> str:
        """
        Print all the pairs

        :param pair: tuple
        :rtype: str
        """
        return '%s <---> %s' % (_print_person(pair[0]), _print_person(pair[1]))

    @staticmethod
    def _pop_list(my_list: list) -> dict:
        """
        Take a list of People and remove a random choice, then remove that Person

        :param my_list:
        :rtype: dict
        """
        assert isinstance(my_list, list)
        indices = list(range(0, len(my_list)))

        x = random.choice(indices)
        y = my_list[x]

        del indices[x]
        del my_list[x]

        return y


def load_people(data: list) -> list:
    """
    Load a list of people

    :param data: list
    :rtype: list
    """

    global _people, _pairs
    _people = data
    _pairs = Pairs(_people[:])

    assert isinstance(_people, list)
    assert isinstance(_pairs, Pairs)

    return _people


def _print_person(data:dict) -> str:
    """
    Print a person dictionary in a sexy format

    :param data: dict
    :rtype: str
    """
    assert 'name' in data and 'username' in data
    return '%s (%s)' % (data['name'], data['username'])


def people() -> list:
    """
    Return all people

    :rtype: list
    """
    return _people


def print_people() -> str:
    """
    return a nicely formatted string of people

    :rtype: str
    """
    return ','.join(_print_person(x) for x in _people)


def pairs() -> Pairs:
    """
    return Pairs

    :rtype: Pairs
    """
    return _pairs


def print_pairs() -> str:
    """
    Return a nice sexy list of all paired people

    :rtype: str
    """
    return str(_pairs)

# -*- coding: utf-8 -*-

import re
from copy import deepcopy


class Converter(object):
    COST = 100
    CHARACTERS = '[^{split}]+'

    def __init__(self):
        self.cost = self.COST
        self.characters = self.CHARACTERS

    def copy(self, split):
        c = deepcopy(self)
        c.characters = c.characters.replace('{split}', split)
        return c

    def __call__(self, value):
        return str(value)


class IntConverter(Converter):
    COST = 50
    CHARACTERS = '[-+]?[1-9][0-9]*'

    def __call__(self, value):
        return int(value)


class GreedyConverter(Converter):
    COST = 500
    CHARACTERS = '.*'


CONVERTERS = {
    'int': IntConverter(),
    'str': Converter(),
    'greedy': GreedyConverter(),
}

_path_re = re.compile(r'''
    (?P<static>[^<]*)                                        # static path data
    <
        (?P<variable_name>[a-z][a-z0-9_]*)                   # variable
        (?:\|                                                # converter start
            (?P<converter_name>[a-z]+)
        )?                                                   # converter end
    >
''', re.VERBOSE)


class Path(object):
    """Path that can be used to match (and extract variables) from a string.
    :attribute original: Original and unparsed path-value.
    :attribute regex: Regular (compiled) expression of the original value.
    :attribute cost: Calculate cost of the path.
    :attribute variables: Variables this path provides.
    :type original: str
    :type converters: dict
    :type split: str
    :type regex: _sre.SRE_Pattern
    :type variables: dict[str, Converter]
    """

    def __init__(self, value, converters=None, split='/'):
        """Path that can be used to match (and extract variables) from a
        string.
        :param value: Value to be parsed as a path.
        :param converters: Mapping of available converters.
        :param split: Path splitting value, defaults to '/'.
        :type value: str
        :type converters: dict | None
        :type split: str
        """
        self.original = value
        self.converters = dict()

        for name, converter in (converters or CONVERTERS).items():
            self.converters[name] = converter.copy(split)

        self.regex, self.cost, self.variables = path_parse(self.original,
                                                           self.converters)

    def __call__(self, string):
        """Run the path over a string.
        :param string: String to match against the path.
        :return: A dictionary of matches variables, or None if not matched.
        :type string: str
        :rtype: dict | None
        """
        match = self.regex.search(string)

        if match is not None:
            result = dict()

            for name, value in match.groupdict().items():
                converter = self.variables[name]
                result[name] = converter(value)

            return result
        else:
            return None

    def __lt__(self, other):
        """Compare a path to another path (based on the cost)."""
        return path_build_compare(self) < path_build_compare(other)

    def __eq__(self, other):
        """Compare a path to another path (based on the cost)."""
        return path_build_compare(self) == path_build_compare(other)

    def __repr__(self):
        """Represent the path."""
        return '<Path ({:s})>'.format(self.regex.pattern)

    __ne__ = lambda s, o: not s == o
    __gt__ = lambda s, o: not s < o and not s == o


def path_parse(value, converters):
    pos = 0
    end = len(value)
    _match = _path_re.match

    regex = list()
    weights = list()
    variables = dict()

    while pos < end:
        m = _match(value, pos)
        if m is None:
            break

        data = m.groupdict()
        pos = m.end()

        if data['converter_name']:
            converter = converters[data['converter_name']]
        else:
            converter = converters['str']

        variables[data['variable_name']] = converter

        regex.append(re.escape(data['static']))
        regex.append('(?P<{:s}>{:s})'.format(data['variable_name'],
                                             converter.characters))

        weights.append([0, -len(data['static'])])
        weights.append([1, converter.cost])

    if pos < end:
        remainder = value[pos:]

        regex.append(re.escape(remainder))
        weights.append([0, -len(remainder)])

    rgx = re.compile(u'^{:s}$'.format(u''.join(regex)), re.UNICODE)

    return rgx, weights, variables


def path_build_compare(path):
    if isinstance(path, Path):
        return bool(path.variables), -len(path.cost), path.cost
    elif isinstance(path, (list, tuple)):
        return tuple(path)
    else:
        raise ValueError('Uncomparible argument.')

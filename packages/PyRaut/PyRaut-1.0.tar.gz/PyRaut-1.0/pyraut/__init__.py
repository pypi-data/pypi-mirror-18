# -*- coding: utf-8 -*-
import logging
import operator
from typing import List

from .path import Path
from .processors import Match, Processor
from .processors import MatchError
from .processors import PathProcessor
from .processors import ProvideProcessor
from .processors import ValueProcessor

logger = logging.getLogger('raut')


class RautException(Exception):
    pass


class RautMissingArgument(RautException):
    pass


class RautSkip(RautException):
    pass


class RautNotFound(RautException):
    pass


class Raut(object):
    def __init__(self, processors: List[Processor] = None):
        self.routes = list()
        self.processors = processors or list()  # List[Processor]

    def attach(self, **kwargs):
        def inner(func):
            self.routes.append(Route(self, kwargs, func))
            return func

        return inner

    def match(self, **kwargs):
        values = list()
        matches = list()

        for processor in list(self.processors):
            if processor.name not in kwargs:
                raise RautMissingArgument('Missing %s.' % processor.name)
            values.append((processor, kwargs[processor.name]))

        for route in self.routes:
            try:
                match = Match()
                for processor, value in values:
                    match.update(processor(value, route))
            except MatchError:
                pass
            else:
                matches.append([route, match])

        if len(matches):
            size = max(map(len, [m[1].score for m in matches]))
            matches = list(filter(lambda m: len(m[1].score) == size, matches))
            matches.sort(key=operator.itemgetter(1))

        logger.debug('Matched %s', [v[1] for v in values])
        for match in matches:
            logger.debug('Match - %s', match)

        return matches

    def solve(self, **kwargs):
        for path, match in self.match(**kwargs):
            try:
                return path.func(**match.kwargs)
            except RautSkip:
                logger.debug('Callback raised RautSkip for match %s', match)

        raise RautNotFound()

    def blueprint(self, **kwargs):
        return Blueprint(self, **kwargs)

    def add_processor(self, processor: Processor) -> 'Raut':
        self.processors.append(processor)
        return self


class Route(object):
    def __init__(self, raut, kwargs, func):
        self.raut = raut
        self.kwargs = kwargs
        self.func = func


class Blueprint(object):
    def __init__(self, raut, **kwargs):
        self.raut = raut
        self.kwargs = kwargs

    def attach(self, **kwargs):
        for processor in self.raut.processors:  # type: Processor
            name = processor.name
            blueprint_value = self.kwargs.get(name)
            value = kwargs.get(name, blueprint_value)

            kwargs[name] = processor.blueprint(value, blueprint_value)

        return self.raut.attach(**kwargs)

# -*- coding: utf-8 -*-
from contextlib import contextmanager

from pytest import raises

import pyraut as r


@contextmanager
def should_raise(exception, message=None):
    with raises(exception) as err:
        yield

    if message is not None:
        assert str(err.value) == message, str(err.value)


def test_is_present():
    assert r


def test_one():
    raut = r.Raut()
    raut.add_processor(r.PathProcessor('path'))

    @raut.attach(path='/')
    def route_root():
        return 'route /'

    @raut.attach(path='/one')
    def route_one():
        return 'route /one'

    @raut.attach(path='/two')
    def route_two():
        return 'route /two'

    same = raut.blueprint()

    @same.attach(path='/three')
    def route_three():
        return 'route /three'

    sub = raut.blueprint(path='/sub')

    @sub.attach(path='')
    def route_sub_root():
        return 'route /sub'

    @sub.attach(path='/one')
    def route_sub_one():
        return 'route /sub/one'

    @sub.attach(path='/two')
    def route_sub_two():
        return 'route /sub/two'

    assert raut.solve(path='/') == 'route /'
    assert raut.solve(path='/two') == 'route /two'
    assert raut.solve(path='/three') == 'route /three'
    assert raut.solve(path='/sub') == 'route /sub'
    assert raut.solve(path='/sub/two') == 'route /sub/two'

    with should_raise(r.RautNotFound):
        raut.solve(path='/unknown')


def test_two():
    raut = r.Raut()
    raut.add_processor(r.PathProcessor('path'))
    raut.add_processor(r.ValueProcessor('method', optional=True))

    @raut.attach(path='/')
    def route_root():
        return 'route /'

    @raut.attach(path='/one', method='GET')
    def route_get_one():
        return 'route get /one'

    @raut.attach(path='/one', method='POST')
    def route_post_one():
        return 'route post /one'

    sub = raut.blueprint(path='/sub')

    @sub.attach(path='/one', method='GET')
    def route_sub_get_one():
        return 'route get /sub/one'

    @sub.attach(path='/one', method='POST')
    def route_sub_post_one():
        return 'route post /sub/one'

    @sub.attach(path='/one/§')
    def route_one_sub():
        return 'route /one/sub'

    sub_only_put = raut.blueprint(path='/sub', method='PUT')

    @sub_only_put.attach(path='/one')
    def route_sub_only_put_one():
        return 'route put /sub/one'

    assert raut.solve(path='/', method='GET') == 'route /'
    assert raut.solve(path='/one', method='POST') == 'route post /one'
    assert raut.solve(path='/sub/one', method='POST') == 'route post /sub/one'
    assert raut.solve(path='/sub/one', method='PUT') == 'route put /sub/one'
    assert raut.solve(path='/one/sub', method='PUT') == 'route /one/sub'

    with should_raise(r.RautNotFound):
        raut.solve(path='/unknown', method='PUT')

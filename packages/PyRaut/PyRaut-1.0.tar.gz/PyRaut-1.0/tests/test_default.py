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


def test_simple():
    raut = r.Raut()
    raut.add_processor(r.PathProcessor('path'))

    @raut.attach(path='/')
    def route_root():
        return 'route /'

    assert raut.solve(path='/') == 'route /'

    with should_raise(r.RautNotFound):
        raut.solve(path='/unknown')

    route, match = raut.match(path='/')[0]
    assert repr(match) == '<Match (score=[<Path (^\/$)>])>'


def test_params():
    raut = r.Raut()
    raut.add_processor(r.PathProcessor('path'))
    raut.add_processor(r.ValueProcessor('method', optional=True))

    @raut.attach(path='/post/<id|int>')
    def route_post_by_id(id):
        return 'post %d' % id

    @raut.attach(path='/post/<id|int>', method='PATCH')
    def route_update_post_by_id(id):
        return 'update post %d' % id

    @raut.attach(path='/post/<name|str>')
    def route_post_by_name(name):
        return 'post %s' % name

    @raut.attach(path='/post/<name>/edit')
    def route_edit_post_by_name(name):
        return 'edit post %s' % name

    @raut.attach(path='/post/<other|greedy>')
    def route_post_not_found(other):
        return 'error %s' % other

    assert raut.solve(path='/post/44', method='GET') == 'post 44'
    assert raut.solve(path='/post/44', method='PATCH') == 'update post 44'
    assert raut.solve(path='/post/four', method='GET') == 'post four'
    assert raut.solve(path='/post/44/edit', method='GET') == 'edit post 44'
    assert raut.solve(path='/post/44/x', method='GET') == 'error 44/x'


def test_multiple():
    raut = r.Raut()
    raut.add_processor(r.PathProcessor('path'))
    raut.add_processor(r.ValueProcessor('method', optional=True))

    @raut.attach(path='/', method=['GET', 'HEAD', 'OPTIONS'])
    def route_root():
        return 'route /'

    @raut.attach(path='/one', method='GET')
    def route_one():
        return 'route /one'

    @raut.attach(path='/two')
    def route_two():
        return 'route /two'

    assert raut.solve(path='/', method='GET') == 'route /'
    assert raut.solve(path='/', method='OPTIONS') == 'route /'
    assert raut.solve(path='/one', method='GET') == 'route /one'
    assert raut.solve(path='/two', method='OPTIONS') == 'route /two'

    with should_raise(r.RautNotFound):
        raut.solve(path='/one', method='POST')

    with should_raise(r.RautMissingArgument):
        raut.solve(path='/one')


def test_skipping():
    raut = r.Raut()
    raut.add_processor(r.PathProcessor('path'))
    raut.add_processor(r.ProvideProcessor('params'))

    @raut.attach(path='/')
    def route_a(params):
        if params.get('name', 'a') == 'a':
            return 'route a /'
        else:
            raise r.RautSkip()

    @raut.attach(path='/')
    def route_b(params):
        if params.get('name') == 'b':
            return 'route b /'
        else:
            raise r.RautSkip()

    assert raut.solve(path='/', params={}) == 'route a /'
    assert raut.solve(path='/', params={'name': 'b'}) == 'route b /'

    with should_raise(r.RautNotFound):
        raut.solve(path='/', params={'name': 'c'})


def test_not_optional():
    raut = r.Raut()
    raut.add_processor(r.PathProcessor('path'))

    @raut.attach()
    def route_root():
        return 'route /'

    with should_raise(RuntimeError):
        raut.solve(path='/')


def test_path_optional():
    raut = r.Raut()
    raut.add_processor(r.PathProcessor('left'))
    raut.add_processor(r.PathProcessor('right', optional=True))

    @raut.attach(left='/a', right='/a')
    def route_one():
        return 'route one'

    @raut.attach(left='/a')
    def route_two():
        return 'route two'

    assert raut.solve(left='/a', right='/a') == 'route one'
    assert raut.solve(left='/a', right='/b') == 'route two'

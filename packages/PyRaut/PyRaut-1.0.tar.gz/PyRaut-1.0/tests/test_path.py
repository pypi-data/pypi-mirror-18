# -*- coding: utf-8 -*-

from pytest import raises

import pyraut as r


def test_various():
    p0 = r.Path('/welcome')
    p1 = r.Path('/blog/<name>')
    p2 = r.Path('/blog/<id|int>')
    p3 = r.Path('/blog/<name>/<action|str>')
    p4 = r.Path('/<page|greedy>')

    # test all the different converters
    assert p0('/welcome') == {}
    assert p1('/blog/my-article') == {'name': 'my-article'}
    assert p2('/blog/12') == {'id': 12}
    assert p3('/blog/my-article/edit') == {
        'name': 'my-article',
        'action': 'edit'
    }
    assert p4('/band/mötorhead') == {'page': 'band/mötorhead'}

    # matching p3, not p1
    assert p1('/blog/my-article/edit') is None

    # test the representation of a path
    assert repr(p1) == '<Path (^\/blog\/(?P<name>[^/]+)$)>'


def test_sorting():
    # build a simple path with a name
    p1 = r.Path('/blog/<name|str>')
    p2 = r.Path('/blog/<id|int>')
    p3 = r.Path('/blog/<name|str>/edit')
    p4 = r.Path('/<page|greedy>')
    p5 = r.Path('/')

    mapping = [p1, p2, p3, p4, p5]

    # make sure that that sorting works
    assert sorted(mapping) == [p5, p3, p2, p1, p4]

    # make sure the sorting with multiple scores work
    assert sorted([(p4, 0), (p5, 1)]) == [(p5, 1), (p4, 0)]
    assert sorted([(p5, 1), (p4, 0)]) == [(p5, 1), (p4, 0)]
    assert sorted([(p5, 1), (p4, 1)]) == [(p5, 1), (p4, 1)]
    assert sorted([(p5, 0), (p4, 1)]) == [(p5, 0), (p4, 1)]

    assert sorted([(True, 9, -9), p1, p5]) == [p5, p1, (True, 9, -9)]

    with raises(ValueError):
        p1 > 5

    # test path comparison
    assert p1 > p2
    assert p2 < p1
    assert p2 != p1
    assert p1 == r.Path('/blog/<name|str>')

    assert (True, 9, -9) > p1
    assert (False, 0, 0) < p1
    assert p1 < (True, 9, -9)
    assert p1 > (False, 0, 0)

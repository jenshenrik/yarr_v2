
from camera import Camera
import entity_factories

def test_apply():
    test_obj = Camera(5, 5, 5, 5, 15, 15)
    x = 7
    y = 8

    result_x, result_y = test_obj.apply(x, y)

    assert result_x == 2
    assert result_y == 3

def test_update():
    test_obj = Camera(5, 5, 5, 5, 15, 15)
    e = entity_factories.spawn_goblin()
    e.x = 10
    e.y = 11

    test_obj.update(e)

    assert test_obj.x == 8
    assert test_obj.y == 9

def test_update_upper_left_bound():
    test_obj = Camera(0, 0, 5, 5, 15, 15)
    e = entity_factories.spawn_goblin()
    e.x = 1
    e.y = 1

    test_obj.update(e)

    assert test_obj.x == 0
    assert test_obj.y == 0

def test_update_lower_left_bound():
    test_obj = Camera(0, 10, 5, 5, 15, 15)
    e = entity_factories.spawn_goblin()
    e.x = 1
    e.y = 14

    test_obj.update(e)

    assert test_obj.x == 0
    assert test_obj.y == 10

def test_update_upper_right_bound():
    test_obj = Camera(10, 0, 5, 5, 15, 15)
    e = entity_factories.spawn_goblin()
    e.x = 14
    e.y = 1

    test_obj.update(e)

    assert test_obj.x == 10
    assert test_obj.y == 0


def test_update_lower_right_bound():
    test_obj = Camera(10, 10, 5, 5, 15, 15)
    e = entity_factories.spawn_goblin()
    e.x = 14
    e.y = 14

    test_obj.update(e)

    assert test_obj.x == 10
    assert test_obj.y == 10

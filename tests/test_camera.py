import unittest

from camera import Camera
import entity_factories


class TestCamera(unittest.TestCase):

    def test_apply(self):
        test_obj = Camera(5, 5, 5, 5, 15, 15)
        x = 7
        y = 8

        result_x, result_y = test_obj.apply(x, y)

        self.assertEqual(result_x, 2)
        self.assertEqual(result_y, 3)

    def test_update(self):
        test_obj = Camera(5, 5, 5, 5, 15, 15)
        e = entity_factories.spawn_goblin()
        e.x = 10
        e.y = 11

        test_obj.update(e)

        self.assertEqual(test_obj.x, 8)
        self.assertEqual(test_obj.y, 9)

    def test_update_upper_left_bound(self):
        test_obj = Camera(0, 0, 5, 5, 15, 15)
        e = entity_factories.spawn_goblin()
        e.x = 1
        e.y = 1

        test_obj.update(e)

        self.assertEqual(test_obj.x, 0)
        self.assertEqual(test_obj.y, 0)

    def test_update_lower_left_bound(self):
        test_obj = Camera(0, 10, 5, 5, 15, 15)
        e = entity_factories.spawn_goblin()
        e.x = 1
        e.y = 14

        test_obj.update(e)

        self.assertEqual(test_obj.x, 0)
        self.assertEqual(test_obj.y, 10)

    def test_update_upper_right_bound(self):
        test_obj = Camera(10, 0, 5, 5, 15, 15)
        e = entity_factories.spawn_goblin()
        e.x = 14
        e.y = 1

        test_obj.update(e)

        self.assertEqual(test_obj.x, 10)
        self.assertEqual(test_obj.y, 0)

    def test_update_lower_right_bound(self):
        test_obj = Camera(10, 10, 5, 5, 15, 15)
        e = entity_factories.spawn_goblin()
        e.x = 14
        e.y = 14

        test_obj.update(e)

        self.assertEqual(test_obj.x, 10)
        self.assertEqual(test_obj.y, 10)

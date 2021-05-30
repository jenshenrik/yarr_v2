import unittest
from random import Random

import actions
import entity_factories
from components.consumable import HealingConsumable

class TestHealingConsumable(unittest.TestCase):

    def testSomething(self):
        # Given
        testObj = HealingConsumable(die=4, number_of_dice=1, bonus=2)
        consumer = entity_factories.spawn_goblin()
        consumer.fighter.take_damage(6)
        action = actions.ItemAction(entity=consumer, item=testObj)

        # When
        testObj.activate(action)

        # Then
        self.assertEqual(consumer.fighter.hp, 4)
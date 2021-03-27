from __future__ import annotations

import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING
from datetime import datetime

import tcod

import entity_factories
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


max_items_by_floor = [
    (1, 1),
    (4, 2),
]

max_monsters_by_floor = [
    (1, 2),
    (4, 3),
    (6, 5),
]

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.health_potion, 35)],
    2: [(entity_factories.confusion_scroll, 10)],
    4: [(entity_factories.lightning_scroll, 25), (entity_factories.sword, 5)],
    6: [(entity_factories.fireball_scroll, 25), (entity_factories.chain_mail, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.orc, 80)],
    3: [(entity_factories.troll, 15)],
    5: [(entity_factories.troll, 30)],
    7: [(entity_factories.troll, 60)],
}


def get_max_value_for_floor(
    weighted_changes_by_floor: List[Tuple[int, int]], floor: int
) -> int:
    current_value = 0

    for floor_minimum, value, in weighted_changes_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value


def get_entities_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
    number_of_entities: int,
    floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_values, k=number_of_entities
    )

    return chosen_entities


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int, node = None):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.node = node

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def place_entities(room: RectangularRoom, dungeon: GameMap, floor_number: int,) -> None:
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(max_monsters_by_floor, floor_number)
    )
    number_of_items = random.randint(
        0, get_max_value_for_floor(max_items_by_floor, floor_number)
    )

    monsters: List[Entity] = get_entities_at_random(
        enemy_chances, number_of_monsters, floor_number
    )
    items: List[Entity] = get_entities_at_random(
        item_chances, number_of_items, floor_number
    )

    for entity in monsters + items:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)


def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:  # 50% chance
        # Move horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    #rooms = naiveGenerate(dungeon, max_rooms, room_min_size, room_max_size)
    rooms = bspGenerate(dungeon, player, engine, max_rooms, room_min_size, room_max_size, 1)
    player.place(*rooms[0].center, dungeon)
    print_dungeon(dungeon)

    for room in rooms:
        place_entities(room, dungeon, engine.game_world.current_floor)

    last_room = rooms[len(rooms) - 1]
    dungeon.tiles[last_room.center] = tile_types.down_stairs
    dungeon.downstairs_location = last_room.center
    return dungeon

def print_dungeon(dungeon: GameMap):
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d-%H:%M:%S.map")
    #with open(filename, "w") as writer:
    for row in dungeon.tiles.T:
        for col in row:
            print(chr(col[2][0]),end="")
        print()
    print(filename)

def bspGenerate(dungeon: GameMap, player, engine: Engine, max_rooms: int, room_min_size: int, room_max_size: int, padding: int):
    bsp = tcod.bsp.BSP(x=0, y=0, width=dungeon.width-1, height=dungeon.height-1)
    bsp.split_recursive(
        depth=5,
        min_width=room_min_size + padding,
        min_height=room_min_size + padding,
        max_horizontal_ratio=1.1,
        max_vertical_ratio=1.1
    )
    rooms = []
    for node in bsp.post_order():
        if node.children:
            node1, node2 = node.children
            room1 = getRoomForNode(node1, rooms)
            room2 = getRoomForNode(node2, rooms)
            for x, y in tunnel_between(room1.center, room2.center):
                dungeon.tiles[x, y] = tile_types.floor

        else:
            new_room = createRoom(node, room_min_size, room_max_size)
            dungeon.tiles[new_room.inner] = tile_types.floor
            player.place(*new_room.center, dungeon)
            rooms.append(new_room)
    return rooms

def getRoomForNode(node, rooms):
    return next((room for room in rooms if room.node.x == node.x and room.node.y == node.y), None)

def createRoom(node, room_min_size, room_max_size):
    """Create a room inside a BSP tree node. Assumes node is large enough
    to fit minimum room size."""
    room_width = random.randint(room_min_size, min(node.width, room_max_size))
    room_height = random.randint(room_min_size, min(node.height, room_max_size))
    new_x = random.randint(node.x, node.x + (node.width - room_width))
    new_y = random.randint(node.y, node.y + (node.height - room_height))
    return RectangularRoom(new_x, new_y, room_width, room_height, node)

def naiveGenerate(dungeon: GameMap, max_rooms: int, room_min_size: int, room_max_size: int):
    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # the new room intersects another one and is thrown away

        # Dig out the room's inner area
        dungeon.tiles[new_room.inner] = tile_types.floor

        # Dig out a tunnel between this room and the previous one
        if len(rooms) > 1:
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        rooms.append(new_room)
    return rooms

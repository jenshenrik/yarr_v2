from typing import Tuple

class Camera():
    def __init__(self, x: int, y: int, width: int, height: int, map_width: int, map_height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, x: int, y: int) -> Tuple[int, int]:
        x = x - self.x
        y = y - self.y
        return (x, y)

    def update(self, entity) -> Tuple[int, int]:
        x = entity.x - int(self.width/2)
        y = entity.y - int(self.height/2)

        # Check if camera coordinates exceeds lower bound
        if x < 0:
            x = 0
        if y < 0:
           y = 0
        # Check if camera coordinates exceeds upper bound
        if (x + self.width) > self.map_width:
            x = self.map_width - self.width
        if (y + self.height) > self.map_height:
            y = self.map_height - self.height

        self.x, self.y = (x, y)
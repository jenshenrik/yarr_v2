from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING

import tcod
from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

import exceptions
from message_log import MessageLog
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(
        self, player: Actor, context: Context = None
    ):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.context = context

    # Used for pickling
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['context']
        return state

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def toggle_fullscreen(self) -> None:
        if self.context is not None:
            if not self.context.sdl_window_p:
                return
            fullscreen = tcod.lib.SDL_GetWindowFlags(self.context.sdl_window_p) & (
                    tcod.lib.SDL_WINDOW_FULLSCREEN | tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP
            )
            tcod.lib.SDL_SetWindowFullscreen(
                self.context.sdl_window_p,
                0 if fullscreen else tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP,
            )
        else:
            print("engine has no context, cannot toggle fullscreen")

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_functions.render_dungeon_level(
                console=console,
                dungeon_level=self.game_world.current_floor,
                location=(0, 47),
                )

        render_functions.render_names_at_mouse_location(
            console=console, x=21, y=44, engine=self
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)

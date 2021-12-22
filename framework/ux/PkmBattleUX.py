import abc
import time
from multiprocessing.connection import Listener
from typing import List

import arcade
import threading


from framework.util import non_blocking_lock

# Set constants for the screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
TITLE = "Pokemon Battle"
SPRITE_SCALING = 1.0


class ServerCom(threading.Thread):

    def __init__(self, window, authkey, address='localhost', port=6000):
        super().__init__()
        self.window = window
        self.authkey = authkey
        self.address = address
        self.port = port

    def run(self):
        while True:
            # family is deduced to be 'AF_INET'
            listener = Listener((self.address, self.port), authkey=self.authkey)
            conn = listener.accept()
            print('connection accepted from', listener.last_accepted)
            while True:
                msg = conn.recv()
                # do something with msg
                if msg == 'close':
                    conn.close()
                    break
                else:
                    print(msg)
                    self.window.push_command(msg)
            listener.close()


class AnimationEvent(abc.ABC):

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def run_step(self):
        pass

    @abc.abstractmethod
    def finished(self) -> bool:
        pass


class PauseEvent(AnimationEvent):

    def __init__(self, delta):
        self.delta = delta
        self.start_time = 0.0

    def start(self):
        self.start_time = time.time()

    def run_step(self):
        pass

    def finished(self) -> bool:
        return self.delta < time.time() - self.start_time


class SwitchEvent(AnimationEvent):

    def __init__(self, sprite1, sprite2, delta):
        self.sprite1 = sprite1
        self.sprite2 = sprite2
        self.origin1 = sprite1.center_x, sprite1.center_y
        self.origin2 = sprite2.center_x, sprite2.center_y
        self.target1 = sprite2.center_x, sprite2.center_y
        self.target2 = sprite1.center_x, sprite1.center_y
        self.delta = delta
        self.start_time = 0.0

    def start(self):
        self.start_time = time.time()

    def run_step(self):
        rate = (time.time() - self.start_time) / self.delta
        if rate > 0.975:
            rate = 1.0
        self.sprite1.center_x = (self.target1[0] - self.origin1[0]) * rate + self.origin1[0]
        self.sprite1.center_y = (self.target1[1] - self.origin1[1]) * rate + self.origin1[1]
        self.sprite2.center_x = (self.target2[0] - self.origin2[0]) * rate + self.origin2[0]
        self.sprite2.center_y = (self.target2[1] - self.origin2[1]) * rate + self.origin2[1]

    def finished(self) -> bool:
        return self.delta < time.time() - self.start_time


class AttackEvent(AnimationEvent):

    def __init__(self, sprite_pkm, sprite_attack, delta):
        self.sprite = sprite_attack
        self.origin = sprite_attack.center_x, sprite_attack.center_y
        self.target = sprite_pkm.center_x, sprite_pkm.center_y
        self.delta = delta
        self.start_time = 0.0

    def start(self):
        self.start_time = time.time()

    def run_step(self):
        rate = (time.time() - self.start_time) / self.delta
        if rate > 0.975:
            rate = 1.0
        self.sprite.center_x = (self.target[0] - self.origin[0]) * rate + self.origin[0]
        self.sprite.center_y = (self.target[1] - self.origin[1]) * rate + self.origin[1]

    def finished(self) -> bool:
        return self.delta < time.time() - self.start_time


class PkmBattleUX(arcade.Window):
    """ Main game class. """

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=TITLE):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.sprite_list = None

        # Set up the sprite info
        self.party1: List[arcade.Sprite] = []
        self.party2: List[arcade.Sprite] = []
        self.attack = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Text
        self.log = ''
        self.hp1 = 'HP: 300'
        self.hp2 = 'HP: 300'
        self.status1 = 'Stat: CLR'
        self.status2 = 'Stat: CLR'
        self.slp1 = 'Slp: 0'
        self.slp2 = 'Slp: 0'

        # Command Queue
        self.lock = threading.Lock()
        self.commands = []

        # Animation
        self.anim_events = []
        self.curr_event = PauseEvent(0.1)
        self.curr_event.start()

        # Set com channel
        self.server = ServerCom(self, authkey='VGC AI'.encode('utf-8'))

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.sprite_list = arcade.SpriteList()

        # start com
        self.server.setDaemon(True)
        self.server.start()

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Drawing the text
        arcade.draw_text(self.log, 10.0, 10.0, arcade.color.WHITE, 12, 180, 'left')

        arcade.draw_text(self.hp1, 10.0, 110.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.status1, 10.0, 90.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.slp1, 10.0, 70.0, arcade.color.WHITE, 12, 180, 'left')

        arcade.draw_text(self.hp2, 310.0, 210.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.status2, 310.0, 190.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.slp2, 310.0, 170.0, arcade.color.WHITE, 12, 180, 'left')

        # Draw all the sprites.
        self.sprite_list.draw()

    def on_update(self, delta_time):
        """ Game logic. """

        # resolve current animation
        if not self.curr_event.finished():
            self.curr_event.run_step()

        # fetch next animation event
        elif len(self.anim_events) > 0:
            self.curr_event = self.anim_events.pop(0)
            self.curr_event.start()

        # resolve pending commands
        else:
            self._resolve_next_command()

        # Move sprites
        self.sprite_list.update()

    def push_command(self, command):
        self.lock.acquire()
        self.commands.append(command)
        self.lock.release()

    def _resolve_next_command(self):
        if len(self.commands) > 0:
            with non_blocking_lock(self.lock):
                command = self.commands.pop(0)
                cmd_type = command[0]
                data = command[1]
                if cmd_type == 'init':
                    self._init_game(data)
                elif cmd_type == 'attack':
                    self._attack(data)
                elif cmd_type == 'switch':
                    self._switch(data)
                elif cmd_type == 'clear_attack':
                    self._clear_attack(data)

    def _init_game(self, data):
        self.party1.append(arcade.Sprite("sprites/01.png", SPRITE_SCALING))
        self.party1[0].center_x = 125
        self.party1[0].center_y = 100
        self.sprite_list.append(self.party1[0])

        self.party1.append(arcade.Sprite("sprites/01.png", SPRITE_SCALING))
        self.party1[1].center_x = 290
        self.party1[1].center_y = 60
        self.sprite_list.append(self.party1[1])

        self.party1.append(arcade.Sprite("sprites/01.png", SPRITE_SCALING))
        self.party1[2].center_x = 350
        self.party1[2].center_y = 60
        self.sprite_list.append(self.party1[2])

        self.hp1 = 'HP: 300'

        self.party2.append(arcade.Sprite("sprites/02.png", SPRITE_SCALING))
        self.party2[0].center_x = 275
        self.party2[0].center_y = 200
        self.sprite_list.append(self.party2[0])

        self.party2.append(arcade.Sprite("sprites/02.png", SPRITE_SCALING))
        self.party2[1].center_x = 50
        self.party2[1].center_y = 240
        self.sprite_list.append(self.party2[1])

        self.party2.append(arcade.Sprite("sprites/02.png", SPRITE_SCALING))
        self.party2[2].center_x = 110
        self.party2[2].center_y = 240
        self.sprite_list.append(self.party2[2])

        self.hp2 = 'HP: 300'

        self.log = 'Battle begins.'

    def _switch(self, data):
        old_active = self.party1[0]
        self.party1[0] = self.party1[1]
        self.party1[1] = old_active
        self.anim_events.append(SwitchEvent(self.party1[0], self.party1[1], 1.0))
        self.anim_events.append(PauseEvent(0.5))
        self.log = 'Switch.'

    def _attack(self, data):
        self.attack = arcade.Sprite("sprites/03.png", SPRITE_SCALING)
        self.attack.center_x = self.party1[0].center_x
        self.attack.center_y = self.party1[0].center_y
        self.sprite_list.append(self.attack)
        self.anim_events.append(AttackEvent(self.party2[0], self.attack, 1.0))
        self.commands.insert(0, ('clear_attack', []))
        self.log = 'Attack.'

    def _clear_attack(self, data):
        self.sprite_list.remove(self.attack)
        self.anim_events.append(PauseEvent(0.5))


def main():
    """ Test """
    window = PkmBattleUX()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

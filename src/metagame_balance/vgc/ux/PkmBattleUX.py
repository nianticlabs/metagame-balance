import abc
import threading
import time
from multiprocessing.connection import Listener
from typing import List, Tuple

import arcade

from metagame_balance.vgc.datatypes.Types import PkmType, PkmStat
# Set constants for the screen size
from metagame_balance.vgc.util.Networking import non_blocking_lock

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
                try:
                    msg = conn.recv()
                except EOFError:
                    conn.close()
                    break
                # do something with msg
                if msg == 'close':
                    conn.close()
                    break
                else:
                    # print(msg)
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

        # Background image will be stored in this variable
        self.background = None

        # Variables that will hold sprite lists
        self.sprite_list = None

        # Set up the sprite info
        self.party: Tuple[List[arcade.Sprite], List[arcade.Sprite]] = ([], [])
        self.attack = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Text
        self.log = ''
        self.hp = ['HP: 300', 'HP: 300']
        self.moves = 'Moves:'
        self.a = ['300', '300', '300', '300']
        self.atk = ['Atk: 0', 'Atk: 0']
        self.dfs = ['Def: 0', 'Def: 0']
        self.spd = ['Spd: 0', 'Spd: 0']

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

        # Load the background image. Do this in the setup so we don't keep reloading it all the time.
        self.background = arcade.load_texture("sprites/background.png")

        # Sprite lists
        self.sprite_list = arcade.SpriteList()

        # start com
        self.server.setDaemon(True)
        self.server.start()

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Drawing the text
        arcade.draw_text(self.log, 10.0, 10.0, arcade.color.WHITE, 12, 180, 'left')

        arcade.draw_text(self.spd[0], 130.0, 200.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.dfs[0], 130.0, 180.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.atk[0], 130.0, 160.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.hp[0], 130.0, 140.0, arcade.color.WHITE, 12, 180, 'left')

        arcade.draw_text(self.moves, 10.0, 40.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.a[0], 80.0, 40.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.a[1], 120.0, 40.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.a[2], 160.0, 40.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.a[3], 200.0, 40.0, arcade.color.WHITE, 12, 180, 'left')

        arcade.draw_text(self.spd[1], 210.0, 200.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.dfs[1], 210.0, 180.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.atk[1], 210.0, 160.0, arcade.color.WHITE, 12, 180, 'left')
        arcade.draw_text(self.hp[1], 210.0, 140.0, arcade.color.WHITE, 12, 180, 'left')

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
                    self._clear_attack()
                elif cmd_type == 'event':
                    self._event(data)

    def _init_game(self, data):
        while len(self.sprite_list) > 0:
            self.sprite_list.pop()
        del self.party[0][:]
        del self.party[1][:]

        type0_0 = data[0]
        n = 1
        self.party[0].append(arcade.Sprite(f"sprites/pkm/{type0_0}_{n}.png", SPRITE_SCALING))
        self.party[0][0].center_x = 90
        self.party[0][0].center_y = 135
        self.sprite_list.append(self.party[0][0])

        type0_1 = data[1]
        n = 2 if type0_0 == type0_1 else 1
        self.party[0].append(arcade.Sprite(f"sprites/pkm/{type0_1}_{n}.png", SPRITE_SCALING))
        self.party[0][1].center_x = 50
        self.party[0][1].center_y = 260
        self.sprite_list.append(self.party[0][1])

        type0_2 = data[2]
        n = 3 if type0_2 == type0_1 and type0_2 == type0_0 else (2 if type0_2 == type0_1 or type0_2 == type0_0 else 1)
        self.party[0].append(arcade.Sprite(f"sprites/pkm/{type0_2}_{n}.png", SPRITE_SCALING))
        self.party[0][2].center_x = 110
        self.party[0][2].center_y = 260
        self.sprite_list.append(self.party[0][2])

        hp0 = data[3]
        self.hp[0] = f'HP: {hp0}'

        self.a[0] = str(data[4])
        self.a[1] = str(data[5])
        self.a[2] = str(data[6])
        self.a[3] = str(data[7])

        type1_0 = data[8]
        n = 1
        self.party[1].append(arcade.Sprite(f"sprites/pkm/{type1_0}_{n}.png", SPRITE_SCALING))
        self.party[1][0].center_x = 310
        self.party[1][0].center_y = 135
        self.sprite_list.append(self.party[1][0])

        type1_1 = data[9]
        n = 2 if type1_0 == type1_1 else 1
        self.party[1].append(arcade.Sprite(f"sprites/pkm/{type1_1}_{n}.png", SPRITE_SCALING))
        self.party[1][1].center_x = 290
        self.party[1][1].center_y = 260
        self.sprite_list.append(self.party[1][1])

        type1_2 = data[10]
        n = 3 if type1_2 == type1_1 and type1_2 == type1_0 else (2 if type1_2 == type1_1 or type1_2 == type1_0 else 1)
        self.party[1].append(arcade.Sprite(f"sprites/pkm/{type1_2}_{n}.png", SPRITE_SCALING))
        self.party[1][2].center_x = 350
        self.party[1][2].center_y = 260
        self.sprite_list.append(self.party[1][2])

        hp1 = data[11]
        self.hp[1] = f'HP: {hp1}'

        self.log = 'Battle begins.'

    def _switch(self, data):
        team = data[0]
        party = data[1] + 1
        hp = data[2]
        old_active = self.party[team][0]
        self.party[team][0] = self.party[team][party]
        self.party[team][party] = old_active
        self.anim_events.append(SwitchEvent(self.party[team][0], self.party[team][party], 1.0))
        self.anim_events.append(PauseEvent(0.5))
        self.hp[team] = f'HP: {hp}'
        self.atk[team] = f'Atk: 0'
        self.dfs[team] = f'Def: 0'
        if team == 0:
            moves = data[3], data[4], data[5], data[6]
            self.a = [str(moves[0]), str(moves[1]), str(moves[2]), str(moves[3])]
        self.log = f'Trainer {team} switches to party {party}.'

    def _attack(self, data):
        team = data[0]
        move = data[1]
        dmg = data[2]
        self.attack = arcade.Sprite(f"sprites/move/{move}.png", SPRITE_SCALING)
        self.attack.center_x = self.party[team][0].center_x
        self.attack.center_y = self.party[team][0].center_y
        self.sprite_list.append(self.attack)
        if dmg:
            opp_team = 0 if team else 1
            self.anim_events.append(AttackEvent(self.party[opp_team][0], self.attack, 1.0))
        else:
            self.anim_events.append(PauseEvent(1.0))
        self.commands.insert(0, ('clear_attack', []))
        self.log = f'Trainer {team} attacks with move {PkmType(move).name}.'

    def _clear_attack(self):
        self.sprite_list.remove(self.attack)
        self.anim_events.append(PauseEvent(0.5))

    def _event(self, data):
        evt = data[0]
        team = data[1]
        if evt == 'hp':
            stat = data[2]
            self.hp[team] = f'HP: {stat}'
            self.log = f'Active {team} HP becomes {stat}.'
        elif evt == PkmStat.ATTACK.name:
            stat = data[2]
            self.atk[team] = f'Atk: {stat}'
            self.log = f'Active {team} ATK status becomes {stat} turns.'
        elif evt == PkmStat.DEFENSE.name:
            stat = data[2]
            self.dfs[team] = f'Atk: {stat}'
            self.log = f'Active {team} DEF status becomes {stat} turns.'
        elif evt == PkmStat.SPEED.name:
            stat = data[2]
            self.spd[team] = f'Spd: {stat}'
            self.log = f'Active {team} SPD status becomes {stat} turns.'
        elif evt == 'log':
            self.log = data[1]
        self.anim_events.append(PauseEvent(0.5))


def main():
    """ Test """
    window = PkmBattleUX()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

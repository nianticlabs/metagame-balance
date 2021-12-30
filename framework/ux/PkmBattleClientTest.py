
import time

from multiprocessing.connection import Client

from framework.behaviour.BattlePolicies import RandomBattlePolicy
from framework.process.BattleEngine import PkmBattleEnv
from framework.util.PkmTeamGenerators import RandomGenerator

address = ('localhost', 6000)
conn = Client(address, authkey='VGC AI'.encode('utf-8'))
conn.send(('init', [1, 4, 1, 250, 150, 100, 100, 150, 2, 5, 2, 300]))
conn.send('close')
conn.close()

time.sleep(1)

address = ('localhost', 6000)
conn = Client(address, authkey='VGC AI'.encode('utf-8'))
conn.send(('switch', [0, 1, 100, 150, 150, 150, 150]))
conn.send(('switch', [1, 1, 150]))
conn.send(('attack', [0, 3, False]))
conn.send(('attack', [1, 3, True]))
conn.send(('event', ['hp', 0, 100]))
conn.send(('event', ['atk', 0, 2]))
conn.send('close')
conn.close()

time.sleep(1)


gen = RandomGenerator()
full_team0 = gen.get_team()
full_team1 = gen.get_team()
conn = Client(address, authkey='VGC AI'.encode('utf-8'))
env = PkmBattleEnv((full_team0.get_battle_team([0, 1, 2]), full_team0.get_battle_team([0, 1, 2])), debug=True, conn=conn)
env.reset()
t = False
a0 = RandomBattlePolicy()
a1 = RandomBattlePolicy()
ep = 0
n_battles = 1
while ep < n_battles:
    s = env.reset()
    v = env.game_state_view
    env.render(mode='ux')
    ep += 1
    while not t:
        o0 = s[0] if a0.requires_encode() else v[0]
        o1 = s[1] if a1.requires_encode() else v[1]
        a = [a0.get_action(o0), a1.get_action(o1)]
        s, _, t, v = env.step(a)
        env.render(mode='ux')
    t = False
env.close()

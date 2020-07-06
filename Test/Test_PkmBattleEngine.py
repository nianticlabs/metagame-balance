from Engine.PkmBattleEngine import PkmBattleEngine
from Engine.PkmTeamGenerator import RandomGenerator
from Player.HeuristicBattleAgent import HeuristicBattleAgent
from Player.GUIBattleAgent import GUIBattleAgent
from Player.RandomBattleAgent import RandomBattleAgent
from Util.Recorder import Recorder


def main():
    env = PkmBattleEngine(debug=True)
    env.set_team_generator(RandomGenerator())
    env.reset()  # set correct team size for get_n_party
    t = False
    a0 = GUIBattleAgent(env.trainer_view[0].get_n_party())
    a1 = RandomBattleAgent()
    r = Recorder(name="random_agent")
    ep = 0
    n_battles = 3
    while ep < n_battles:
        s = env.reset()
        v = env.trainer_view
        env.render()
        ep += 1
        while not t:
            a = [a0.get_action(v[0]), a1.get_action(v[1])]
            r.record((s[0], a[0], ep))
            s, _, t, v = env.step(a)
            env.render()
        t = False
    r.save()
    a0.close()


if __name__ == '__main__':
    main()

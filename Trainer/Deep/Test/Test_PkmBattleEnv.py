from Engine.PkmBattleEngine import PkmBattleEngine
from Engine.PkmTeamGenerator import RandomGenerator
from Player.HeuristicAgent import HeuristicAgent
from Player.RandomAgent import RandomAgent


def main():
    env = PkmBattleEngine(debug=True)
    env.set_team_generator(RandomGenerator())
    s = env.reset()
    v = env.trainer_view
    env.render()
    t = False
    a0 = RandomAgent()
    a1 = HeuristicAgent()
    while not t:
        s, _, t, v = env.step([a0.get_action(s[0]), a1.get_action(v[1])])
        env.render()


if __name__ == '__main__':
    main()

from typing import List, Tuple

from Engine.PkmBaseStructures import PkmTeam
from Engine.PkmBattleEngine import PkmBattleEngine
from Trainer.Tabular.Abstract.BattleAgent import BattleAgent
from Util.Recorder import Recorder


class Competitor:

    def __init__(self, team: PkmTeam, battle_agent: BattleAgent):
        self.team: PkmTeam = team
        self.battleAgent: BattleAgent = battle_agent


class Match:

    def __init__(self, n_games: int, competitors: Tuple[Competitor, Competitor], name="match", debug=False,
                 render=False, record=False):
        self.n_games: int = n_games
        self.competitors: Tuple[Competitor, Competitor] = competitors
        self.debug: bool = debug
        self.name: str = name
        self.wins: Tuple[int, int] = 0, 0
        self.render: bool = render
        self.record: bool = record

    def run(self):
        c0 = self.competitors[0]
        c1 = self.competitors[1]
        env = PkmBattleEngine(debug=self.debug, teams=[c0.team, c1.team])
        t = False
        a0 = c0.battleAgent
        a1 = c1.battleAgent
        r = Recorder(name="random_agent")
        game = 0
        while game < self.n_games:
            s = env.reset()
            v = env.trainer_view
            if self.render:
                env.render()
            game += 1
            while not t:
                a = [a0.get_action(v[0]), a1.get_action(v[1])]
                if self.record:
                    r.record((s[0], a[0], game))
                s, _, t, v = env.step(a)
                if self.render:
                    env.render()
            t = False
            self.wins[env.winner] += 1
        if self.record:
            r.save()
        a0.close()

    def records(self) -> Tuple[int, int]:
        """
        Get match records.

        :return: player 0 winds, player 1 wins
        """
        return self.wins

from multiprocessing.connection import Listener

from metagame_balance.vgc.competition import Competitor


class RemoteCompetitorManager:

    def __init__(self, competitor: Competitor, authkey, address='localhost', port=5000):
        self.competitor = competitor
        self.authkey = authkey
        self.address = address
        self.port = port
        self.conn = None

    def run(self):
        while True:
            # family is deduced to be 'AF_INET'
            listener = Listener((self.address, self.port), authkey=self.authkey)
            print('Waiting...')
            self.conn = listener.accept()
            print('connection accepted from', listener.last_accepted)
            while True:
                try:
                    msg = self.conn.recv()
                except EOFError:
                    self.conn.close()
                    break
                # do something with msg
                self.__run_method(msg)
            listener.close()

    def __run_method(self, msg):
        if msg[0] == 'BattlePolicy':
            if msg[1] == 'get_action':
                self.conn.send(self.competitor.battle_policy.get_action(msg[2]))
            elif msg[1] == 'requires_encode':
                self.conn.send(self.competitor.battle_policy.requires_encode())
            elif msg[1] == 'close':
                self.competitor.battle_policy.close()
        elif msg[0] == 'TeamSelectionPolicy':
            if msg[1] == 'get_action':
                self.conn.send(self.competitor.team_selection_policy.get_action(msg[2]))
            elif msg[1] == 'requires_encode':
                self.conn.send(self.competitor.team_selection_policy.requires_encode())
            elif msg[1] == 'close':
                self.competitor.team_selection_policy.close()
        elif msg[0] == 'TeamBuildPolicy':
            if msg[1] == 'get_action':
                self.conn.send(self.competitor.team_build_policy.get_action(msg[2]))
            elif msg[1] == 'requires_encode':
                self.conn.send(self.competitor.team_build_policy.requires_encode())
            elif msg[1] == 'close':
                self.competitor.team_build_policy.close()
        elif msg[0] == 'TeamPredictor':
            if msg[1] == 'get_action':
                self.conn.send(self.competitor.team_predictor.get_action(msg[2]))
            elif msg[1] == 'requires_encode':
                self.conn.send(self.competitor.team_predictor.requires_encode())
            elif msg[1] == 'close':
                self.competitor.team_predictor.close()
        elif msg[0] == 'BalancePolicy':
            if msg[1] == 'get_action':
                self.conn.send(self.competitor.balance_policy.get_action(msg[2]))
            elif msg[1] == 'requires_encode':
                self.conn.send(self.competitor.balance_policy.requires_encode())
            elif msg[1] == 'close':
                self.competitor.balance_policy.close()
        elif msg[0] == 'name':
            self.conn.send(self.competitor.name)

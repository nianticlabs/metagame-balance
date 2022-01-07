from multiprocessing.connection import Listener

from framework.competition.Competition import Competitor


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
            elif msg[2] == 'close':
                self.competitor.battle_policy.close()
        elif msg[0] == 'SelectorPolicy':
            if msg[1] == 'get_action':
                self.conn.send(self.competitor.selector_policy.get_action(msg[2]))
            elif msg[1] == 'requires_encode':
                self.conn.send(self.competitor.selector_policy.requires_encode())
            elif msg[2] == 'close':
                self.competitor.selector_policy.close()
        elif msg[0] == 'TeamBuilderPolicy':
            if msg[1] == 'get_action':
                self.conn.send(self.competitor.team_builder_policy.get_action(msg[2]))
            elif msg[1] == 'requires_encode':
                self.conn.send(self.competitor.team_builder_policy.requires_encode())
            elif msg[2] == 'close':
                self.competitor.team_builder_policy.close()
        elif msg[0] == 'TeamPredictor':
            if msg[1] == 'get_action':
                self.conn.send(self.competitor.team_prediction_policy.get_action(msg[2]))
            elif msg[1] == 'requires_encode':
                self.conn.send(self.competitor.team_prediction_policy.requires_encode())
            elif msg[2] == 'close':
                self.competitor.team_prediction_policy.close()
        elif msg[0] == 'DataAggregator':
            if msg[1] == 'get_action':
                self.conn.send(self.competitor.data_aggregator_policy.get_action(msg[2]))
            elif msg[1] == 'requires_encode':
                self.conn.send(self.competitor.data_aggregator_policy.requires_encode())
            elif msg[2] == 'close':
                self.competitor.data_aggregator_policy.close()
        elif msg[0] == 'TeamValuator':
            if msg[1] == 'get_action':
                self.conn.send(self.competitor.team_valuator_policy.get_action(msg[2]))
            elif msg[1] == 'requires_encode':
                self.conn.send(self.competitor.team_valuator_policy.requires_encode())
            elif msg[2] == 'close':
                self.competitor.team_valuator_policy.close()
        elif msg[0] == 'BalancePolicy':
            if msg[1] == 'get_action':
                self.conn.send(self.competitor.balance_policy.get_action(msg[2]))
            elif msg[1] == 'requires_encode':
                self.conn.send(self.competitor.balance_policy.requires_encode())
            elif msg[2] == 'close':
                self.competitor.balance_policy.close()
        elif msg[0] == 'name':
            self.conn.send(self.competitor.name)

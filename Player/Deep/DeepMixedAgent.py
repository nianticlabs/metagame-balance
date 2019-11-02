from Util.Projection import *
from Trainer.Tabular.Abstract.Agent import *
import tensorflow as tf


class DeepMixedAgent(Agent):

    def __init__(self, n_actions, model_path):
        with open(model_path + '/checkpoint') as f:
            checkpoint = f.readline().split()[1].split('"')[1]
        self.graph = tf.Graph()
        self.sess = tf.Session(graph=self.graph)
        self.n_actions = n_actions
        with self.graph.as_default():
            saver = tf.train.import_meta_graph(model_path + '/' + checkpoint + ".meta")
            saver.restore(self.sess, tf.train.latest_checkpoint(model_path))
            self.policy = self.graph.get_tensor_by_name('global_0/global_0_policy:0')
            self.input_v = self.graph.get_tensor_by_name('global_0/global_0_input:0')

    def check_state(self, s):
        pass

    def update(self, s0, s1, a, r, t):
        pass

    def get_action(self, s):
        """

        :param s: state
        :return: action
        """
        return np.random.choice(self.n_actions, p=self.sess.run([self.policy], feed_dict={self.input_v: [s]})[0][0])

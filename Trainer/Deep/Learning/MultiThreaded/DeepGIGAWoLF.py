from Util.Projection import projection
from threading import Thread
import numpy as np
import copy
import tensorflow as tf
import tensorflow.contrib.slim as slim
import os
from random import random


class DeepGIGAWoLF:
    class Trainer:

        def __init__(self, env, optimizer, g_net, t_net, e_rate, pi_l_rate, y, sess, leader, name='player',
                     global_id=0):
            self.name = name
            self.g_net = g_net
            self.t_net = t_net
            self.pi_l_rate = pi_l_rate
            self.y = y
            self.e_rate = e_rate
            self.n_actions = env.action_space.n
            self.net = DeepGIGAWoLF.Network(optimizer, env, name='player_' + self.name, global_id=global_id)
            print('player_' + self.name)
            self.pi_t = None
            self.pi_slow_t = None
            self.q_t = None
            self.pi_t_batch = []
            self.pi_slow_t_batch = []
            self.q_t_batch = []
            self.s_batch = []
            self.sess = sess
            self.leader = leader

        def get_action(self, s):
            """

            :return: action
            """
            # choose random action with probability e_rate
            if random() < self.e_rate:
                return int(random() * self.n_actions)
            pi, q = self.sess.run([self.net.policy, self.net.out_q], feed_dict={self.net.in_state: [s]})
            pi, self.q_t = pi[0], q[0]
            # if self.name == '0_0':
            #     print(' PI ', pi, 'Q', self.q_t)
            return np.random.choice(self.n_actions, p=pi)

        def compute_pi_q(self, s, a, r, t):
            # load pi and q from target
            feed_dict = {self.t_net.in_state: [s]}
            pi_t, pi_slow_t, max_q = self.sess.run([self.t_net.policy, self.t_net.policy_slow, self.t_net.max_q],
                                                   feed_dict=feed_dict)
            self.pi_t, self.pi_slow_t, max_q = pi_t[0], pi_slow_t[0], max_q[0]
            self.s_batch += [s]
            # compute target Q-values
            self.q_t[a] = r + (1 - t) * self.y * max_q
            self.q_t_batch += [self.q_t]
            # compute target policy
            avg_pi = [0] * self.n_actions  # average policy
            for a in range(self.n_actions):
                avg_pi[a] = self.pi_t[a] + self.pi_l_rate * self.q_t[a]
            # project this strategy
            avg_pi = projection(avg_pi, 0)
            # Update the agent's 'z' distribution, using the step size and 'possible' rewards
            z = [0] * self.n_actions
            for a in range(self.n_actions):
                z[a] = self.pi_slow_t[a] + self.pi_l_rate * self.q_t[a] / 3
            # project this strategy
            z = projection(z, 0)
            # Calculate delta using sum of squared differences
            num = np.sqrt(sum((np.array(z) - np.array(self.pi_slow_t)) ** 2))
            den = np.sqrt(sum((np.array(z) - np.array(avg_pi)) ** 2))
            # delta learning rate
            if den == 0:
                d_l_rate = 1
            else:
                d_l_rate = min(1, num / den)
            # do an update of the agent's strategy
            for a in range(self.n_actions):
                self.pi_slow_t[a] = z[a]
                self.pi_t[a] = avg_pi[a] + d_l_rate * (z[a] - avg_pi[a])
            # if self.name == '0_0':
            #     print(' target PI ', self.pi_t, ' <- ', pi_t[0])
            #     print(' target PI slow', self.pi_slow_t, ' <- ', pi_slow_t[0])
            self.pi_t_batch += [self.pi_t]
            self.pi_slow_t_batch += [self.pi_slow_t]

        def accumulate_grads_on_global(self):
            """
            Accumulate gradients from local network to global online network.
            """
            feed_dict = {self.net.target_q: self.q_t_batch, self.net.target_pi: self.pi_t_batch,
                         self.net.target_pi_slow: self.pi_slow_t_batch, self.net.in_state: self.s_batch}
            self.sess.run(self.net.apply_gradients, feed_dict=feed_dict)
            # empty batches
            self.pi_t_batch = []
            self.pi_slow_t_batch = []
            self.q_t_batch = []
            self.s_batch = []

        def update_target_network(self):
            """
            Copy weights from global online network to global target network.
            """
            self.sess.run(self.net.global_to_target)

        def update_from_global(self):
            """
            Copy weights from global online network to local network.
            """
            self.sess.run(self.net.global_to_local)

    class Simulation(Thread):

        def __init__(self, env, optimizer, g_net, pi_l_rate, y, e_rate, tau, n_eps, n_steps, n_players, sess, g_id,
                     name='gameplay'):
            super().__init__()
            self.game = env
            self.pi_l_rate = pi_l_rate
            self.tau = tau
            self.player = []
            self.name = name
            p = 0
            while p < n_players:
                self.player.append(
                    DeepGIGAWoLF.Trainer(env, optimizer, g_net[p]['global'], g_net[p]['target'], e_rate, pi_l_rate, y,
                                         sess,
                                         g_id == 0, name=self.name + '_' + str(p), global_id=p))
                p += 1
            self.n_eps = n_eps
            self.n_steps = n_steps
            self.n_players = n_players
            self.sess = sess

        def run(self):
            with self.sess.graph.as_default():
                a = [None] * self.n_players
                ep = 0
                step = 0
                while ep < self.n_eps:
                    ep += 1
                    if self.name == '0':
                        print('EP', ep)
                    # sample initial game state
                    s1 = self.game.reset()
                    while True:
                        # update local networks from global network by copying the weights
                        for p in self.player:
                            p.update_from_global()
                        step += 1
                        # get joint action from players (state s1)
                        for i, p in enumerate(self.player):
                            a[i] = p.get_action(s1[i])
                        # move world, and sample state and reward
                        s0 = s1
                        s1, r, t, _ = self.game.step(tuple(a))
                        # for each player
                        for i, p in enumerate(self.player):
                            p.compute_pi_q(s0[i], a[i], r[i], t)
                            # at every period steps
                            if step % self.tau == 0:
                                # apply local gradients in global net
                                p.accumulate_grads_on_global()
                                if p.leader:
                                    # update target networks weights
                                    p.update_target_network()
                        if step % self.n_steps == 0:
                            break

    @staticmethod
    def train(env, g_l_rate, concurrent_games, pi_l_rate, y, tau, n_eps, n_steps, e_rate, n_players, model_path,
              env_name):
        with tf.Session() as sess:
            with tf.get_default_graph().as_default():
                coord = tf.train.Coordinator()
                optimizer = tf.train.AdamOptimizer(learning_rate=g_l_rate)
                g_net = []
                p = 0
                while p < n_players:
                    g_net += [{'global': DeepGIGAWoLF.Network(optimizer, env, name='global_' + str(p), global_id=p),
                               'target': DeepGIGAWoLF.Network(optimizer, env, name='target_' + str(p), global_id=p)}]
                    print('global_' + str(p))
                    print('target_' + str(p))
                    p += 1
                game_pool = []
                g = 0
                while g < concurrent_games:
                    game_pool.append(
                        DeepGIGAWoLF.Simulation(copy.deepcopy(env), optimizer, g_net, pi_l_rate, y, e_rate, tau, n_eps,
                                                n_steps, n_players, sess, g, name=str(g)))
                    g += 1
                # tf.summary.FileWriter('./Graph', sess.graph)
                sess.run(tf.global_variables_initializer())
                for env in game_pool:
                    env.start()
                coord.join(game_pool)
                # save model
                if not os.path.exists(model_path):
                    os.makedirs(model_path)
                saver = tf.train.Saver()
                saver.save(sess, model_path + '/model.cpkb')

    class Network:
        def __init__(self, optimizer, env, name='default', global_id=0):
            with tf.variable_scope(name):
                self.in_state = tf.placeholder(tf.float32, shape=(None, env.observation_space.n), name=name+'_input')
                self.hidden_l = slim.fully_connected(self.in_state, 150,
                                                     weights_initializer=tf.contrib.layers.xavier_initializer(),
                                                     activation_fn=tf.nn.elu)
                self.hidden_l = slim.fully_connected(self.in_state, 150,
                                                     weights_initializer=tf.contrib.layers.xavier_initializer(),
                                                     activation_fn=tf.nn.elu)
                self.hidden_l = slim.fully_connected(self.in_state, 150,
                                                     weights_initializer=tf.contrib.layers.xavier_initializer(),
                                                     activation_fn=tf.nn.elu)
                self.out_q = slim.fully_connected(self.hidden_l, env.action_space.n, activation_fn=None,
                                                  weights_initializer=tf.contrib.layers.xavier_initializer(),
                                                  biases_initializer=None)
                self.out_pi = slim.fully_connected(self.hidden_l, env.action_space.n, activation_fn=None,
                                                   weights_initializer=tf.contrib.layers.xavier_initializer(),
                                                   biases_initializer=None)
                self.out_pi_slow = slim.fully_connected(self.hidden_l, env.action_space.n, activation_fn=None,
                                                        weights_initializer=tf.contrib.layers.xavier_initializer(),
                                                        biases_initializer=None)
                self.max_q = tf.reduce_max(self.out_q, 1)
                self.policy = tf.nn.softmax(self.out_pi, name=name+'_policy')
                self.policy_slow = tf.nn.softmax(self.out_pi_slow)
            self.target_q = tf.placeholder(tf.float32, shape=(None, env.action_space.n))
            self.loss_q = tf.square(self.target_q - self.out_q)
            self.target_pi = tf.placeholder(tf.float32, shape=(None, env.action_space.n))
            self.target_pi_slow = tf.placeholder(tf.float32, shape=(None, env.action_space.n))
            self.loss_pi = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.out_pi, labels=self.target_pi))
            self.loss_pi_slow = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.out_pi_slow, labels=self.target_pi_slow))
            self.loss = tf.reduce_mean(self.loss_q + self.loss_pi + self.loss_pi_slow)
            self.gradients, _ = tf.clip_by_global_norm(
                tf.gradients(self.loss, tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, name)), 40.0)
            self.apply_gradients = optimizer.apply_gradients(
                zip(self.gradients, tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'global_' + str(global_id))))

            def copy_network(origin_scope, destiny_scope):
                origin_w = slim.get_trainable_variables(origin_scope)
                destiny_w = slim.get_trainable_variables(destiny_scope)
                copy_op = {}
                for o_w, d_w in zip(origin_w, destiny_w):
                    copy_op[o_w.name] = d_w.assign(o_w)
                return copy_op

            self.global_to_local = copy_network('global_' + str(global_id), name)
            self.global_to_target = copy_network('global_' + str(global_id), 'target_' + str(global_id))

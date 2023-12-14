import math
import numpy
import tensorflow as tf
from game import *
from typing import List
import copy


# I'm using some code from the original pseudocode AlphaZero here
class AlphaZeroConfig(object):
    def __init__(self):
        self.num_actors = 5000

        self.num_sampling_moves = 30
        self.max_moves = 512
        self.num_simulations = 800
        # Root prior exploration noise.
        self.root_dirichlet_alpha = 0.3
        self.root_exploration_fraction = 0.25
        # UCB formula
        self.pb_c_base = 19652
        self.pb_c_init = 1.25
        # Training
        self.training_steps = int(700e3)
        self.checkpoint_interval = int(1e3)
        self.window_size = int(1e6)
        self.batch_size = 4096
        self.weight_decay = 1e-4
        self.momentum = 0.9
        self.learning_rate_schedule = {
            0: 2e-1,
            100e3: 2e-2,
            300e3: 2e-3,
            500e3: 2e-4
        }


class Node(object):

    def __init__(self, prior: float):
        self.visit_count = 0
        self.to_play = -1
        self.prior = prior
        self.value_sum = 0
        self.children = {}

    def expanded(self):
        return len(self.children) > 0

    def value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count


class ReplayBuffer(object):

    def __init__(self, config: AlphaZeroConfig):
        self.window_size = config.window_size
        self.batch_size = config.batch_size
        self.buffer = []

    def save_game(self, gametosave):
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)
        self.buffer.append(gametosave)

    def sample_batch(self):
        # Sample uniformly across positions.
        move_sum = float(sum(g.history for g in self.buffer))
        games = numpy.random.choice(
            self.buffer,
            size=self.batch_size,
            p=[g.history / move_sum for g in self.buffer])
        game_pos = [(g, numpy.random.randint(g.history)) for g in games]
        return [(g.make_image(i), g.make_target(i)) for (g, i) in game_pos]


class Network(object):
    # unfinished
    def inference(self, image):
        return -1, {}  # Value, Policy

    def get_weights(self):
        # Returns the weights of this network.
        return []


class SharedStorage(object):
    def __init__(self):
        self._networks = {}

    def latest_network(self) -> Network:
        if self._networks:
            return self._networks[max(iter(self._networks.keys()))]
        else:
            return Network()  # policy -> uniform, value -> 0.5

    def save_network(self, step: int, network: Network):
        self._networks[step] = network


def alphazero(config: AlphaZeroConfig):
    storage = SharedStorage()
    replay_buffer = ReplayBuffer(config)

    for i in range(config.num_actors):
        run_selfplay(config, storage, replay_buffer)

    train_network(config, storage, replay_buffer)

    return storage.latest_network()


def run_selfplay(config: AlphaZeroConfig, storage: SharedStorage,
                 replay_buffer: ReplayBuffer):
    while True:
        network = storage.latest_network()
        game = play_game(config, network)
        replay_buffer.save_game(game)


def play_game(config: AlphaZeroConfig, network: Network):
    # todo: alter the original store_search_statistics from here
    gametoplay = Game()
    while not gametoplay.is_terminal() and gametoplay.history < config.max_moves:
        action, root = run_mcts(config, gametoplay, network)
        gametoplay.take_action(action)
        gametoplay.store_search_statistics(root)
    return gametoplay


def run_mcts(config: AlphaZeroConfig, game: Game, network: Network):
    root = Node(0)
    evaluate(root, game, network)
    add_exploration_noise(config, root)

    for _ in range(config.num_simulations):
        node = root
        scratch_game = copy.deepcopy(game)
        search_path = [node]

        while node.expanded():
            action, node = select_child(config, node)
            scratch_game.take_action(action)
            search_path.append(node)

        value = evaluate(node, scratch_game, network)
        backpropagate(search_path, value, (scratch_game.history % 2))
    return select_action(config, game, root), root


def select_action(config: AlphaZeroConfig, game: Game, root: Node):
    visit_counts = [(child.visit_count, action)
                    for action, child in iter(root.children.items())]
    if game.history < config.num_sampling_moves:
        _, action = 0, 0
    else:
        _, action = max(visit_counts)
    return action


def select_child(config: AlphaZeroConfig, node: Node):
    _, action, child = max((ucb_score(config, node, child), action, child)
                           for action, child in (node.children.items()))
    return action, child


def ucb_score(config: AlphaZeroConfig, parent: Node, child: Node):
    pb_c = math.log((parent.visit_count + config.pb_c_base + 1) /
                    config.pb_c_base) + config.pb_c_init
    pb_c *= math.sqrt(parent.visit_count) / (child.visit_count + 1)

    prior_score = pb_c * child.prior
    value_score = child.value()
    return prior_score + value_score


def evaluate(node: Node, game: Game, network: Network):
    # todo: alter from the old make_image
    value, policy_logits = network.inference(game.make_image(-1))

    # Expand the node.
    node.to_play = game.history % 2
    policy = {a: math.exp(policy_logits[a]) for a in game.get_possible_actions()}
    policy_sum = sum(iter(policy.values()))
    for action, p in enumerate(policy.items()):
        node.children[action] = Node(p / policy_sum)
    return value


def backpropagate(search_path: List[Node], value: float, to_play):
    for node in search_path:
        node.value_sum += value if node.to_play == to_play else (1 - value)
        node.visit_count += 1


def add_exploration_noise(config: AlphaZeroConfig, node: Node):
    actions = node.children.keys()
    noise = numpy.random.gamma(config.root_dirichlet_alpha, 1, len(actions))
    frac = config.root_exploration_fraction
    for a, n in zip(actions, noise):
        node.children[a].prior = node.children[a].prior * (1 - frac) + n * frac


def train_network(config: AlphaZeroConfig, storage: SharedStorage,
                  replay_buffer: ReplayBuffer):
    network = Network()
    optimizer = tf.keras.optimizers.SGD(config.learning_rate_schedule,
                                           config.momentum)
    for i in range(config.training_steps):
        if i % config.checkpoint_interval == 0:
            storage.save_network(i, network)
        batch = replay_buffer.sample_batch()
        update_weights(optimizer, network, batch, config.weight_decay)
    storage.save_network(config.training_steps, network)


def update_weights(optimizer: tf.compat.v1.train.Optimizer, network: Network, batch,
                   weight_decay: float):
    loss = 0
    for image, (target_value, target_policy) in batch:
        value, policy_logits = network.inference(image)
        loss += (
                tf.keras.losses.mean_squared_error(value, target_value) +
                tf.nn.softmax_cross_entropy_with_logits(
                    logits=policy_logits, labels=target_policy))

    for weights in network.get_weights():
        loss += weight_decay * tf.nn.l2_loss(weights)

    optimizer.minimize(loss)

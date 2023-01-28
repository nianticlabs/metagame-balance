# Game Meta Balance

This repository is the official implementation of the paper titled "Bilevel Entropy based Mechanism Design for Balancing Meta in Video Games".

Brief Description: Our paper formulates the game meta balance problem as mechanism design problem. We set the objective of the designer as maximizing the entropy of a (given) player's mixed strategy (over the strategy space) at nash equilibrium. Such a formulation, paired with state-of-the-art solvers leads to a scalable algorithm as shown in our paper. The repository provides an official implementation of our problem formulation. The respository also serves as a benchmark for game balance on three domains (source code adapted from respective gits)
1. [Rock Paper Scissor Fire Water (RPSFW)](https://en.wikipedia.org/wiki/Rock_paper_scissors#:~:text=Rock%20beats%20scissors%2C%20paper%20beats,time%20for%20fire%20and%20water)
2. [Workshop Workfare (WW)](https://github.com/Danielhp95/GGJ-2020-cool-game) (also referred as coolgame in code)
3. [Pokemon Video Game Championship (VGC)](https://gitlab.com/DracoStriker/pokemon-vgc-engine)

If you find our work useful in your research please consider citing our paper:

```
@inproceedings{game-balance-2023-bigmb,
  title     = {Bilevel Entropy based Mechanism Design for Balancing Meta in Video Games},
  author    = {Pendurkar, Sumedh and
               Chow, Chris and
               Jie, Luo and
               Sharon, Guni
               },
  booktitle = {The 22nd International Conference on Autonomous Agents and Multiagent Systems (AAMAS)},
  month = {May},
year = {2023}
}
```


# Installation
```commandline
poetry install
```

if you are in a pip-only environment, then
```commandline
pip install -r requirements.txt
```


If `elo` and `gym` have difficulty installing. get into the virtualenv that poetry creates
and `pip install` the particular versions needed.

# Running Experiments
```commandline
poetry run python src/metagame_balance/main.py
```

## coolgame experiments
```commandline
usage: main [-h] [--n_epochs N_EPOCHS] [--snapshot_gameplay_policy_epochs SNAPSHOT_GAMEPLAY_POLICY_EPOCHS] [--snapshot_game_state_epochs SNAPSHOT_GAME_STATE_EPOCHS] [--reg REG] [--baseline]
            {rpsfw,vgc,coolgame} ...

positional arguments:
  {rpsfw,vgc,coolgame}  domain

optional arguments:
  -h, --help            show this help message and exit
  --n_epochs N_EPOCHS
  --snapshot_gameplay_policy_epochs SNAPSHOT_GAMEPLAY_POLICY_EPOCHS
  --snapshot_game_state_epochs SNAPSHOT_GAME_STATE_EPOCHS
  --reg REG
  --baseline

usage: main coolgame [-h] [--cmaes_init_var CMAES_INIT_VAR] [--entropy_eval_epochs ENTROPY_EVAL_EPOCHS]

optional arguments:
  -h, --help            show this help message and exit
  --cmaes_init_var CMAES_INIT_VAR
  --entropy_eval_epochs ENTROPY_EVAL_EPOCHS
```

Using poetry:
```commandline
poetry run main coolgame
```

or, using python directly
```commandline
python ./src/metagame_balance/main.py coolgame
```

(keeping in mind you can use the commandline args above.)

# License
Copyright © Niantic, Inc. 2023. Patent Pending.
All rights reserved.
Please see the [license file](LICENSE) for terms.

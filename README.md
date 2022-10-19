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
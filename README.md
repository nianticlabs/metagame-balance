# Pokémon VGC AI Framework

[[_TOC_]]

## Installation

1. Install Python 3.6.8 or higher.

2. Clone this project.

3. Install the requirements.txt

4. Use you preferred Interactive Development Environment.

Alternatively you may use the Dockerfile to create a ready to run container. All dependencies are installed in the venv
vgc-env and project is found in the /vgc-ai folder. User root has vgc as password. A SSH server is installed and run on
the container boot.

## Source Code

The `/vgc` module is the core implementation of the VGC AI Framework.

In the `/test` folder is contained some unit tests from the core framework modules.

## Tutorial

In this section we present a set of introductory tutorials.

### Set a Pokemon Battle in the Pokemon Battle Env (OpenAI Gym)

Set Pokemon battles is just to set a simple OpenAI Gym environment loop. The `PkmBattleEnv` is parametrized
by two `PkmTeam`, each will be piloted by its respective `BattlePolicy` agent.

```python
team0, team1 = PkmTeam(), PkmTeam()
agent0, agent1 = RandomBattlePolicy(), RandomBattlePolicy()
env = PkmBattleEnv((team0, team1))  # set new environment with teams
n_battles = 3  # total number of battles
t = False
battle = 0
while battle < n_battles:
    s = env.reset()
    while not t:  # True when all pkms of one of the two PkmTeam faint
        a = [agent0.get_action(s[0]), agent1.get_action(s[1])]
        s, _, t, _ = env.step(a)  # for inference we don't need reward
        env.render()
    t = False
    battle += 1
print(env.winner)  # tuple with the victories of agent0 and agent1
```

`s` is a duple with the game state view encoding for each agent. `r` is a duple with the reward for each agent.

To create custom `PkmTeam` you can just input an array of `Pkm`.

```python
team = PkmTeam([Pkm(), Pkm(), Pkm()])  # up to three!
```

The `PkmTeam` represents a in battle team, which is a subset of a `PkmFullTeam`. The later is used for team building 
settings. You can obtain a battle team from a full team by providing the team indexes.

```python
full_team = FullPkmTeam([Pkm(), Pkm(), Pkm(), Pkm(), Pkm(), Pkm()])
team = full_team.get_battle_team([1, 4, 5])
```

### Create a Pokemon Roster and Meta

A `PkmRoster` represents the entirety of unit selection for a team build competition. It is defined as 
`set[PkmTemplate]`. A `PkmTemplate` represents a Pokemon species. It defines the legal stats combinations and moveset
for that Pokemon species. To create a roster you jsut need to convert a list of `PkmTemplate`.

```python
roster = set([PkmTemplate(), PkmTemplate(), PkmTemplate()])
```

To get a `Pkm` instance from a `PkmTemplate` you just need to provide the moves indexes.

```python
templ = PkmTemplate()
pkm = templ.gen_pkm([1, 2, 5, 3])  # 4 max!
```

To create a meta is as simple as initializing.

```python
meta = StandardMetaData()
```

### Create My VGC AI Agent

To implement a VGC competitor agent you need to create an implementation of the class `Competitor` and override its
multiple methods that return the various types of behaviours that will be called during an ecosystem simulation.
Example:

```python
class Competitor(ABC):
    
    def __init__(self):
        self.my_battle_policy = RandomBattlePolicy()
        self.my_team_build_policy = MyVGCBuildPolicy()
        
    @property
    def battle_policy(self) -> BattlePolicy:
        return self.my_battle_policy

    @property
    def team_build_policy(self) -> TeamBuildPolicy:
        return self.my_team_build_policy

    @property
    def name(self) -> str:
        return "My VGC AI agent"
```

The battle policy must inherit from `BattlePolicy` and the team build policy must inherit from `TeamBuildPolicy`.

### Set Competition Managers and a Tree Championship

A `CompetitorManager` binds and manages a `Competitor` with its current `PkmFullTeam` and respective performance (ELO 
rating). These can be used in the context of a `TreeChampionship` or any full Ecosystem track. 

```python
roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
competitors = [ExampleCompetitor('Player ' + str(i)) for i in range(N_PLAYERS)]
championship = TreeChampionship(roster, debug=True)
for competitor in competitors:
    championship.register(CompetitorManager(competitor))  # add competitor to the tournament and set his team
championship.new_tournament()  # create a tournament tree
winner = championship.run()  # run tournament
print(winner.competitor.name + " wins the tournament!")  # fetch winner
```

The `TeamBuildPolicy` from the `Competitor` is called to request the agent to choose its team.

### Run Your own Full Competitions

The `BattleEcosystem` allows to run a Battle Competition Track. You just need to instantiate a `PkmRoster`, `MetaData`,
and register the competitors wrapped under their `CompetitorManager`. You then must set how many epochs you want to run.

```python
roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
meta_data = MetaData()
le = BattleEcosystem(meta_data, debug=True)
epochs = 10
for i in range(N_PLAYERS):
    cm = CompetitorManager(ExampleCompetitor("Player %d" % i))
    cm.team = RandomTeamFromRoster(roster).get_team()
    le.register(cm)
le.run(epochs)
```

For the `ChampionshipEcosystem` the process is similar. The difference resides in you must set both the number of 
championship epochs and how many battle epochs run inside each championship epoch.

```python
roster = RandomPkmRosterGenerator(None, n_moves_pkm=10, roster_size=100).gen_roster()
meta_data = StandardMetaData()
ce = ChampionshipEcosystem(roster, meta_data, debug=True)
battle_epochs = 10
championship_epochs = 10
for i in range(N_PLAYERS):
    cm = CompetitorManager(ExampleCompetitor("Player %d" % i))
    ce.register(cm)
ce.run(n_epochs=battle_epochs, n_league_epochs=championship_epochs)
```

### How to use View Objects

TODO

### Visualize Battles

See and use examples provided in `/vgc/ux`.

### More

In the `/example` folder it can be found multiple examples for how to use the framework, to train or test isolated agents
or behaviours or run full ecosystems with independent processes controlling each agent.

In the `/organization` folder it can be found the multiple entry points for the main ecosystem layers in the VGC AI
Framework.

## Documentation

The full documentation from API, Framework architecture to the Competition Tracks and
Rules can be found in the [Wiki](https://gitlab.com/DracoStriker/pokemon-vgc-engine/-/wikis/home).

## Citation

Please cite this work if used.

```
@INPROCEEDINGS{9618985,

  author={Reis, Simão and Reis, Luís Paulo and Lau, Nuno},

  booktitle={2021 IEEE Conference on Games (CoG)}, 

  title={VGC AI Competition - A New Model of Meta-Game Balance AI Competition}, 

  year={2021},

  volume={},

  number={},

  pages={01-08},

  doi={10.1109/CoG52621.2021.9618985}}
```

## Todo

* Add Baseline Agents
* Improve Framework Performance
* Improve the Battle Championship class.

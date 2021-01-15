from Framework.Competition.CompetitionObjects import Competitor
from simple_plugin_loader import Loader

# initialize the loader
loader = Loader()

# load your plugins
plugins = loader.load_plugins('C:\\Users\\Simon\\PycharmProjects\\pokemon-vgc-engine\\Competitor', Competitor, recursive=True, verbose=True)

print(plugins)
c = plugins['competitor1']()
bp = c.get_battle_policy()
print(bp.get_action(None))
c = plugins['competitor2']()
bp = c.get_battle_policy()
print(bp.get_action(None))

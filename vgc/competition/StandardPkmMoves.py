from vgc.datatypes.Objects import PkmMove
from vgc.datatypes.Types import PkmType, PkmStatus, WeatherCondition, PkmStat, PkmEntryHazard

# Struggle
Struggle = PkmMove(max_pp=0, name="Struggle")

# Normal Moves
Recover = PkmMove(0., 1., 5, PkmType.NORMAL, "Recover", recover=80., target=0, prob=1.)
DoubleEdge = PkmMove(120., 1., 10, PkmType.NORMAL, "Double-Edge", recover=-40., prob=1.)
ExtremeSpeed = PkmMove(80., 1., 10, PkmType.NORMAL, "Extreme Speed", priority=True)
Slam = PkmMove(80., .75, 20, PkmType.NORMAL, "Slam", status=PkmStatus.PARALYZED, prob=1 / 3)
Tackle = PkmMove(40., 1., 20, PkmType.NORMAL, "Tackle")

# Fire Moves
SunnyDay = PkmMove(0., 1., 5, PkmType.FIRE, "Sunny Day", weather=WeatherCondition.SUNNY, prob=1.)
FireBlast = PkmMove(110., .85, 5, PkmType.FIRE, "Fire Blast", status=PkmStatus.BURNED, prob=.3)
Flamethrower = PkmMove(90., 1., 15, PkmType.FIRE, "Flamethrower", status=PkmStatus.BURNED, prob=.1)
Ember = PkmMove(40., 1., 20, PkmType.FIRE, "Ember", status=PkmStatus.BURNED, prob=.1)

# Water Moves
RainDance = PkmMove(0., 1., 5, PkmType.WATER, "Rain Dance", weather=WeatherCondition.RAIN, prob=1.)
HydroPump = PkmMove(110., .8, 5, PkmType.WATER, "Hydro Pump")
AquaJet = PkmMove(40., 1., 20, PkmType.WATER, "Aqua Jet", priority=True)
BubbleBeam = PkmMove(65., 1., 20, PkmType.WATER, "Bubble Beam", stat=PkmStat.SPEED, stage=-1, prob=.1)

# Electric Moves
ThunderWave = PkmMove(0., 1., 20, PkmType.ELECTRIC, "Thunder Wave", status=PkmStatus.PARALYZED, prob=1.)
Thunder = PkmMove(110., .7, 10, PkmType.ELECTRIC, "Thunder", status=PkmStatus.PARALYZED, prob=.3)
Thunderbolt = PkmMove(90., 1., 15, PkmType.ELECTRIC, "Thunderbolt", status=PkmStatus.PARALYZED, prob=.1)
ThunderShock = PkmMove(40., 1., 20, PkmType.ELECTRIC, "Thunder Shock", status=PkmStatus.PARALYZED, prob=.1)

# Grass Moves
Spore = PkmMove(0., 1., 5, PkmType.GRASS, "Spore", status=PkmStatus.SLEEP, prob=1)
GigaDrain = PkmMove(75., 1., 15, PkmType.GRASS, "Giga Drain", recover=30., prob=1.)
RazorLeaf = PkmMove(55., .95, 20, PkmType.GRASS, "Razor Leaf")
EnergyBall = PkmMove(90., 1., 10, PkmType.GRASS, "Energy Ball", stat=PkmStat.DEFENSE, stage=-1, prob=.1)

# Ice Moves
Hail = PkmMove(0., 1., 5, PkmType.ICE, "Hail", weather=WeatherCondition.HAIL)
Blizzard = PkmMove(110., .7, 5, PkmType.ICE, "Blizzard", status=PkmStatus.FROZEN, prob=.1)
IceBeam = PkmMove(90., 1., 10, PkmType.ICE, "Ice Beam", status=PkmStatus.FROZEN, prob=.1)
IceShard = PkmMove(40., 1., 20, PkmType.ICE, "Ice Shard", priority=True)

# Fighting Moves
BulkUp = PkmMove(0., 1., 5, PkmType.FIGHT, "Bulk Up", stat=PkmStat.ATTACK, stage=2, target=0, prob=1.)
MachPunch = PkmMove(40., 1., 20, PkmType.FIGHT, "Mach Punch", priority=True)
CloseCombat = PkmMove(120., 1., 5, PkmType.FIGHT, "Close Combat", stat=PkmStat.DEFENSE, stage=-2, target=0, prob=1.)
DynamicPunch = PkmMove(100., .5, 5, PkmType.FIGHT, "Dynamic Punch", status=PkmStatus.CONFUSED, prob=1.)

# Poison Moves
Poison = PkmMove(0., 1., 5, PkmType.POISON, "Poison", status=PkmStatus.POISONED, prob=1.)
GunkShot = PkmMove(110., .8, 5, PkmType.POISON, "Gunk Shot", status=PkmStatus.POISONED, prob=.3)
PoisonJab = PkmMove(80., 1., 5, PkmType.POISON, "Poison Jab", status=PkmStatus.POISONED, prob=.3)
AcidSpray = PkmMove(40., 1., 20, PkmType.POISON, "Acid Spray", stat=PkmStat.DEFENSE, stage=-2, prob=1.)

# Ground Moves
Spikes = PkmMove(0., 1., 20, PkmType.GROUND, "Spikes", hazard=PkmEntryHazard.SPIKES, prob=1.)
Earthquake = PkmMove(100., 1., 10, PkmType.GROUND, "Earthquake")
MudShot = PkmMove(55., .95, 15, PkmType.GROUND, "Mud Shot", stat=PkmStat.SPEED, stage=-1, prob=1.)
EarthPower = PkmMove(90., 1., 10, PkmType.GROUND, "Earth Power", stat=PkmStat.DEFENSE, stage=-1, prob=.1)

# Flying Moves
Roost = PkmMove(0., 1., 5, PkmType.FLYING, "Roost", recover=80., target=0, prob=1.)
Chatter = PkmMove(65., 1., 20, PkmType.FLYING, "Chatter", status=PkmStatus.CONFUSED, prob=1.)
Hurricane = PkmMove(110., .7, 10, PkmType.FLYING, "Hurricane", status=PkmStatus.CONFUSED, prob=.3)
WingAttack = PkmMove(60., 1., 20, PkmType.FLYING, "Wing Attack")

# Psychic Moves
CalmMind = PkmMove(0., 1., 5, PkmType.PSYCHIC, "Calm Mind", stat=PkmStat.DEFENSE, stage=2, target=0, prob=1.)
Psychic = PkmMove(90., 1., 10, PkmType.PSYCHIC, "Psychic", stat=PkmStat.DEFENSE, stage=-1, prob=.1)
PsychoBoost = PkmMove(140., .9, 5, PkmType.PSYCHIC, "Psycho Boost", stat=PkmStat.DEFENSE, stage=-2, target=0, prob=.1)
Psybeam = PkmMove(65., 1., 10, PkmType.PSYCHIC, "Psybeam", status=PkmStatus.CONFUSED, prob=.1)

# Bug Moves
StringShot = PkmMove(0., 1., 5, PkmType.BUG, "String Shot", stat=PkmStat.SPEED, stage=-1)
BugBuzz = PkmMove(90., 1., 10, PkmType.BUG, "Bug Buzz", stat=PkmStat.DEFENSE, stage=-1, prob=.1)
LeechLife = PkmMove(80., 1., 10, PkmType.BUG, "Leech Life", recover=40., prob=1.)

# Rock Moves
Sandstorm = PkmMove(0., 1., 5, PkmType.ROCK, "Sandstorm", weather=WeatherCondition.SANDSTORM, prob=1.)
PowerGem = PkmMove(80., 1., 20, PkmType.ROCK, "Power Gem")
RockTomb = PkmMove(60., .95, 15, PkmType.ROCK, "Rock Tomb", stat=PkmStat.SPEED, stage=-1, prob=1.)
StoneEdge = PkmMove(100., .8, 5, PkmType.ROCK, "Stone Edge")

# Ghost Moves
NightShade = PkmMove(0., 1., 10, PkmType.GHOST, "Night Shade", fixed_damage=40., prob=1.)
ShadowBall = PkmMove(80., 1., 15, PkmType.GHOST, "Shadow Ball", stat=PkmStat.DEFENSE, stage=-1, prob=.2)
ShadowSneak = PkmMove(40., 1., 20, PkmType.GHOST, "Mach Punch", priority=True)

# Dragon Moves
DragonRage = PkmMove(0., 1., 10, PkmType.DRAGON, "Dragon Rage", fixed_damage=40., prob=1.)
DracoMeteor = PkmMove(130., .9, 5, PkmType.DRAGON, "Draco Meteor", stat=PkmStat.ATTACK, stage=-2, target=0, prob=1.)
DragonBreath = PkmMove(60., 1., 20, PkmType.DRAGON, "Dragon Breath", status=PkmStatus.PARALYZED, prob=1.)
Outrage = PkmMove(120., 1., 10, PkmType.DRAGON, "Outrage", status=PkmStatus.CONFUSED, target=0, prob=1.)

# Dark Moves
NastyPlot = PkmMove(0., 1., 5, PkmType.DARK, "Nasty Plot", stat=PkmStat.ATTACK, stage=2, target=0, prob=1.)
Crunch = PkmMove(80., 1., 15, PkmType.DARK, "Crunch", stat=PkmStat.DEFENSE, stage=-1, prob=.2)
Snarl = PkmMove(55., .95, 15, PkmType.DARK, "Snarl", stat=PkmStat.ATTACK, stage=-1, prob=1.)

# Steel Moves
IronDefense = PkmMove(0., 1., 5, PkmType.STEEL, "Iron Defense", stat=PkmStat.DEFENSE, stage=2, target=0, prob=1.)
IronTail = PkmMove(100., .75, 15, PkmType.STEEL, "Iron Tail", stat=PkmStat.DEFENSE, stage=-1, prob=.3)
SteelWing = PkmMove(70., .9, 20, PkmType.STEEL, "Steel Wing", stat=PkmStat.DEFENSE, stage=2, target=0, prob=.1)
BulletPunch = PkmMove(40., 1., 20, PkmType.STEEL, "Bullet Punch", priority=True)

# Fairy Moves
SweetKiss = PkmMove(0., .75, 5, PkmType.FAIRY, "Sweet Kiss", status=PkmStatus.CONFUSED, prob=1.)
PlayRough = PkmMove(90., .9, 10, PkmType.FAIRY, "Play Rough", stat=PkmStat.ATTACK, stage=-1, prob=.1)
Moonblast = PkmMove(95., 1., 15, PkmType.FAIRY, "Moonblast", stat=PkmStat.ATTACK, stage=-1, prob=.3)

# Standard Move Pool
STANDARD_MOVE_ROSTER = [Recover, DoubleEdge, ExtremeSpeed, Slam, Tackle, SunnyDay, FireBlast, Flamethrower,
                        Ember, RainDance, HydroPump, AquaJet, BubbleBeam, ThunderWave, Thunder, Thunderbolt,
                        ThunderShock, Spore, GigaDrain, RazorLeaf, EnergyBall, Hail, Blizzard, IceBeam,
                        IceShard, BulkUp, MachPunch, CloseCombat, DynamicPunch, Poison, GunkShot, PoisonJab,
                        AcidSpray, Spikes, EarthPower, Earthquake, MudShot, Roost, Chatter, Hurricane,
                        WingAttack, CalmMind, Psychic, PsychoBoost, Psybeam, StringShot, BugBuzz, LeechLife,
                        Sandstorm, PowerGem, RockTomb, StoneEdge, NightShade, ShadowBall, ShadowSneak, DragonRage,
                        DracoMeteor, DragonBreath, Outrage, NastyPlot, Crunch, Snarl, IronDefense, IronTail, SteelWing,
                        BulletPunch, SweetKiss, PlayRough, Moonblast]

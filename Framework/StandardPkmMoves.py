from Engine.DataObjects import PkmMove, PkmType, PkmStatus
from Engine.DataTypes import WeatherCondition, PkmStat, PkmEntryHazard
import random

# Struggle
Struggle = PkmMove(max_pp=0, name="Struggle")

# Normal Moves
Recover = PkmMove(0., 1., 5, PkmType.NORMAL, "Recover", lambda v: v.set_recover(80.))
DoubleEdge = PkmMove(120., 1., 10, PkmType.NORMAL, "Double-Edge", lambda v: v.set_recover(-40.))
ExtremeSpeed = PkmMove(80., 1., 10, PkmType.NORMAL, "Extreme Speed", priority=True)
Slam = PkmMove(80., .75, 20, PkmType.NORMAL, "Slam",
               lambda v: v.set_status(PkmStatus.PARALYZED, 1) if random.random() < 1 / 3 else None)
Tackle = PkmMove(40., 1., 20, PkmType.NORMAL, "Tackle")

# Fire Moves
SunnyDay = PkmMove(0., 1., 5, PkmType.FIRE, "Sunny Day", lambda v: v.set_weather(WeatherCondition.SUNNY))
FireBlast = PkmMove(110., .85, 5, PkmType.FIRE, "Fire Blast",
                    lambda v: v.set_status(PkmStatus.BURNED, 1) if random.random() < .3 else None)
Flamethrower = PkmMove(90., 1., 15, PkmType.FIRE, "Flamethrower",
                       lambda v: v.set_status(PkmStatus.BURNED, 1) if random.random() < .1 else None)
Ember = PkmMove(40., 1., 20, PkmType.FIRE, "Ember",
                lambda v: v.set_status(PkmStatus.BURNED, 1) if random.random() < .1 else None)

# Water Moves
RainDance = PkmMove(0., 1., 5, PkmType.WATER, "Rain Dance", lambda v: v.set_weather(WeatherCondition.RAIN))
HydroPump = PkmMove(110., .8, 5, PkmType.WATER, "Hydro Pump")
AquaJet = PkmMove(40., 1., 20, PkmType.WATER, "Aqua Jet", priority=True)
BubbleBeam = PkmMove(65., 1., 20, PkmType.WATER, "Bubble Beam",
                     lambda v: v.set_stage(PkmStat.SPEED, -1, 1) if random.random() < .1 else None)

# Electric Moves
ThunderWave = PkmMove(0., 1., 20, PkmType.ELECTRIC, "Thunder Wave", lambda v: v.set_status(PkmStatus.PARALYZED, 1))
Thunder = PkmMove(110., .7, 10, PkmType.ELECTRIC, "Thunder",
                  lambda v: v.set_status(PkmStatus.PARALYZED, 1) if random.random() < .3 else None)
Thunderbolt = PkmMove(90., 1., 15, PkmType.ELECTRIC, "Thunderbolt",
                      lambda v: v.set_status(PkmStatus.PARALYZED, 1) if random.random() < .1 else None)
ThunderShock = PkmMove(40., 1., 20, PkmType.ELECTRIC, "Thunder Shock",
                       lambda v: v.set_status(PkmStatus.PARALYZED, 1) if random.random() < .1 else None)

# Grass Moves
Spore = PkmMove(0., 1., 5, PkmType.GRASS, "Spore", lambda v: v.set_status(PkmStatus.SLEEP, 1))
GigaDrain = PkmMove(75., 1., 15, PkmType.GRASS, "Giga Drain", lambda v: v.set_recover(30.))
RazorLeaf = PkmMove(55., 95., 20, PkmType.GRASS, "Razor Leaf")
EnergyBall = PkmMove(90., 1., 10, PkmType.GRASS, "Energy Ball",
                     lambda v: v.set_stage(PkmStat.DEFENSE, -1, 1) if random.random() < .1 else None)

# Ice Moves
Hail = PkmMove(0., 1., 5, PkmType.ICE, "Hail", lambda v: v.set_weather(WeatherCondition.HAIL))
Blizzard = PkmMove(110., .7, 5, PkmType.ICE, "Blizzard",
                   lambda v: v.set_status(PkmStatus.FROZEN, 1) if random.random() < .1 else None)
IceBeam = PkmMove(90., 1., 10, PkmType.ICE, "Ice Beam",
                  lambda v: v.set_status(PkmStatus.FROZEN, 1) if random.random() < .1 else None)
IceShard = PkmMove(40., 1., 20, PkmType.ICE, "Ice Shard", priority=True)

# Fighting Moves
BulkUp = PkmMove(0., 1., 5, PkmType.FIGHT, "Bulk Up", lambda v: v.set_stage(PkmStat.ATTACK, 2, 0))
MachPunch = PkmMove(40., 1., 20, PkmType.FIGHT, "Mach Punch", priority=True)
CloseCombat = PkmMove(120., 1., 5, PkmType.FIGHT, "Close Combat", lambda v: v.set_stage(PkmStat.DEFENSE, -2, 0))
DynamicPunch = PkmMove(100., .5, 5, PkmType.FIGHT, "Dynamic Punch", lambda v: v.set_status(PkmStatus.CONFUSED, 1))

# Poison Moves
Poison = PkmMove(0., 1., 5, PkmType.POISON, "Poison", lambda v: v.set_status(PkmStatus.POISONED, 1))
GunkShot = PkmMove(110., .8, 5, PkmType.POISON, "Gunk Shot",
                   lambda v: v.set_status(PkmStatus.POISONED, 1) if random.random() < .3 else None)
PoisonJab = PkmMove(80., 1., 5, PkmType.POISON, "Poison Jab",
                    lambda v: v.set_status(PkmStatus.POISONED, 1) if random.random() < .3 else None)
AcidSpray = PkmMove(40., 1., 20, PkmType.POISON, "Acid Spray ", lambda v: v.set_stage(PkmStat.DEFENSE, -2, 1))

# Ground Moves
Spikes = PkmMove(0., 1., 20, PkmType.GROUND, "Spikes", lambda v: v.set_entry_hazard(PkmEntryHazard.SPIKES, 1))
Earthquake = PkmMove(100., 1., 10, PkmType.GROUND, "Earthquake")
MudShot = PkmMove(55., 95., 15, PkmType.GROUND, "Mud Shot", lambda v: v.set_stage(PkmStat.SPEED, -1, 1))
EarthPower = PkmMove(90., 1., 10, PkmType.GROUND, "Earth Power",
                     lambda v: v.set_stage(PkmStat.DEFENSE, -1, 1) if random.random() < .1 else None)

# Flying Moves
Roost = PkmMove(0., 1., 5, PkmType.FLYING, "Roost", lambda v: v.set_recover(80.))
Chatter = PkmMove(65., 1., 20, PkmType.FLYING, "Chatter", lambda v: v.set_status(PkmStatus.CONFUSED, 1))
Hurricane = PkmMove(110., .7, 10, PkmType.FLYING, "Hurricane",
                    lambda v: v.set_status(PkmStatus.CONFUSED, 1) if random.random() < .3 else None)
WingAttack = PkmMove(60., 100., 20, PkmType.FLYING, "WingAttack")

# Psychic Moves
CalmMind = PkmMove(0., 1., 5, PkmType.PSYCHIC, "Calm Mind", lambda v: v.set_stage(PkmStat.DEFENSE, 2, 0))
Psychic = PkmMove(90., 1., 10, PkmType.PSYCHIC, "Psychic",
                  lambda v: v.set_stage(PkmStat.DEFENSE, -1, 1) if random.random() < .1 else None)
PsychoBoost = PkmMove(140., .9, 5, PkmType.PSYCHIC, "Psycho Boost", lambda v: v.set_stage(PkmStat.DEFENSE, -2, 0))
Psybeam = PkmMove(65., 1., 10, PkmType.PSYCHIC, "Psybeam",
                  lambda v: v.set_status(PkmStatus.CONFUSED, 1) if random.random() < .1 else None)

# Bug Moves
StringShot = PkmMove(0., 1., 5, PkmType.BUG, "String Shot", lambda v: v.set_stage(PkmStat.SPEED, -1, 1))
BugBuzz = PkmMove(90., 1., 10, PkmType.BUG, "Bug Buzz",
                  lambda v: v.set_stage(PkmStat.DEFENSE, -1, 1) if random.random() < .1 else None)
LeechLife = PkmMove(80., 1., 10, PkmType.BUG, "Leech Life", lambda v: v.set_recover(40.))
SilverWind = PkmMove(60., 1., 5, PkmType.BUG, "Silver Wind", lambda v: (v.set_stage(PkmStat.ATTACK, 1, 0),
                                                                        v.set_stage(PkmStat.DEFENSE, 1, 0),
                                                                        v.set_stage(PkmStat.SPEED, 1,
                                                                                    0)) if random.random() < .1 else None)

# Rock Moves
Sandstorm = PkmMove(0., 1., 5, PkmType.ROCK, "Sandstorm", lambda v: v.set_weather(WeatherCondition.SANDSTORM))
PowerGem = PkmMove(80., 1., 20, PkmType.ROCK, "Power Gem")
RockTomb = PkmMove(60., .95, 15, PkmType.ROCK, "Rock Tomb", lambda v: v.set_stage(PkmStat.SPEED, -1, 1))
StoneEdge = PkmMove(100., .8, 5, PkmType.ROCK, "Stone Edge")

# Ghost Moves
NightShade = PkmMove(0., 1., 10, PkmType.GHOST, "Night Shade", lambda v: v.set_fixed_damage(100.))
ShadowBall = PkmMove(80., 1., 15, PkmType.GHOST, "Shadow Ball",
                     lambda v: v.set_stage(PkmStat.DEFENSE, -1, 1) if random.random() < .2 else None)
ShadowSneak = PkmMove(40., 1., 20, PkmType.GHOST, "Mach Punch", priority=True)
OminousWind = PkmMove(60., 1., 5, PkmType.GHOST, "Ominous Wind", lambda v: (v.set_stage(PkmStat.ATTACK, 1, 0),
                                                                            v.set_stage(PkmStat.DEFENSE, 1, 0),
                                                                            v.set_stage(PkmStat.SPEED, 1,
                                                                                        0)) if random.random() < .1 else None)

# Dragon Moves
DragonRage = PkmMove(0., 1., 10, PkmType.DRAGON, "Dragon Rage", lambda v: v.set_fixed_damage(40.))
DracoMeteor = PkmMove(130., .9, 5, PkmType.DRAGON, "Draco Meteor", lambda v: v.set_stage(PkmStat.ATTACK, -2, 0))
DragonBreath = PkmMove(60., 1., 20, PkmType.DRAGON, "Dragon Breath", lambda v: v.set_status(PkmStatus.PARALYZED, 1))
Outrage = PkmMove(120., 1., 10, PkmType.DRAGON, "Outrage", lambda v: v.set_status(PkmStatus.CONFUSED, 0))

# Dark Moves
NastyPlot = PkmMove(0., 1., 5, PkmType.DARK, "Nasty Plot", lambda v: v.set_stage(PkmStat.ATTACK, 2, 0))
Crunch = PkmMove(80., 1., 15, PkmType.DARK, "Crunch",
                 lambda v: v.set_stage(PkmStat.DEFENSE, -1, 1) if random.random() < .2 else None)
Snarl = PkmMove(55., .95, 15, PkmType.DARK, "Snarl", lambda v: v.set_stage(PkmStat.ATTACK, -1, 1))

# Steel Moves
IronDefense = PkmMove(0., 1., 5, PkmType.STEEL, "Iron Defense", lambda v: v.set_stage(PkmStat.DEFENSE, 2, 0))
IronTail = PkmMove(100., .75, 15, PkmType.STEEL, "Iron Tail",
                   lambda v: v.set_stage(PkmStat.DEFENSE, -1, 1) if random.random() < .3 else None)
SteelWing = PkmMove(70., .9, 20, PkmType.STEEL, "Steel Wing",
                    lambda v: v.set_stage(PkmStat.DEFENSE, 1, 0) if random.random() < .1 else None)
BulletPunch = PkmMove(40., 1., 20, PkmType.STEEL, "Bullet Punch", priority=True)

# Fairy Moves
SweetKiss = PkmMove(0., .75, 5, PkmType.FAIRY, "Sweet Kiss", lambda v: v.set_status(PkmStatus.CONFUSED, 1))
PlayRough = PkmMove(90., .9, 10, PkmType.FAIRY, "Play Rough",
                    lambda v: v.set_stage(PkmStat.ATTACK, -1, 1) if random.random() < .1 else None)
Moonblast = PkmMove(95., 1., 15, PkmType.FAIRY, "Moonblast",
                    lambda v: v.set_stage(PkmStat.ATTACK, -1, 1) if random.random() < .3 else None)

# Standard Move Pool
STANDARD_MOVE_POOL = [Recover, DoubleEdge, ExtremeSpeed, Slam, Tackle, SunnyDay, FireBlast, Flamethrower,
                      Ember, RainDance, HydroPump, AquaJet, BubbleBeam, ThunderWave, Thunder, Thunderbolt,
                      ThunderShock, Spore, GigaDrain, RazorLeaf, EnergyBall, Hail, Blizzard, IceBeam,
                      IceShard, BulkUp, MachPunch, CloseCombat, DynamicPunch, Poison, GunkShot, PoisonJab,
                      AcidSpray, Spikes, EarthPower, Earthquake, MudShot, Roost, Chatter, Hurricane,
                      WingAttack, CalmMind, Psychic, PsychoBoost, Psybeam, StringShot, BugBuzz, LeechLife,
                      SilverWind, Sandstorm, PowerGem, RockTomb, StoneEdge, NightShade, ShadowBall,
                      ShadowSneak, OminousWind, DragonRage, DracoMeteor, DragonBreath, Outrage, NastyPlot,
                      Crunch, Snarl, IronDefense, IronTail, SteelWing, BulletPunch, SweetKiss, PlayRough,
                      Moonblast]

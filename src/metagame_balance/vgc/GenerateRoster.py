import argparse
import pickle
import os
from metagame_balance.vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator

def main(args):

    base_roster = RandomPkmRosterGenerator(None, n_moves_pkm=4, roster_size=args.num_pkm).gen_roster()
    filepath =  os.path.join(args.roster_path, "roster_{}_OP_0.pkl".format(args.num_pkm))
    pickle.dump(base_roster, open(filepath, 'wb'))
    """
    Code below is to create a an Roster with a OP pokmeon
    OP is defined as max health and max stats for one unique move to that pokemon
    TODO: use json instead of pickle
    """
    """
    base_roster = list(base_roster)
    from collections import defaultdict
    seen_moves = defaultdict(int)
    for pkm in base_roster:
        for move in pkm.move_roster:
            seen_moves[move] += 1

    for pkm in base_roster:
        for move in pkm.move_roster:
            if seen_moves[move] == 1:
                pkm.max_hp = 500
                move.power = 150
                move.acc = 100
                move.max_pp = 20
                break
        if pkm.max_hp == 500:
            break
    print(base_roster[0].max_hp)
    if base_roster[0].max_hp == 500:
        for move in base_roster[0].move_roster:
            print(move.name, move.power, move.acc, move.max_pp)
        import pickle
        pickle.dump(base_roster, open("roster_30_OP_1.pkl", 'wb'))
    import sys
    sys.exit(0)
    """
    """
    Code below is to generate roster pokmeons with same move set but different (random max hp)
    """
    """
    from copy import deepcopy
    import random
    pkm = list(RandomPkmRosterGenerator(None, n_moves_pkm=4, roster_size=1).gen_roster())[0]
    base_roster = [deepcopy(pkm) for i in range(NUM_PKM)]
    for i in range(NUM_PKM):
        base_roster[i].pkm_id = i
        base_roster[i].max_hp = random.randint(100, 300)

    """


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_pkm', type=int, default=30)
    parser.add_argument('--roster_path', type=str, default='')
    args = parser.parse_args()
    main(args)

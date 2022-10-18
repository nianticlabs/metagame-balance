import argparse
import datetime
import logging
import os

import numpy as np

from metagame_balance.cool_game.env import CoolGameEnvironment, CoolGameStateDelta, CoolGameState
from metagame_balance.framework import Balancer
from metagame_balance.rpsfw_scratch import RPSFWEnvironment, RPSFWStateDelta
from metagame_balance.vgc.util.RosterParsers import MetaRosterStateParser as VGCParser
from metagame_balance.vgc_scratch import VGCEnvironment, VGCStateDelta
from metagame_balance.policies.CMAESBalancePolicy import CMAESBalancePolicyV2


def init_rpsfw_domain(args: argparse.Namespace):
    return {
        "balancer": CMAESBalancePolicyV2(init_var=0.7),
        "env": RPSFWEnvironment(epochs=args.selection_epochs,
                              reg_param  = args.reg,
                              alg_baseline = args.baseline),
        # "parser": RPSFWParser(num_items=args.game_size)
        "state_delta_constructor": RPSFWStateDelta.decode,
        "name": "rpsfw"
            }


def init_vgc_domain(args: argparse.Namespace):
    return {
        "balancer": CMAESBalancePolicyV2(init_var=0.05),
        "env": VGCEnvironment(roster_path=args.roster_path or None,
                              n_league_epochs=args.n_league_epochs,
                              n_battles_per_league=args.n_battles_per_league,
                              reg_param  = args.reg,
                              alg_baseline = args.baseline
                              ),
        "parser": VGCParser(num_pkm=args.num_pkm or None,
                            consider_hp=not args.ignore_hp),
        "state_delta_constructor": VGCStateDelta.decode,
        "name": "vgc",
    }


def init_coolgame_domain(args: argparse.Namespace):
    return {
        "balancer": CMAESBalancePolicyV2(
            init_var=args.cmaes_init_var,
        ),
        "env": CoolGameEnvironment(epochs=args.selection_epochs,
            reg_param = args.reg,
            alg_baseline = args.baseline
            ),
        "state_delta_constructor": CoolGameStateDelta.decode,
        "name": "cool_game"
    }


def setup_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_epochs', type=int, default=1)
    parser.add_argument("--snapshot_gameplay_policy_epochs", type=int, default=100)
    parser.add_argument("--snapshot_game_state_epochs", type=int, default=100)
    subparsers = parser.add_subparsers(help="domain")

    # rpsfw
    rpsfw_parser = subparsers.add_parser('rpsfw')
    # TODO trickle config down
    rpsfw_parser.add_argument('--game_size', type=int, default=5)
    rpsfw_parser.add_argument("--selection_epochs", type=int, default=10)
    rpsfw_parser.add_argument('--baseline', action='store_true')
    rpsfw_parser.add_argument('--reg', type=float, default=0)
    rpsfw_parser.set_defaults(func=init_rpsfw_domain)

    # vgc
    vgc_parser = subparsers.add_parser("vgc")
    vgc_parser.add_argument('--n_league_epochs', type=int, default=1)
    vgc_parser.add_argument('--n_battles_per_league', type=int, default=10)
    vgc_parser.add_argument('--roster_path', type=str)
    vgc_parser.add_argument('--num_pkm', type=int, default=30)
    vgc_parser.add_argument('--reg', type=float, default=0)
    vgc_parser.add_argument('--ignore_hp', action='store_true')
    vgc_parser.add_argument('--baseline', action='store_true')
    vgc_parser.set_defaults(func=init_vgc_domain)

    coolgame_parser = subparsers.add_parser("coolgame")
    coolgame_parser.add_argument("--cmaes_init_var", type=float, default=0.05)
    coolgame_parser.add_argument('--baseline', action='store_true')
    coolgame_parser.add_argument("--selection_epochs", type=int, default=10)
    coolgame_parser.add_argument('--reg', type=float, default=0)
    coolgame_parser.set_defaults(func=init_coolgame_domain)

    return parser


class IgnoreGymFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return not record.getMessage().startswith("gym")


def main():
    parser = setup_argparser()
    args = parser.parse_args()

    # fun trick from argparse docs, this calls the "func" defined in set_defaults above
    domain = None
    try:
        domain = args.func(args)
    except AttributeError:
        # if no subcommand was called
        parser.print_help()
        parser.exit()

    now = datetime.datetime.now()

    slug = f'{domain["name"]}_{now.strftime("%Y%m%d__%H_%M_%S")}'
    # TODO don't hardcode prefix
    prefix = f'./experiments/{slug}'

    logfile = os.path.join(prefix, "log.log")
    os.makedirs(prefix, exist_ok=True)
    logging.basicConfig(filename=logfile, level=logging.INFO, force=True)
    logging.getLogger().addFilter(IgnoreGymFilter())
    for h in logging.getLogger().handlers:
        h.addFilter(IgnoreGymFilter())

    logging.info(f"Called with: {str(args)}")
    balancer = Balancer(domain['balancer'], domain['env'], domain['state_delta_constructor'],
                        args.snapshot_game_state_epochs,
                        args.snapshot_gameplay_policy_epochs, prefix)
    balancer.run(args.n_epochs)


if __name__ == "__main__":
    main()

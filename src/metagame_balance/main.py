import argparse

from metagame_balance.framework import Balancer
from metagame_balance.rpsfw_scratch import RPSFWEnvironment, RPSFWStateDelta
from metagame_balance.rpsfw.util.Parsers import MetaRosterStateParser as RPSFWParser
from metagame_balance.vgc.util.RosterParsers import MetaRosterStateParser as VGCParser
from metagame_balance.vgc_scratch import VGCEnvironment, VGCStateDelta
from metagame_balance.policies.CMAESBalancePolicy import CMAESBalancePolicyV2


def init_rpsfw_domain(args: argparse.Namespace):
    return {
        "env": RPSFWEnvironment(epochs=args.n_epochs),
        "parser": RPSFWParser(num_items=args.game_size)
            }


def init_vgc_domain(args: argparse.Namespace):
    return {
        "env": VGCEnvironment(roster_path=args.roster_path or None),
        "parser": VGCParser(num_pkm=args.num_pkm or None,
                            consider_hp=args.consider_hp)
    }


def setup_argparser():
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help="domain")

        # rpsfw
        rpsfw_parser = subparsers.add_parser('rpsfw')
        # TODO trickle config down
        rpsfw_parser.add_argument('--game_size', type=int, default=5)
        rpsfw_parser.add_argument("--n_epochs", type=int, default=10)
        rpsfw_parser.set_defaults(func=init_rpsfw_domain)

        # vgc
        vgc_parser = subparsers.add_parser("vgc")
        vgc_parser.add_argument('--roster_path', type=str)
        vgc_parser.add_argument('--num_pkm', type=int)
        vgc_parser.add_argument('--consider_hp', action='store_true')
        vgc_parser.set_defaults(func=init_vgc_domain)

        return parser


def run():
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
    balancer = Balancer(CMAESBalancePolicyV2(), domain['env'], domain['parser'].state_to_delta_roster)
    balancer.run(args.n_epochs)


if __name__ == "__main__":
    run()

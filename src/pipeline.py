from pathlib import Path

import kfp
from kfp import LocalClient
from kfp.v2 import dsl
from kfp.v2.components.types.artifact_types import Artifact
from kfp.v2.dsl import Input, Dataset, Output
from metagame_balance.main import main


@dsl.component(
    base_image='python:3.8',
    target_image='gcr.io/ml-rel/metagame-balance'
)
def run_vgc(
        n_epochs: int,
        regularization: float,
        cma_init_var: float,
        stage2_iter: int,
        stage1_iter: int,
        num_pkm: int,
        team_size: int,
        logfile: Output[Artifact],
        last_game_state: Output[Artifact],
        entropy_values: Output[Artifact],
        last_policy_adversary: Output[Artifact],
        last_policy_agent: Output[Artifact],
        reward_plot: Output[Artifact],
):
    #  parser = argparse.ArgumentParser()
    #     parser.add_argument('--n_epochs', type=int, default=1)
    #     parser.add_argument('--reg', type=float, default=0)
    #     subparsers = parser.add_subparsers(help="domain")
    # vgc_parser.add_argument("--cma_init_var", type=float, default=0.05)
    #     # stage2 iter
    #     vgc_parser.add_argument('--n_league_epochs', type=int, default=1)
    #     # stage1 iter
    #     vgc_parser.add_argument('--n_battles_per_league', type=int, default=10)
    #     vgc_parser.add_argument('--roster_path', type=str)
    #     vgc_parser.add_argument('--num_pkm', type=int, default=30)
    #     vgc_parser.add_argument('--ignore_hp', action='store_true')
    #     vgc_parser.add_argument('--team_size', type=int, default=3)
    args = ['vgc',
            '--n_epochs', str(n_epochs),
            '--reg', str(regularization),
            '--cma_init_var', str(cma_init_var),
            '--n_league_epochs', str(stage2_iter),
            '--n_battles_per_league', str(stage1_iter),
            '--num_pkm', str(num_pkm),
            '--team_size', str(team_size)]
    o = main(args)

    pairs = [(o.log, logfile), (o.last_game_state, last_game_state),
             (o.entropy_values, entropy_values), (o.last_policy_agent, last_policy_agent),
             (o.last_policy_adversary, last_policy_adversary), (o.reward_plot, reward_plot)]

    for vgc_output, pipeline_output in pairs:
        with vgc_output.open("r") as infile, open(pipeline_output.path, "w") as outfile:
            outfile.write(infile.read())


@dsl.pipeline("funny")
def pipeline():
    task = run_vgc(1, 1, 1, 1, 1, 10, 2)


if __name__ == "__main__":
    kfp.run_pipeline_func_locally(pipeline, arguments={},
                                  execution_mode=LocalClient.ExecutionMode('docker'))
# if __name__ == "__main__":
#     run_vgc(
#         1,
#         1,
#         1,
#         1,
#         1,
#         10,
#         2,
#         Output
#     )
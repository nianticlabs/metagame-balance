"""
This module contains a kubeflow pipeline used for running copies of the experiment in parallel.
"""

import kfp
import kfp.components as comp
from kfp import dsl, LocalClient
from kfp.components import create_component_from_func

from kubernetes import client as k8s_client


def _download_gcs(gcs_uri: str,
                  downloaded: comp.OutputBinaryFile(str)):
    from gcsfs import GCSFileSystem
    fs = GCSFileSystem()

    with fs.open(gcs_uri, "rb") as infile:
        downloaded.write(infile.read())


download_gcs = create_component_from_func(
    _download_gcs,
    base_image="python:3.8",
    packages_to_install=[
        "gcsfs~=2022.8.2"
    ]
)


def _run_vgc(
        regularization: float,
        cma_init_var: float,
        stage2_iter: int,
        stage1_iter: int,
        num_pkm: int,
        team_size: int,
        baseline: bool,
        update_after: int,
        roster: comp.InputPath(str),
        logfile: comp.OutputTextFile(str),
        last_game_state: comp.OutputBinaryFile(str),
        entropy_values: comp.OutputBinaryFile(str),
        last_policy_adversary: comp.OutputBinaryFile(str),
        last_policy_agent: comp.OutputBinaryFile(str),
        reward_plot: comp.OutputBinaryFile(str),
        last_encoded_gamestate: comp.OutputBinaryFile(str)
):
    from metagame_balance.main import main
    from io import TextIOWrapper


    # these need to be in the right order
    args = [
            '--n_epochs', str(stage1_iter),
            '--reg', str(regularization),
            'vgc',
            '--cma_init_var', str(cma_init_var),
            '--update_after', str(update_after),
            '--n_league_epochs', str(1),
            '--n_battles_per_league', str(stage2_iter),
            '--num_pkm', str(num_pkm),
            '--team_size', str(team_size),
            '--roster_path', roster
    ]

    if baseline:
        args.insert(0, "--baseline")

    o = main(args)

    pairs = [(o.log, logfile), (o.last_game_state, last_game_state),
             (o.entropy_values, entropy_values), (o.last_policy_agent, last_policy_agent),
             (o.last_policy_adversary, last_policy_adversary), (o.reward_plot, reward_plot),
             (o.last_encoded_gamestate, last_encoded_gamestate)]

    for vgc_output, pipeline_output in pairs:
        if isinstance(pipeline_output, TextIOWrapper):
            read_options = "r"
        else:
            read_options = "rb"
        with vgc_output.open(read_options) as infile:
            # outputs are textIOWrappers or BytesIO
            pipeline_output.write(infile.read())


run_vgc = create_component_from_func(
    func=_run_vgc,
    base_image='python:3.8',
    packages_to_install=[
        "numpy>=1.15.4",
        "gym>=0.10.9",
        "PySimpleGUI>=4.20.0",
        "simple-plugin-loader>=1.6",
        "elo>=0.1.1,<0.2.0",
        "arcade>=2.6.7,<2.7.0",
        "cma==3.2.2",
        "torch==1.10.2",
        "scipy>=1.5",
        "tqdm==4.64.1",
        "matplotlib==3.6.1",
        "metagame-balance==0.5.3"
    ]
)


@dsl.pipeline("vgc_experiment",
              description="metagame balance experiments pipeline")
def pipeline(
        stage1_iter: int,
        regularization: float,
        cma_init_var: float,
        stage2_iter: int,
        num_pkm: int,
        team_size: int,
        baseline: bool,
        update_after: int,
        roster_gcs_uri: str
):
    volume_name = "user-pypi-config"
    secret_name = "pypi-config"
    secret_mount_path = "/etc/xdg/pip"  # Pip global config path

    download_roster = download_gcs(
        gcs_uri=roster_gcs_uri
    )

    task = run_vgc(
        regularization=regularization,
        cma_init_var=cma_init_var,
        stage2_iter=stage2_iter,
        stage1_iter=stage1_iter,
        num_pkm=num_pkm,
        team_size=team_size,
        baseline=baseline,
        update_after=update_after,
        roster=download_roster.output
    )

    task.add_volume(
        k8s_client.V1Volume(name=volume_name,
                            secret=k8s_client.V1SecretVolumeSource(
                                secret_name=secret_name
                            ))
    )
    task.container.add_volume_mount(
        k8s_client.V1VolumeMount(name=volume_name, mount_path=secret_mount_path)
    )
    (task.set_memory_request('4G')
        .set_memory_limit('32G')
        .set_cpu_request('2')
        .set_cpu_limit('4')
        .add_node_selector_constraint('cloud.google.com/gke-nodepool', "cpu-worker-pool-highcpu")
     )


if __name__ == "__main__":
    from kfp import compiler, dsl

    cmplr = compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V1_LEGACY)
    cmplr.compile(pipeline, "test.yaml")
    #
    # kfp.run_pipeline_func_locally(pipeline, arguments={},
    #                               execution_mode=LocalClient.ExecutionMode('docker'))

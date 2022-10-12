import kfp
import kfp.components as comp
from kfp import dsl, LocalClient
from kfp.components import create_component_from_func

from kubernetes import client as k8s_client


def _run_vgc(
        n_epochs: int,
        regularization: float,
        cma_init_var: float,
        stage2_iter: int,
        stage1_iter: int,
        num_pkm: int,
        team_size: int,
        logfile: comp.OutputTextFile(str),
        last_game_state: comp.OutputBinaryFile(str),
        entropy_values: comp.OutputBinaryFile(str),
        last_policy_adversary: comp.OutputBinaryFile(str),
        last_policy_agent: comp.OutputBinaryFile(str),
        reward_plot: comp.OutputBinaryFile(str)
):
    from metagame_balance.main import main
    from kfp import components as comp

    # these need to be in the right order
    args = [
            '--n_epochs', str(n_epochs),
            '--reg', str(regularization),
            'vgc',
            '--cma_init_var', str(cma_init_var),
            '--n_league_epochs', str(stage2_iter),
            '--n_battles_per_league', str(stage1_iter),
            '--num_pkm', str(num_pkm),
            '--team_size', str(team_size)]

    print("pingy")

    o = main(args)

    pairs = [(o.log, logfile), (o.last_game_state, last_game_state),
             (o.entropy_values, entropy_values), (o.last_policy_agent, last_policy_agent),
             (o.last_policy_adversary, last_policy_adversary), (o.reward_plot, reward_plot)]

    for vgc_output, pipeline_output in pairs:
        with vgc_output.open("r") as infile:
            # outputs are textIOWrappers or ByteIOWrappers
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
        "matplotlib==3.3.4",
        "metagame-balance==0.1.0"
    ]
)


@dsl.pipeline("vgc_experiment",
              description="metagame balance experiments pipeline",
              pipeline_root="gs://niantic-ml-data/ml-intern-rl/pipelines/experiment_v1")
def pipeline(
        # n_epochs: int,
        # regularization: float,
        # cma_init_var: float,
        # stage2_iter: float
):
    volume_name = "user-pypi-config"
    secret_name = "pypi-config"
    secret_mount_path = "/etc/xdg/pip"  # Pip global config path

    task = run_vgc(
        n_epochs=1,
        regularization=1,
        cma_init_var=1,
        stage2_iter=1,
        stage1_iter=1,
        num_pkm=10,
        team_size=2)

    task.add_volume(
        k8s_client.V1Volume(name=volume_name,
                            secret=k8s_client.V1SecretVolumeSource(
                                secret_name=secret_name
                            ))
    )
    task.container.add_volume_mount(
        k8s_client.V1VolumeMount(name=volume_name, mount_path=secret_mount_path)
    )


if __name__ == "__main__":
    from kfp import compiler, dsl

    cmplr = compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V1_LEGACY)
    cmplr.compile(pipeline, "test.yaml")
    #
    # kfp.run_pipeline_func_locally(pipeline, arguments={},
    #                               execution_mode=LocalClient.ExecutionMode('docker'))

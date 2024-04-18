# Import the Kubeflow Pipelines SDK and other libraries
import os
import kfp
import kfp.components as comp
import kfp.dsl as dsl
from kfp_utils.util import disable_cache

@dsl.pipeline(
    name="Nord-Pas-de-Calais Creating Synthetic Data and Matsim Simulation",
    description="A pipeline that create the synthetic data and simulate a Matsim using KFServing"
)
def auto_simulation(
    department="Il-de-France",
    major="0",
    minor="1",
    revision="0",
    results="",
    dataset_dir="",
    docker_image="",
    # code=,
):
    suffix = "v{}.{}.{}b".format(major, minor, revision)

    data_transform = dsl.ContainerOp(

        name="Data Transform",
        image=docker_image,
        command="python3",
        arguments=[
            #"projects/classification/potato/main_.py",
            #all agruments from function of data creation function
            "--suffix",
            suffix,
        ],
    )

    data_transform = disable_cache(data_transform)

    synthesis = dsl.ContainerOp(
        name="synthesis",
        image=docker_image,
        command="python3",
        arguments=[
            # "projects/classification/potato/main_.py",
            # all agruments from function of data creation function
            "--suffix",
            suffix,
        ],
    )
    synthesis = disable_cache(synthesis)

    matsim_simulation1 = dsl.ContainerOp(
        name="matsim_simulation1",
        image=docker_image,
        command="python3",
        arguments=[
            # "projects/classification/potato/main_.py",
            # all agruments from function of data creation function
            "--suffix",
            suffix,
        ],
    )
    matsim_simulation1 = disable_cache(matsim_simulation1)

    matsim_simulation2 = dsl.ContainerOp(
        name="matsim_simulation2",
        image=docker_image,
        command="python3",
        arguments=[
            # "projects/classification/potato/main_.py",
            # all agruments from function of data creation function
            "--suffix",
            suffix,
        ],
    )
    matsim_simulation2 = disable_cache(matsim_simulation2)

    test = dsl.ContainerOp(
        name="test",
        image=docker_image,
        command="python3",
        arguments=[
            # "projects/classification/potato/main_.py",
            # all agruments from function of data creation function
            "--suffix",
            suffix,
        ],
    )
    test = disable_cache(test)

    synthesis.after(data_transform)
    matsim_simulation1.after(synthesis)
    matsim_simulation2.after(matsim_simulation1)
    test.after(matsim_simulation2)
    dsl.get_pipeline_conf().set_image_pull_policy(policy="Always")

    # it lost virtual machine information to mount data,


if __name__ == '__main__':
  kfp.compiler.Compiler().compile(auto_simulation, package_path='my-app.yaml')
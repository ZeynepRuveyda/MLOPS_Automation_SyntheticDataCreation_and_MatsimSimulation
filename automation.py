# Import the Kubeflow Pipelines SDK and other libraries
import os

import kfp
import kfp.components as comp
import kfp.dsl as dsl

from kubernets.clients import V1Volume, V1VolumeMount

# Create volume and data management and transform
def data_transform():
    vop = dsl.VolumeOp(name="pvc",
                       resource_name="pvc", size='20Gi', 
                       modes=dsl.VOLUME_MODE_RWO)

    return dsl.ContainerOp(
        name = '', 
        image = '', 
        command = ['python3', '.py'],

        pvolumes={
            'npc/data': vop.volume
        }
    )

def synthesis(comp1):
    return dsl.ContainerOp(
        name = 'synthesis',
        image = '',
        pvolumes={
            'npc/data': comp1.pvolumes['npc/data']
        },
        command = ['python3', 'output.py']
    )    

def matsim_simulation1(comp2):
    return dsl.ContainerOp(
        name = 'matsim_simulation1',
        image = '',
        pvolumes={
            'npc/data': comp2.pvolumes['npc/data']
        },
        command = ['python3', 'output.py']
    )

def matsim_simulation2(comp3):
    return dsl.ContainerOp(
        name = 'matsim_simulation2',
        image = '',
        pvolumes={
            'npc/data': comp2.pvolumes['npc/data']
        },
        command = ['python3', 'writers.py']
    )

def test(comp4):
    return dsl.ContainerOp(
        name = 'test',
        image = '',
        pvolumes={
            'npc/data': comp2.pvolumes['npc/data']
        },
        command = ['python3', 'test.py']
    )    


# Define the pipeline using the Kubeflow Pipelines DSL
@dsl.pipeline(
    name="Nord-Pas-de-Calais Creating Synthetic Data and Matsim Simulation",
    description="A pipeline that create the synthetic data and simulate a Matsim using KFServing"
)

def  passing_parameter():
    comp1 = data_transform().add_pod_label("automation", "true")
    comp2 = matsim_simulation1(comp1)
    comp3 = matsim_simulation2(comp2)
    comp4 = Test(comp4)
    

# Compile and run the pipeline

if __name__ == '__main__':
  kfp.compiler.Compiler().compile(automation_pipeline, package_path='my-app.yaml')
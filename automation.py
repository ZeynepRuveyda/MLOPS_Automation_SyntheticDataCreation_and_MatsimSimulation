# Import the Kubeflow Pipelines SDK and other libraries
import os

import kfp
import kfp.components as comp
import kfp.dsl as dsl

# Create volume and data management and transform
def data_transform():
    vop = dsl.VolumeOp(name="pvc",
                       resource_name="pvc", size='1Gi', 
                       modes=dsl.VOLUME_MODE_RWO)

    return dsl.ContainerOp(
        name = '/minikube', 
        image = 'gcr.io/k8s-minikube/kicbase:v0.0.42@sha256:d35ac07dfda971cabee05e0deca8aeac772f885a5348e1a0c0b0a36db20fcfc0', 
        command = ['python3', '.py'],

        pvolumes={
            '/data': vop.volume
        }
    )

def synthesis(comp1):
    return dsl.ContainerOp(
        name = 'synthesis',
        image = '',
        pvolumes={
            '/data': comp1.pvolumes['/data']
        },
        command = ['python3', 'output.py']
    )    

def matsim_simulation1(comp2):
    return dsl.ContainerOp(
        name = 'matsim_simulation1',
        image = '',
        pvolumes={
            '/data': comp2.pvolumes['/data']
        },
        command = ['python3', 'output.py']
    )

def matsim_simulation2(comp3):
    return dsl.ContainerOp(
        name = 'matsim_simulation2',
        image = '',
        pvolumes={
            '/data': comp2.pvolumes['/data']
        },
        command = ['python3', 'writers.py']
    )

def test(comp4):
    return dsl.ContainerOp(
        name = 'test',
        image = '',
        pvolumes={
            '/data': comp2.pvolumes['/data']
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
  kfp.compiler.Compiler().compile(automation_pipeline, __file__[:-3]+ '.yaml')
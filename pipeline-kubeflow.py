import kfp
from kfp.components import create_component_from_func
import os
import subprocess
from kfp import dsl
import kfp.dsl as dsl
from kfp import compiler

@dsl.pipeline(
    name="Nord-Pas-de-Calais Creating Synthetic Data and Matsim Simulation",
    description="A pipeline that creates synthetic data and simulates a Matsim using KFServing"
)
def synthetic_population_pipeline(
    # Parameters for the pipeline function
    working_directory: str = '/home/ozelz/npc1/tmp', 
    data_path: str = '/home/ozelz/npc1/data',
    output_path: str = '/home/ozelz/npc1/output',
    processes: int = 4,
    hts: str = 'entd',
    sampling_rate: float = 0.001,
    random_seed: int = 1234,
    java_memory: str = '48G',
    mode_choice: bool = True,
    regions: list = [],
    departments: list = ["59", "62"],
    gtfs_path: str = 'gtfs_npc',
    osm_path: str = 'osm_npc',
    ban_path: str = 'ban_npc',
    bdtopo_path: str = 'bdtopo_npc',
    osmosis_binary: str = '/home/ozelz/osmosis/bin/osmosis'
):

    # Define a volume to mount
    volume = dsl.VolumeOp(
        name="volume",
        resource_name="mlpipeline-minio-artifact",
        modes=dsl.VOLUME_MODE_RWO
    )
    
    # Define pipeline steps here
    with dsl.Pipeline() as pipeline:
        # Step 1: Run the main processing task
        synpp_command = f'python3 -m synpp --working-directory {working_directory} --data-path {data_path} --output-path {output_path}'
        synpp_task = dsl.ContainerOp(
            name='run-synpp',
            image='zeynep02/my-app-v7:latest',  # Use your custom image here
            command=['sh', '-c', synpp_command],
            volumes=[volume.volume]
        )

        # Mount the volume to the container
        synpp_task.add_volume_mount(volume.volume_mount)        

# Define the parts of the pipeline to run
partstorun = [
    'synthesis.output',  # To create the output population in the output_path
    'matsim.output'  # You'll need Java for that and Uncomment the line below if you want to run the full simulation
] 

# This section defines which parts of the pipeline should be run
run = partstorun# Compile and run the pipeline
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(synthetic_population_pipeline, package_path='my-app.yaml')

    


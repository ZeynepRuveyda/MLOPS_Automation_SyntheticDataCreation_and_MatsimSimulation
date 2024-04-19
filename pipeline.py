import os
import subprocess
import kfp.dsl as dsl

def synthetic_population_pipeline(
    working_directory: str = '/home/ozelz/npc1/tmp', # where the pipeline can store temporary data
    processes: int = 4,
    hts: str = 'entd', # Define whether to use ENTD or EGT as the household travel survey (HTS)
    # Define sampling rate and random seed for the output population
    sampling_rate: float = 0.001,
    random_seed: int = 1234,
    # Paths to the input data and where the output should be stored
    data_path: str = '/home/ozelz/npc1/data',
    output_path: str = '/home/ozelz/npc1/output',
    java_memory: str = '48G',  # Only interesting if you run the simulation
    mode_choice: bool = True,  # Activate if you want to run mode choice
    
    # Uncommented below to enable vehicle fleet generation
    # generate_vehicles_file: bool = True,
    # generate_vehicles_method: str = fleet_sample,
    # vehicles_data_year: int = 2015,
   
    regions: list = [],
    departments: list = ["59", "62"],
    gtfs_path: str = 'gtfs_npc',
    osm_path: str = 'osm_npc',
    ban_path: str = 'ban_npc',
    bdtopo_path: str = 'bdtopo_npc',
    osmosis_binary: str = '/home/ozelz/osmosis/bin/osmosis'
):

# Define the pipeline using the Kubeflow Pipelines DSL
@dsl.pipeline(
    name="Nord-Pas-de-Calais Creating Synthetic Data and Matsim Simulation",
    description="A pipeline that create the synthetic data and simulate a Matsim using KFServing"
)
    # Define volume mounts for container images
    volumes = [
        dsl.VolumeOp(name='working-dir', resource_name='working-dir', mount_path=working_directory),
        dsl.VolumeOp(name='data', resource_name='data', mount_path=data_path),
        dsl.VolumeOp(name='output', resource_name='output', mount_path=output_path),
    ]
    
    # Define pipeline steps here
    with dsl.Pipeline() as pipeline:
        # Step 1: Create cache, tmp, and output directories
        create_dirs_task = dsl.ContainerOp(
            name='create-dirs',
            image='busybox',
            command=['sh', '-c', f'mkdir -p {working_directory} {output_path} {working_directory}/tmp']
        ).apply(volumes)
        
        # Step 2: Run the main processing task
        synpp_command = f'python3 -m synpp --working-directory {working_directory} --data-path {data_path} --output-path {output_path}'
        synpp_task = dsl.ContainerOp(
            name='run-synpp',
            image='python:3',
            command=['sh', '-c', synpp_command]
        ).apply(volumes)

# Define the parts of the pipeline to run
parts_to_run = [
    'synthesis.output',  # To create the output population in the output_path
    # Uncomment the line below if you want to run the full simulation
    'matsim.output'  # You'll need Java for that
]

# This section defines which parts of the pipeline should be run
run = parts_to_run

# Compile and run the pipeline
if __name__ == '__main__':
  kfp.compiler.Compiler().compile(automation_pipeline, package_path='my-app.yaml')

import os
import subprocess
import kfp.dsl as dsl

# Define the pipeline using the Kubeflow Pipelines DSL
@dsl.pipeline(
    name="Nord-Pas-de-Calais Creating Synthetic Data and Matsim Simulation",
    description="A pipeline that create the synthetic data and simulate a Matsim using KFServing"
)

def synthetic_population_pipeline(
    # Update the data path to match the Dockerfile
    working_directory: str = '/home/ozelz/npc1/tmp', # where the pipeline can store temporary data
    data_path: str = '/home/ozelz/npc1/data',    #'/data'
    output_path: str = '/home/ozelz/npc1/output', #'/output'
    processes: int = 4,
    hts: str = 'entd', # Define whether to use ENTD or EGT as the household travel survey (HTS)
    # Define sampling rate and random seed for the output population
    sampling_rate: float = 0.001,
    random_seed: int = 1234,
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

    # Define pipeline steps here
    with dsl.Pipeline() as pipeline:
        # Step 1: Run the main processing task
        synpp_command = f'python3 -m synpp --working-directory {working_directory} --data-path {data_path} --output-path {output_path}'
        synpp_task = dsl.ContainerOp(
            name='run-synpp',
            image='docker.io/zeynep02/my-app-v6',  # Use your custom image here
            command=['sh', '-c', synpp_command]
        )


# Define the parts of the pipeline to run
partstorun = [
    'synthesis.output',  # To create the output population in the output_path
    'matsim.output'  # You'll need Java for that and Uncomment the line below if you want to run the full simulation
]


# This section defines which parts of the pipeline should be run
run = partstorun

# Compile and run the pipeline
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(automation_pipeline, package_path='my-app.yaml')

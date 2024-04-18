# Use an official Anaconda runtime as a parent image
FROM continuumio/anaconda3:latest

# Set the working directory in the container
WORKDIR /app

# Copy the environment.yml file into the container at /app
COPY environment.yml .

# Create the Conda environment
RUN conda env create -f environment.yml

# Activate the Conda environment
RUN echo "source activate $(head -1 environment.yml | cut -d' ' -f2)" > ~/.bashrc
RUN PATH /opt/conda/envs/$(head -1 environment.yml | cut -d' ' -f2)/bin:$PATH
#ENV PATH /opt/conda/envs/$(head -1 environment.yml | cut -d' ' -f2)/bin:$PATH

# Copy the current directory contents into the container at /app
COPY . .

# Specify the command to run on container start
CMD ["python3", "automation(1).py"]
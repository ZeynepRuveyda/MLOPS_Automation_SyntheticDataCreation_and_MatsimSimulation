# Use an official Anaconda runtime as a parent image
FROM continuumio/anaconda3:2024.02-1  
#latest

# Set the working directory in the container
ENV DIRECTORY=/app
WORKDIR ${DIRECTORY}
#WORKDIR /app

# Download and extract Osmosis
RUN wget https://github.com/openstreetmap/osmosis/releases/download/0.47.1/osmosis-0.47.1.tgz && \
    mkdir osmosis && \
    mv osmosis-0.47.1.tgz osmosis && \
    cd osmosis && \
    tar xvfz osmosis-0.47.1.tgz && \
    rm osmosis-0.47.1.tgz && \
    chmod a+x bin/osmosis


# Copy the environment.yml file into the container at /app
COPY . . 
#COPY environment.yml .

# Create the Conda environment
RUN conda env create -f environment.yml

# Activate the Conda environment
RUN echo "source activate $(head -1 $DIRECTORY/environment.yml | cut -d' ' -f2)" >> ~/.bashrc
RUN echo "export PATH=/opt/conda/envs/$(head -1 $DIRECTORY/environment.yml | cut -d' ' -f2)/bin:$PATH" >> ~/.bashrc
#RUN echo "source activate $(head -1 environment.yml | cut -d' ' -f2)" >> ~/.bashrc
#ENV PATH /opt/conda/envs/$(head -1 environment.yml | cut -d' ' -f2)/bin:$PATH >> ~/.bashrc

# Specify the command to run on container start
CMD ["bash", "-c", "python3", "pipeline1.py"]
#CMD ["python3", "pipeline.py"]

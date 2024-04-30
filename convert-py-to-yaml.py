import yaml

input_file = 'pipeline-kubeflow.py'
output_file = 'pipeline-kubeflow.yaml'

#read the python file
with open(input_file,'r') as f:
    python_code = f.read()

#convert to YAML file
yaml_code = yaml.dump(python_code, default_flow_style=False)

#create YAML file
with open(output_file,'w') as f:
    f.write(yaml_code)





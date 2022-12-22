import pandas as pd
import yaml

# Load the data into a DataFrame
df = pd.read_csv('sonar-data.csv')

# Convert the data types of the DataFrame to a dictionary
schema_dict = {column: str(dtype) for column, dtype in df.dtypes.items()}

# Create the YAML structure
schema_yaml = {'columns': [{column: dtype} for column, dtype in schema_dict.items()]}

# Use the `dump` method of the yaml library to write the dictionary to a YAML file
with open('schema.yaml', 'w') as file:
    yaml.dump(schema_yaml, file)


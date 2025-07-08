import os
import sys
import yaml
from yaml import SafeDumper

class CustomDumper(SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(CustomDumper, self).increase_indent(flow, False)

def get_changed_files():
    """
    Get the list of changed files from the command line arguments.
    """
    if len(sys.argv) < 2:
        print("No changed files provided.")
        return []
    return sys.argv[1:]

def validate_yaml(file_path):
    """
    Validate the YAML syntax of a file.
    """
    try:
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
    except (yaml.YAMLError, FileNotFoundError) as e:
        print(f"Error validating {file_path}: {e}")
        sys.exit(1)

def update_elastic_agent_config(input_file):
    """
    Update the elastic-agent.yml file with the new input.
    """
    location = os.path.dirname(os.path.dirname(input_file))
    main_config_path = os.path.join(location, 'elastic-agent.yml')

    if not os.path.exists(main_config_path):
        print(f"Error: {main_config_path} not found.")
        sys.exit(1)

    validate_yaml(main_config_path)

    with open(input_file, 'r') as f:
        new_inputs = yaml.safe_load(f)

    with open(main_config_path, 'r') as f:
        main_config = yaml.safe_load(f)

    if 'inputs' not in main_config or main_config['inputs'] is None:
        main_config['inputs'] = []

    # Process each new input
    for new_input in new_inputs:
        if 'id' not in new_input:
            print(f"Warning: Input without ID found in {input_file}, skipping")
            continue
            
        new_input_id = new_input['id']
        
        # Check if input with same ID already exists
        existing_input_index = None
        for i, existing_input in enumerate(main_config['inputs']):
            if existing_input.get('id') == new_input_id:
                existing_input_index = i
                break
        
        if existing_input_index is not None:
            # Update existing input
            main_config['inputs'][existing_input_index] = new_input
            print(f"Updated existing input with ID: {new_input_id}")
        else:
            # Add new input
            main_config['inputs'].append(new_input)
            print(f"Added new input with ID: {new_input_id}")

    with open(main_config_path, 'w') as f:
        yaml.dump(main_config, f, Dumper=CustomDumper, default_flow_style=False, indent=2, sort_keys=False, allow_unicode=True)

    validate_yaml(main_config_path)
    print(f"Successfully updated {main_config_path} with {input_file}")

if __name__ == "__main__":
    changed_files = get_changed_files()
    
    if not changed_files:
        print("No files to process.")
        sys.exit(0)
    
    print(f"Processing {len(changed_files)} changed files: {changed_files}")
    
    processed_files = 0
    for file_path in changed_files:
        if file_path.endswith('.yml') and 'inputs' in file_path and 'elastic-agent.yml' not in file_path:
            print(f"Processing input file: {file_path}")
            validate_yaml(file_path)
            update_elastic_agent_config(file_path)
            processed_files += 1
        else:
            print(f"Skipping file (not an input file): {file_path}")
    
    if processed_files == 0:
        print("No valid input files found to process.")
    else:
        print(f"Successfully processed {processed_files} input files.")
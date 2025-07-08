import os
import sys
import yaml

def get_changed_files():
    """
    Get the list of changed files from the command line arguments.
    """
    if len(sys.argv) < 2:
        print("No changed files provided.")
        sys.exit(0)
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
        new_input = yaml.safe_load(f)

    with open(main_config_path, 'r') as f:
        main_config = yaml.safe_load(f)

    if 'inputs' not in main_config:
        main_config['inputs'] = []

    main_config['inputs'].extend(new_input)

    with open(main_config_path, 'w') as f:
        yaml.dump(main_config, f, default_flow_style=False)

    validate_yaml(main_config_path)
    print(f"Successfully updated {main_config_path} with {input_file}")

if __name__ == "__main__":
    changed_files = get_changed_files()
    for file_path in changed_files:
        if file_path.endswith('.yml') and 'inputs' in file_path and 'elastic-agent.yml' not in file_path:
            validate_yaml(file_path)
            update_elastic_agent_config(file_path)
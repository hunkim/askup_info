import os
import subprocess

# Define input and output directories
jobs_dir = 'jobs'
output_dir = 'output'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over files in the jobs directory
for filename in os.listdir(jobs_dir):
    # Check if the file is a Python file
    if filename.endswith('.py'):
        # Generate output filename
        output_filename = os.path.splitext(filename)[0] + '.txt'
        output_path = os.path.join(output_dir, output_filename)

        # Run the Python file and capture the output
        process = subprocess.run(['python3', os.path.join(jobs_dir, filename)], capture_output=True, text=True)
        output = process.stdout.strip()

        # Write the output to a file
        with open(output_path, 'w') as f:
            f.write(output)

        print(f'Successfully executed {filename} and saved output to {output_path}')

import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
        try:
            working_dir_abs = os.path.abspath(working_directory)

            target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

            # Will be True or False
            valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

            if not valid_target_dir:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
            if not os.path.isfile(target_dir):
                return f'Error: "{file_path}" does not exist or is not a regular file'
            
            if not file_path.endswith('.py'):
                 return f'Error: "{file_path}" is not a Python file'
            
            command = ["python", target_dir]
            command.extend(args)

            process = subprocess.run(args=command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

            output_string = ''

            if process.returncode != 0:
                output_string = output_string + f"Process exited with code {process.returncode}"
            
            if len(process.stderr) and len(process.stdout):
                 output_string = output_string + "No output produced"

            output_string = output_string + f"STDOUT: {process.stdout}\n" + f"STDERR:{process.stderr}"
                 

            return output_string
            
        except Exception as e:
             return f"Error: executing Python file: {e}"
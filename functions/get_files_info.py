import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status. This does not run python files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        }
    ),
)

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)

    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs


    if directory == ".":
        header = "Result for current directory:\n"
    else:
        header = f"Result for '{working_directory}' directory:\n"

    if not valid_target_dir:
        return header + f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return header + f'    Error: "{target_dir}" is not a directory'
    
    message = header
    
    for item in os.listdir(target_dir):
        full_path = "/".join([target_dir, item])
        is_dir = True
        if os.path.isfile(full_path):
            is_dir=False
        size = os.path.getsize(full_path)
        message = message + f"  - {item}: file_size={size} bytes, is_dir={is_dir}\n"
    
    return message
        


    


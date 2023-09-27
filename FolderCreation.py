import os
import shutil

# Define the input and output folder paths


def createOutputFolder(input_folder : str = "Universidades", output_Folder : str = "Corpus", doCopy : bool = True):

    input_folder = input_folder
    output_folder = output_Folder

    # Ensure the output folder exists or create it if it doesn't
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of files in the input folder
    files = os.listdir(input_folder)

    # Loop through the files in the input folder
    for file in files:
        # Construct the full path of the input file
        input_file_path = os.path.join(input_folder, file)

        # Check if the item is a file (not a subdirectory)
        if os.path.isfile(input_file_path):
            # Create a folder with the same name as the file (without extension)
            folder_name = os.path.splitext(file)[0]
            folder_path = os.path.join(output_folder, folder_name)

            # Ensure the folder doesn't already exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            if doCopy:
                # Copy the file to the newly created folder
                shutil.copy(input_file_path, folder_path)

    print("Folders created and files copied successfully.")
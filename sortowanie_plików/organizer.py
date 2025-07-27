import os
import shutil


FILE_TYPES = {
    'images': ['.jpg', '.jpeg', '.png', '.gif'],
    'documents': ['.pdf', '.docx', '.txt'],
    'videos': ['.mp4', '.avi', '.mov'],
    'audio': ['.mp3', '.wav', '.aac'],
    'archives': ['.zip', '.rar', '.tar'],
}

def get_destination_folder(file_extension):
    for folder, extensions in FILE_TYPES.items():
        if file_extension.lower() in extensions:
            return folder
    return 'others'

def organize_files(source_directory):
    if not os.path.isdir(source_directory):
        print(f"The directory {source_directory} does not exist or is not a directory.")
        return

    for filename in os.listdir(source_directory):
        if filename == os.path.basename(__file__):
            continue

        source_path = os.path.join(source_directory, filename)

        if os.path.isfile(source_path):
            _, file_extension = os.path.splitext(filename)
            destination_folder_name = get_destination_folder(file_extension)
            
            destination_folder_path = os.path.join(source_directory, destination_folder_name)
            
            os.makedirs(destination_folder_path, exist_ok=True)
            
            shutil.move(source_path, os.path.join(destination_folder_path, filename))
            print(f"Moved {filename} to {destination_folder_name}")

if __name__ == "__main__":
    source_folder_path = os.path.dirname(os.path.abspath(__file__))
    organize_files(source_folder_path)





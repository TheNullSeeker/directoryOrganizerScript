import os
import shutil

# Define the mapping of file extensions to folder names
EXTENSION_FOLDERS = {
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.odt', '.rtf'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.flv'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z'],
    'Scripts': ['.py', '.js', '.sh', '.bat'],
    'Spreadsheets': ['.xls', '.xlsx', '.ods', '.csv'],
    'Presentations': ['.ppt', '.pptx', '.odp']
}

def organize_files(directory):
    try:
        # Ensure the directory exists
        if not os.path.isdir(directory):
            print(f"Error: {directory} is not a valid directory.")
            return
        
        # Create folders if they don't exist
        for folder in EXTENSION_FOLDERS.keys():
            folder_path = os.path.join(directory, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        
        # Move files to appropriate folders
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                moved = False
                for folder, extensions in EXTENSION_FOLDERS.items():
                    if any(filename.lower().endswith(ext) for ext in extensions):
                        shutil.move(file_path, os.path.join(directory, folder, filename))
                        moved = True
                        break
                
                # If file doesn't match any category, leave it in place or move to 'Others'
                if not moved:
                    others_path = os.path.join(directory, 'Others')
                    if not os.path.exists(others_path):
                        os.makedirs(others_path)
                    shutil.move(file_path, os.path.join(others_path, filename))
        
        print(f"Files in {directory} have been organized.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Prompt the user for the directory path
    user_directory = input("Enter the path of the directory you want to organize: ").strip()
    organize_files(user_directory)

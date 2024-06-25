import os
import shutil

# Define the default mapping of file extensions to folder names
DEFAULT_EXTENSION_FOLDERS = {
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.odt', '.rtf'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.flv'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z'],
    'Scripts': ['.py', '.js', '.sh', '.bat'],
    'Spreadsheets': ['.xls', '.xlsx', '.ods', '.csv'],
    'Presentations': ['.ppt', '.pptx', '.odp']
}

# Initialize the extension folders with the default values
EXTENSION_FOLDERS = DEFAULT_EXTENSION_FOLDERS.copy()

def organize_files(directory, exclude_formats=None):
    if exclude_formats is None:
        exclude_formats = []

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
                if any(filename.lower().endswith(ext) for ext in exclude_formats):
                    continue
                
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
        print("Thank you for using File Organizer Script.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def create_custom_category():
    while True:
        folder_name = input("Enter the folder name (or * to go back): ").strip()
        if folder_name == "*":
            return
        
        extensions = input("Enter file extensions (separated by commas): ").strip().lower().split(',')
        if not extensions:
            print("Error: No extensions entered. Please enter at least one extension.")
            continue
        
        EXTENSION_FOLDERS[folder_name] = [ext.strip() for ext in extensions]
        print(f"Category '{folder_name}' with extensions {extensions} has been successfully added.")
        return

def exclude_file_formats():
    exclude_formats = input("Enter file formats to exclude (separated by commas): ").strip().lower().split(',')
    exclude_formats = [ext.strip() for ext in exclude_formats]
    
    confirmation = input(f"Exclude the following file formats: {exclude_formats}? (yes/no): ").strip().lower()
    if confirmation == "yes":
        return exclude_formats
    return []

def edit_existing_category():
    while True:
        print("\nExisting Categories:")
        for i, folder in enumerate(EXTENSION_FOLDERS.keys(), 1):
            print(f"{i}. {folder}")
        
        folder_choice = input("Select a folder to edit by number (or * to go back, or # for home): ").strip()
        if folder_choice == "*" or folder_choice == "#":
            return
        
        try:
            folder_choice = int(folder_choice)
            folder_name = list(EXTENSION_FOLDERS.keys())[folder_choice - 1]
        except (ValueError, IndexError):
            print("Invalid choice. Please select a valid number.")
            continue
        
        while True:
            print(f"\nEditing Category: {folder_name}")
            print(f"Current extensions: {EXTENSION_FOLDERS[folder_name]}")
            print("1. Add new file formats")
            print("2. Edit existing file formats")
            print("3. Remove file formats")
            print("4. Rename folder")
            print("5. Go back")
            print("6. Home")
            
            edit_choice = input("Enter your choice: ").strip()
            
            if edit_choice == "1":
                new_formats = input("Enter new file formats (separated by commas): ").strip().lower().split(',')
                EXTENSION_FOLDERS[folder_name].extend([ext.strip() for ext in new_formats])
                print(f"New formats added: {new_formats}")
            elif edit_choice == "2":
                existing_formats = input("Enter the file formats to replace (separated by commas): ").strip().lower().split(',')
                new_formats = input("Enter new file formats (separated by commas): ").strip().lower().split(',')
                EXTENSION_FOLDERS[folder_name] = [new_format.strip() if ext in existing_formats else ext for ext in EXTENSION_FOLDERS[folder_name]]
                print(f"Formats updated to: {EXTENSION_FOLDERS[folder_name]}")
            elif edit_choice == "3":
                remove_formats = input("Enter file formats to remove (separated by commas): ").strip().lower().split(',')
                EXTENSION_FOLDERS[folder_name] = [ext for ext in EXTENSION_FOLDERS[folder_name] if ext not in remove_formats]
                print(f"Formats after removal: {EXTENSION_FOLDERS[folder_name]}")
            elif edit_choice == "4":
                new_folder_name = input("Enter new folder name: ").strip()
                EXTENSION_FOLDERS[new_folder_name] = EXTENSION_FOLDERS.pop(folder_name)
                folder_name = new_folder_name
                print(f"Folder renamed to: {folder_name}")
            elif edit_choice == "5":
                break
            elif edit_choice == "6":
                return
            else:
                print("Invalid choice. Please select a valid option.")

def restore_defaults():
    confirmation = input("This will remove all custom sub-directory configurations and restore to default settings. Do you wish to proceed? (yes/no): ").strip().lower()
    if confirmation == "yes":
        global EXTENSION_FOLDERS
        EXTENSION_FOLDERS = DEFAULT_EXTENSION_FOLDERS.copy()
        print("All configurations have been restored to default settings.")

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Start the script")
        print("2. Create custom category")
        print("3. Exclude specified file formats")
        print("4. Edit existing sub-directory configs")
        print("5. Restore to default settings")
        print("6. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            user_directory = input("Enter the path of the directory you want to organize: ").strip()
            organize_files(user_directory)
        elif choice == "2":
            create_custom_category()
        elif choice == "3":
            exclude_formats = exclude_file_formats()
            user_directory = input("Enter the path of the directory you want to organize: ").strip()
            organize_files(user_directory, exclude_formats)
        elif choice == "4":
            edit_existing_category()
        elif choice == "5":
            restore_defaults()
        elif choice == "6":
            print("Exiting the script. Thank you for using File Organizer Script!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main_menu()


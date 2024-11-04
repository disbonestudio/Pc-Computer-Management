import os
import shutil
import customtkinter as ctk

class DeleteFilesAndDirectories:
    def __init__(self, directory_paths, success_label):
        self.directory_paths = directory_paths
        self.success_label = success_label

    def delete(self):
        success_messages = []
        for directory_path in self.directory_paths:
            try:
                if os.path.exists(directory_path):
                    self.delete_directory_contents(directory_path)
                    success_messages.append(f"All accessible files and directories in {directory_path} deleted successfully.")
                else:
                    success_messages.append(f"Directory {directory_path} does not exist.")
            except OSError as e:
                success_messages.append(f"Error occurred while processing directory {directory_path}: {e}")

        if self.success_label:
            self.success_label.config(text='\n'.join(success_messages), text_color='green')

    def delete_directory_contents(self, directory_path):
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
            except (PermissionError, OSError) as e:
                # Handle errors as needed (optional)
                pass

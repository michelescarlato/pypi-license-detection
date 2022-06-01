import shutil
import os

class CreateDirectories:

    @staticmethod
    # Check whether the specified path exists or not
    def DirectoryCheck(cg_path, scg_path):
        dirs_to_check = [cg_path,scg_path]

        for directory in dirs_to_check:
            isdir = os.path.isdir(directory)
            if isdir is True:
                shutil.rmtree(directory)
                print("The directory '" + directory + "' deleted.")
                os.makedirs(directory)
                print("The directory '"+directory+"' has been created.")
            if isdir is False:
                os.makedirs(directory)
                print("The directory '" + directory + "' has been created.")
        return

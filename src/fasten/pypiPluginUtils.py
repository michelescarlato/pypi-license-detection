import os

class PypiPluginUtils:

    @staticmethod
    # Check whether the specified path exists or not
    def DirectoryCheck(fasten_data, scg_path):
        dirs_to_check = [fasten_data,scg_path]

        for element in dirs_to_check:
            isExist = os.path.exists(element)
            if not isExist:
              os.makedirs(element)
              print("The "+element+" directory is created!")
        return
import os

class CreateDirectory:

    @staticmethod
    # Check whether the specified path exists or not
    def createDirectory(directory):

        isExist = os.path.exists(directory)
        if not isExist:
            os.makedirs(directory)
#          print(f"The directory '{directory}' was not existent and has been created!")

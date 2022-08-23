import os

def file_exist(file_to_check):
    file_exists = os.path.exists(file_to_check)

    if file_exists:
        if os.stat(file_to_check).st_size > 0:
            return True
        else:
            return False
    else:
        return False
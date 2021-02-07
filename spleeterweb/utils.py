import os
import shutil
import time


def remove_temp_dirs(parent_dir, age):
    """
    Arguments
        parent_dir: Directory containing the temp directories to be removed.
                    parent_dir itself *will not* be removed.
        age:        Age of directory in seconds.

    Returns
        None
    """
    for dir in os.listdir(parent_dir):
        dir_path = os.path.join(parent_dir, dir)
        ctime = os.stat(dir_path).st_ctime
        if time.time() - ctime > age:
            shutil.rmtree(dir_path)
            print(f"{dir_path} was older than {age} seconds, it has been removed.")

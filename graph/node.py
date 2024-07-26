class Node:
    def __init__(self, id : int = None, x : float = None, y : float = None) -> None:
        self.id = id
        self.x = x
        self.y = y

import sys
import os

# Add the new folder to the Python path
new_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'graph'))
if new_folder_path not in sys.path:
    sys.path.append(new_folder_path)
import numpy as np
from .node import *

class Link:
    def __init__(self, source: Node, destination: Node):
        self.source = source
        self.destination = destination
        self.distance = np.sqrt(pow((source.x-destination.x),2)+
                                pow((source.y-destination.y),2)) #them distribution random

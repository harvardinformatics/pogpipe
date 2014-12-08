import os
import sys
import shutil
import os.path
import logging

from Feature import Feature


"""  

"""

class FeatureSet(Feature):

    """Object that stores a group of Features with a common query"""

    def __init__(self,name):

        self.features = []


    def addFeature(self,feat):
        self.features.append(feat)



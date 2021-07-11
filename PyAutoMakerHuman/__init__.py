import os
import sys
from os.path import dirname

rootDir = dirname(__file__)
os.environ["FACE_MODEL_PATH"] = os.path.join(rootDir, "models")
sys.path.append(rootDir)

from face import *
from hand import *
from train import *
from utils import *

print("call!")
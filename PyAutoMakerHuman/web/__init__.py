import os
import platform
import fnmatch
import imutils
import numpy as np
import cv2
import PyAutoMakerHuman as pamh
from flask import Flask, request
from waitress import serve

def cerate_app():
    app = Flask(__name__)
    
    @app.route("/", methods = ["GET", "POST"])
    def index():
        return "index"

    return app
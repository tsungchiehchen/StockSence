from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import process
import json
from pathlib import Path
import zipfile
import sys
import gdown

app = Flask(__name__)
CORS(app)


@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello World</p>"


@app.route("/fetchExample", methods=["GET", "POST"])
@cross_origin()
def fetchExample():
    print("fetch")
    # titlesFile = open(titlesPath, "r")
    # publishTimeFile = open(publishTimePath, "r")

    # titlesJson = json.load(titlesFile)
    # publishTimeJson = json.load(publishTimeFile)

    # resp = jsonify(titles=titlesJson, publishTime=publishTimeJson)

    # return resp

if __name__ == "__main__":
    app.run(port=3100)

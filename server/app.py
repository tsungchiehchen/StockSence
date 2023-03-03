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
    titlesFile = open(titlesPath, "r")
    publishTimeFile = open(publishTimePath, "r")

    titlesJson = json.load(titlesFile)
    publishTimeJson = json.load(publishTimeFile)

    resp = jsonify(titles=titlesJson, publishTime=publishTimeJson)

    return resp


if __name__ == "__main__":
    zippedDatasetPath = Path("../server/data/COVID-19.csv.zip")
    datasetPath = Path("../server/data/COVID-19.csv")

    if not zippedDatasetPath.is_file():
        # Download Kaggle COVID-19 dataset manually as it is too large for GitHub
        print('Download Kaggle COVID-19 dataset manually as it is too large for GitHub', file=sys.stderr)
        gdown.download("https://drive.google.com/uc?export=download&id=1KtZd3LPHocxBcwZFTOoKpqXXXzzA66yd",
                       "../server/data/COVID-19.csv.zip", quiet=False)

    if not datasetPath.is_file():
        print('Dataset unzipping', file=sys.stderr)
        with zipfile.ZipFile("../server/data/COVID-19.csv.zip", "r") as zip_ref:
            zip_ref.extractall("../server/data")

    titlesPath = Path("../server/data/titles.json")
    publishTimePath = Path("../server/data/publishTime.json")

    if not titlesPath.is_file() or not publishTimePath.is_file():
        print('Start processing data', file=sys.stderr)
        process(str(titlesPath), str(publishTimePath))

    print('Data processing complete, please load the page', file=sys.stderr)
    app.run(port=3100)

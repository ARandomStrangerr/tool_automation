from pdfminer.high_level import extract_text
from keras_preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
from sklearn_crfsuite import CRF
import os
import json

commonSuffix = {"inc", "llc", "tld"}


def getPdfFiles(folder):
    path: list[str] = [];
    for fileName in os.listdir(folder):
        if fileName.split(".")[-1] == "pdf":
            path.append(folder + fileName);
    return path;

def readPdfFiles(paths: list[str]):
    text: list[str] = []
    i = 0
    while i < len(paths):
        try:
            text.append(extract_text(paths[i]));
            i += 1;
        except:
            paths.remove(paths[i]);
            continue;
    return [text, paths];

def createWordDictionary(textList: list[str]):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(textList)
    return tokenizer

def addFeatureToText(text, tokenizer: Tokenizer):
    tokenWithFeature = []
    tokens = tokenizer.texts_to_sequences(text)[0];
    tokenLen = len(tokens)
    index = 0
    txt = ""
    while index < tokenLen:
        wordToken: str = tokenizer.index_word[tokens[index]]
        txt += " " + wordToken;
        singleTokenWithFeature = {
            "token": wordToken,
            "isNumber": wordToken.isnumeric(),
            "relativePos": index / tokenLen,
            "isCommonSuffix": 1 if wordToken in commonSuffix else 0,
        }
        tokenWithFeature.append(singleTokenWithFeature)
        index += 1
    print (txt);
    return tokenWithFeature


def makeImportJsonForLabelStudio(filePath: str, text, tokenizer: Tokenizer):
    tokens = tokenizer.texts_to_sequences([text])[0]
    fileName = filePath.split("/")[-1]
    fileName = fileName.split(".")[0]
    text = ""
    result = []
    position = 1
    for token in tokens:
        txt = tokenizer.index_word[token]
        result.append(
            {
                "value": {
                    "start": position,
                    "end": position + len(txt),
                    "text": txt,
                    "label": ["O"],
                },
                "from_name": "label",
                "to_name": "text",
                "type": "labels",
            }
        )
        text += " " + txt
        position += len(txt) + 1
    jsonData = [{"data": {"text": text}, "annotations": [{"result": result}]}]
    with open("./" + fileName + ".json", "w") as f:
        json.dump(jsonData, f, indent=4)

def prepDataWithLabelToTrain(annotatedJsonPath):
    with open(annotatedJsonPath, "r") as f:
        annotatedData = json.load(f)
    x = []
    y = []
    for data in annotatedData:
        tokenFeature = []
        tokenLabel = []
        strLen = len(data["data"]["text"])
        results = data["annotations"][0]["result"]
        for result in results:
            token = result["value"]["text"]
            try:
                label = result["value"]["labels"][0]
            except:
                label = "O"
            start = result["value"]["start"] - 1
            eachTokenFeature = {
                "token": token,
                "isNumber": token.isnumeric(),
                "relativePos": start / strLen,
                "isCommonSuffix": token in commonSuffix,
            }
            tokenFeature.append(eachTokenFeature)
            tokenLabel.append(label)
        x.append(tokenFeature)
        y.append(tokenLabel)
    return x, y


def trainCRFModel(x, y, testSize, randomSeed):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=testSize, random_state=randomSeed);
    crf = CRF(algorithm="lbfgs", c1= 0.01, c2= 0.001, max_iterations=100, all_possible_transitions=True);
    crf.fit(x, y);
    return crf;

def main():
    files = getPdfFiles("./");
    data, files = readPdfFiles(files);
    tokenizer = createWordDictionary(data);
    data = addFeatureToText(data, tokenizer);
    x, y = prepDataWithLabelToTrain("./annotated.json");
    crf = trainCRFModel(x, y, 0.2, 42);

    yPredict = crf.predict([data])[0];
    print(yPredict);
    i = 0;
    while i < len(yPredict):
        if yPredict[i] != 'O':
            print(data[i]);
        i+=1;

main();

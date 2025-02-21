import os;
from pdfminer.high_level import extract_text;
import re;
import json;
from sklearn_crfsuite import CRF;

def getPdfFilePath(folder:str) -> list[str]:
    path: list[str] = [];
    for fileName in os.listdir(folder):
        if fileName.split(".")[-1] == "pdf":
            path.append(folder + fileName);
    return path;

def readPdfFiles(paths:list[str]) -> tuple[list[str], list[str]]:
    texts: list[str] = [];
    i = 0;
    while i<len(paths):
        try:
            texts.append(extract_text(paths[i]));
            i += 1;
        except Exception:
            paths.remove(paths[i]);
    return paths, texts;

def tokenizeText(texts) -> list[list[str]]:
    tokenList:list[list[str]] = [];
    for text in texts:
        # clean up text
        text: str = re.sub(r"\s+", " ", text);
        text: str = text.strip();
        # split text into tokens
        tokenList.append(re.findall(r"[\w]+|[^\s\w]", text));
    return tokenList;

def changeTokenToDict(tokenList: list[list[str]]):
    dictList = [];
    for tokens in tokenList:
        dictionary = [];
        for token in tokens:
            dictionary.append({'text': token});
        dictList.append(dictionary);
    return dictList;

def addCompanyContextToToken(documentList: list[list[dict]]) -> list[list[dict]]:
    commonSufixies = ["ltd", "inc", "corp"];
    for document in documentList:
        i = 0;
        for i in range(len(document)):
            token = document[i];
            text: str = token["text"];
            token["relativePos"] = i/len(document);
            token["isNumeric"] = text.isnumeric();
            token["isCapitalize"] = text[0].isupper();
            token["isCommonSufix"] = text.lower() in commonSufixies;
            token["isWord"] = text.isalpha();
    return documentList;

def addMoneyContextToToken(documentList: list[list[dict]]) -> list[list[dict]]:
    commonSufixies: list[str] = ["total"];
    for document in documentList:
        i = 0;
        for i in range(len(document)):
            token = document[i];
            text: str = token["text"];
            token["relativePos"] = i / len(document);
            token["isNumeric"] = text.isnumeric();
            token["isCommonSufix"] = text.lower() in commonSufixies;

    return documentList;

def exportJsonToLabelStudio(paths: list[str], tokenList: list[list[str]]):
    i = 0;
    for i in range(len(paths)):
        fileName = paths[i].split("/")[-1].split(".")[0];
        text = "";
        tokens = tokenList[i];
        position = 0;
        result = [];
        for token in tokens:
            text += " " + token;
            result.append({
                "type": "labels",
                "from_name": "label",
                "to_name": "text",
                "value": {
                    "start": position,
                    "end": position + len(token),
                    "text": token,
                    "label": ["O"]
                }
            });
            position += len(token) + 1;
        jsonData = [{
            "data": {"text": text.strip()},
            "annotations": [{
                "result": result
            }]
        }];
        with open("./json/"+fileName+".json", "w") as f:
            json.dump(jsonData, f, indent = 4);
    return;

def importAndSplitLabelData(path):
    with open(path, "r") as f:
        jsonImport = json.load(f);
    x: list[list[dict]] = [];
    y: list[list[str]] = [];
    for data in jsonImport:
        thisDoccumentX: list[dict] = [];
        thisDoccumentY: list[str] = [];
        for token in data["label"]:
            thisDoccumentX.append({"text": token["text"]});
            try:
                thisDoccumentY.append(token["labels"][0]);
            except:
                thisDoccumentY.append("O");
        x.append(thisDoccumentX);
        y.append(thisDoccumentY);
    return x,y;

def oversamplingData(x: list[list[dict]], y: list[list[str]], multiplication: int = 2) -> tuple[list[list[dict]], list[list[str]]]:
    for tokens, labels in zip(x,y):
        for i, label in enumerate(labels):
            if label == "B-COMPANY":
                end = i;
                while (labels[end + 1] == "I-COMPANY"):
                    end += 1;
                start = i;
                while (start > 0 and i - start < 10):
                    start -= 1;
                oversampleX: list[dict] = [];
                oversampleY: list[str] = [];
                for j in range(start, end + 1, 1):
                    oversampleX.append(tokens[j]);
                    oversampleY.append(labels[j]);
                print(oversampleX);
                for j in range(multiplication - 1):
                    tokens[start:start] = oversampleX;
                    labels[start:start] = oversampleY;
                break;
    return x, y;

def trainModel(x,y):
    crf = CRF(algorithm="lbfgs", c1 = 0.1, c2 = 0.01, max_iterations = 100, all_possible_transitions=True);
    crf.fit(x,y);
    return crf;

def labelTrainingData():
    paths = getPdfFilePath("./invoices/");
    paths, texts = readPdfFiles(paths);
    tokenList = tokenizeText(texts);
    exportJsonToLabelStudio(paths, tokenList);
    return;

def trainData():
    x,y = importAndSplitLabelData("./TrainData.json");
#    x,y = oversamplingData(x,y);
    x = addCompanyContextToToken(x);
    model = trainModel(x,y);
    paths = ["./Culligan Water Inv#3021896.pdf"];
    paths, texts = readPdfFiles(paths);
    print(texts);
    tokenList = tokenizeText(texts);
    tokenList = changeTokenToDict(tokenList);
    predictX = addCompanyContextToToken(tokenList);
    predictions = model.predict(predictX)[0];
    print(predictions);
    for i in range(len(predictions)):
        if predictions[i] != "O":
            print(tokenList[0][i]);
    return;

trainData();

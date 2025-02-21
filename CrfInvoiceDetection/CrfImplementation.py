from pdfminer.high_level import extract_text;
from sklearn_crfsuite import CRF;
import re;
import os;
import json

# group 1: transfer data into file ready for label-studio
# step 1: transfer text to token from .pdf file
def tokenizeText(pathName:str) -> list[str]:
    text = extract_text(pathName);
    text = re.sub(r"\s+", ' ', text); # remove all \n
    text = re.sub(r'[^\w\s]', '', text); # remove symbols
    text = text.strip(); # removes space at 2 ends
    tokens = text.split(' '); # split into tokens
    return tokens;

# step 2: transfer list of token to .json file ready for label-studio
def formatTokenForLabelStudio(tokens: list[str]) -> list[dict[str, str|int]]:
    dataText = "";
    result: list[dict[str, str | dict]] = [];
    for token in tokens:
        result.append({
            "type": "labels",
            "from_name": "label",
            "to_name": "text",
            "value": {
                "start": len(dataText) + 1,
                "end": len(dataText) + 1 + len(token),
                "text": token,
                "label": ["O"]
            }
        });
        dataText+= " " + token;
    labelStudioToken = [{
        "data": {"text": dataText},
        "annotations": [{"result": result}]
    }];
    return labelStudioToken;

def Group1():
    invoiceFolder = "./invoices";
    invoiceName = os.listdir(invoiceFolder);
    for name in invoiceName:
        # read the content of the invoice
        try:
            tokenList = tokenizeText(f'{invoiceFolder}/{name}');
        except:
            continue;
        # format to export
        dataReady = formatTokenForLabelStudio(tokenList);
        # export
        with open("./json/" + name.split(".")[0] + ".json", "w") as f:
            json.dump(dataReady, f);
    return;
    
# group 2: import data from label-studio and train
# given a list of string, add features of the token to it.
commonSufixies = ['ltd', 'corp', 'llc'];
def addContextToToken_CompanyName(tokens: list[str]):
    tokenWithContext: list[dict[str, str|int|float]] = [];
    for index, token in enumerate(tokens):
        tokenWithContext.append({
            'text': token,
            'relPos': index / len(tokens),
            'isWord': token.isalpha(),
            'isCapitalize': 1 if token[0].isupper() else 0,
            'isCommonSufix': 1 if token[0].lower() in commonSufixies else 0
        });
    return tokenWithContext;

# step 1: import .json exported from label-studio, separate into x-input and y-output
def addContextToTrainData_CompanyName(data):
    x = [];
    y:list[str] = [];
    for index, token in enumerate(data['label']):
        x.append({
            'text': token['text'],
            'relPos': index / len(data['label']),
            'isWord': token['text'].isalpha(),
            'isCapitalize': 1 if token['text'][0].isupper() else 0,
            'isCommonSufix': 1 if token['text'][0].lower() in commonSufixies else 0
        });
        try:
            y.append(token["labels"][0]);
        except:
            y.append("O");
    return x,y;

crfModel = None;
def trainModel(x, y):
    crfModel = CRF(algorithm='lbfgs', max_iterations=100, all_possible_transitions=True);
    crfModel.fit(x,y);
    return;

def Group2():
    # read from export file
    with open("./json/export.json", "r") as f:
        labeledInvoice = json.load(f);
    # separate traning set and label
    X = [];
    Y = [];
    for invoice in labeledInvoice:
        i=0;
        while i < len(invoice['label']):
            if len(invoice['label'][i]['text']) == 0:
                invoice['label'] = invoice['label'][:i] + invoice['label'][i+1:];
            else:
                i+=1;
        x, y = addContextToTrainData_CompanyName(invoice);
        X.append(x);
        Y.append(y);
    # train the data
    trainModel(X,Y);
    return;

#Group1();
Group2();

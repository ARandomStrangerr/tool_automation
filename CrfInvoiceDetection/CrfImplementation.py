from sklearn_crfsuite import CRF;
import re;

def addContextToTrainData(data):
    commonSufixies = ["ltd", "inc", "corp"];
    x = [];
    y = [];
    for label in data['label']:
        text = re.sub(r'[^\w\s]', '', label['text']);
        if len(text) == 0: 
            continue;
        x.append({
            'text': text,
            'relPos': label['start']/len(data),
            'isWord': text.isalpha(),
            'isCapitalize': label['text'][0].isupper(),
            'isCommonSufix': 1 if label['text'].lower() in commonSufixies else 0
        });
        try:
            y.append(label["labels"][0]);
        except:
            y.append("O");
    return x,y;

crf = None;
def trainModel(x, y):
    crf = CRF(algorithm='lbfgs', max_iterations=100, all_possible_transitions=True);
    crf.fit(x,y);
    return crf;

def predictData(x):
    if crf is None:
        raise RuntimeError("model has not been train / imported yet");
    yPredict = crf.predict(x);
    return yPredict;

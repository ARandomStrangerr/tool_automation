import CrfImplementation;
import PdfCleanup;
import LabelStudioPrep;
import json;
import os;

def exportToLabelStudio(invoiceFolderPath, jsonFolderPath):
    invoiceFilesName = os.listdir(invoiceFolderPath); # get all the files name within the folder
    for singleFileName in invoiceFilesName: # iterate through each file in the folder
        singleFilePath = invoiceFolderPath + singleFileName;
        try: # try to read and tokenize each file, the error can't come from regex.
            token = PdfCleanup.tokenizeText(singleFilePath);
        except:
            print(f'cannot read {singleFileName}');
            continue;
        tokenLabelStudioReady = LabelStudioPrep.formatTokenForLabelStudio(token); # format the token so it can be feed to label-studio
        with open(f'{jsonFolderPath}/{singleFileName.split("/")[-1].split(".")[0]}.json', 'w') as f:
             json.dump(tokenLabelStudioReady, f, indent=4);
    return;

def trainComanyName(jsonFilePath):
    with open(jsonFilePath, 'r') as f:
        jsons = json.load(f);
    print(CrfImplementation.addContextToTrainData(jsons[0]));
    
 

trainComanyName("./json/export.json");

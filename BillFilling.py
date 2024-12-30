from pdfminer.high_level import extract_text
import os;
import re;
import spacy

#regex of the fields will be import
regexPattern = {
        "totalAmount": r"(amount owing|amount due (?:\(cad\))*|total|invoice total)\:*\s*(?:CA)*\$*\s*([\d.,]+)"
    };
nlp = spacy.load("en_core_web_sm")

# read invoice which is already text
def readTxtInvoice(path:str): 
    text = extract_text(path);
    lines = [line.strip() for line in text.splitlines() if line.strip()];
    tokens = ' '.join(lines);
    return tokens;

# read invoice which is an image
def readImgInvoice(path):
    pass;

# get the mount of money from this invoice
def extractMoney(text):
    match = re.findall(regexPattern["totalAmount"], text, re.IGNORECASE);
    if match:
        return match[-1];
    return ['0','0'];

# get the name of the vendor from this invoice
def extractVendorName(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            return ent.text
    return None

# get all file's names within a folder
def getAllPdfFiles(path):
    allFiles:list = os.listdir(path);
    return allFiles;

def main():
    folderPath = "./invoices/";
    fileNames = getAllPdfFiles(folderPath);
    cleanedData = [];
    for fileName in fileNames:
        extractedData = {};
        extractedData["fileName"] = fileName;
        text = "";
        try:
            text = readTxtInvoice(folderPath + fileName);
        except Exception as e:
            print(e);
            continue;
        moneyValue = extractMoney(text);
        extractedData[moneyValue[0]] = moneyValue[1];
        vendorName = extractVendorName(text);
        extractedData["vendorName"] = vendorName;
        print(extractedData);
main();

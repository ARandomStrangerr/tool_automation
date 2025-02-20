from pdfminer.high_level import extract_text;
import re;

def tokenizeText(pathName:str):
    text = extract_text(pathName);
    text = re.sub(r"\s+", ' ', text);
    tokens = text.split(' ');
    return tokens;

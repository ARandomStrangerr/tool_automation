import pandas as pd;

def indexFile(path):
    m = {};
    file = pd.read_excel(path);
    for itr in file.iterrows():
        m[itr[1][1]] = itr[1][2];
    return m;

def compare(m1:dict[str, str], m2:dict[str,str]):
    index = 0;
    lst = list(m1.keys());
    while (index < len(lst)):
        if lst[index] in m2:
            m1.pop(lst[index], None);
            m2.pop(lst[index], None);
        index += 1;
    print(m1.keys());
    print();
    print(m2.keys());
    return;

def main():
    missionFile = indexFile("./Mission cost code.xlsx");
    whiteRockFile = indexFile("./White Rock cost code.xlsx");
    compare(missionFile, whiteRockFile);
main();

import pandas as ps;
df = ps.read_excel("./errorSpreadSheet.xlsx")

df['sum'] = df['debit'] + df['credit'];

df['sum'].to_csv('output.csv', index = False);

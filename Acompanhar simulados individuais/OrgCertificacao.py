import pandas as pd

data = {
    "Questão": list(range(1, 51)),
    "Sua Resposta": ["" for _ in range(50)],
    "Resposta Correta": ["" for _ in range(50)],
    "Acertou": ["=IF(B{}=C{},1,0)".format(i + 3, i + 3) for i in range(50)]
}

df = pd.DataFrame(data)
writer = pd.ExcelWriter("PL300_Training.xlsx", engine="xlsxwriter")

df.to_excel(writer, sheet_name="Respostas", index=False, startrow=1)

workbook = writer.book
worksheet = writer.sheets["Respostas"]

worksheet.write("A1", "Template de Treinamento PL-300")

worksheet.write("A53", "Total Acertos:")
worksheet.write("B53", "=SUM(D3:D52)")

worksheet.write("A54", "Porcentagem de Acertos:")
worksheet.write("B54", "=(B53/50)")

writer.close()

print("Arquivo 'PL300_Training.xlsx' gerado com sucesso!")

import pandas as pd


df = pd.read_excel("base-de-dados-infopen-2014.xlsx")

colunas_de_decisao = ["Invite: UF", "1.1. Estabelecimento originalmente destinado a pessoa privadas de liberdade do sexo:"]

df_filtrado = df[colunas_de_decisao]

df_filtrado.to_csv("unidades_filtradas.csv", index = False, encoding="utf-8")

print("Csv criado com sucesso")
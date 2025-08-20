import pandas as pd

#Carregando planilha
df = pd.read_excel("base-de-dados-infopen-2014.xlsx")

# Selecionando as colunas

coluna_estado_presidio = ["Invite: UF"]
coluna_sexo_do_presidio = ["1.1. Estabelecimento originalmente destinado a pessoa privadas de liberdade do sexo:"]

#tratamento especial (muitas colunas)
colunas_para_somar = ["1.3. Capacidade do estabelecimento: | vagas - presos provisórios | Masculino",
                      "1.3. Capacidade do estabelecimento: | vagas - presos provisórios | Feminino",
                      "1.3. Capacidade do estabelecimento: | vagas - regime fechado | Masculino",
                      "1.3. Capacidade do estabelecimento: | vagas - regime fechado | Feminino",
                      "1.3. Capacidade do estabelecimento: | vagas - regime semiaberto | Masculino",
                      "1.3. Capacidade do estabelecimento: | vagas - regime semiaberto | Feminino",
                      "1.3. Capacidade do estabelecimento: | vagas - regime aberto | Masculino",
                      "1.3. Capacidade do estabelecimento: | vagas - regime aberto | Feminino",
                      "1.3. Capacidade do estabelecimento: | vagas - Regime Disciplinar Diferenciado (RDD) | Masculino",
                      "1.3. Capacidade do estabelecimento: | vagas - Regime Disciplinar Diferenciado (RDD) | Feminino",
                      "1.3. Capacidade do estabelecimento: | vagas - Medidas de segurança de internação | Masculino",
                      "1.3. Capacidade do estabelecimento: | vagas - Medidas de segurança de internação | Feminino",
                      ]

coluna_capacidade_presidio = df[colunas_para_somar].sum(axis=1)

df_filtrado = [coluna_estado_presidio, coluna_sexo_do_presidio, coluna_capacidade_presidio]

#Transofrmando as colunas selecionadas em um 
df_filtrado.to_csv("unidades_filtradas.csv", index = False, encoding="utf-8")

print("Csv criado com sucesso")
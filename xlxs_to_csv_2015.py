import pandas as pd
import numpy as np

# --------------------------
# 1️⃣ Carregar planilha
# --------------------------
df = pd.read_excel("base-de-dados-infopen-2015.xlsx")

# --------------------------
# 2️⃣ Estado do presídio
# --------------------------
df["UF"] = df["UF:"].ffill().str.strip().str.lower()

# --------------------------
# 3️⃣ Sexo do estabelecimento
# --------------------------
df["Sexo"] = df[
    "1.1 Estabelecimento originalmente destinado a pessoas privadas de liberdade do sexo:"
].fillna("desconhecido").str.strip().str.lower()

# --------------------------
# 4️⃣ Capacidade total
# --------------------------
colunas_capacidade = [col for col in df.columns if col.startswith("1.3.1.")]
for col in colunas_capacidade:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df["Capacidade Total"] = df[colunas_capacidade].sum(axis=1, skipna=True)

# --------------------------
# 5️⃣ Tipo de gestão
# --------------------------
df["Tipo de Gestão"] = df["1.4. Gestão do estabelecimento:"].fillna("desconhecido") \
    .str.split("(", n=1).str[0].str.strip().str.lower()

# --------------------------
# 6️⃣ Concebido ou adaptado
# --------------------------
df["Concebido ou Adaptado"] = df[
    "1.7. O estabelecimento foi concebido como estabelecimento penal ou foi construído para outra utilização e foi adaptado?"
].fillna("desconhecido") \
    .str.lower() \
    .str.extract(r'(concebido|adaptado)', expand=False) \
    .fillna("desconhecido")

# --------------------------
# 7️⃣ Consultório médico
# --------------------------
df["Consultório Médico"] = df[
    "2.4.1. Módulo de saúde - Espaços mínimos | Consultório médico - O espaço está disponível no estabelecimento?"
].fillna("não").str.strip().str.lower().apply(lambda x: "sim" if x == "sim" else "não")

# --------------------------
# 8️⃣ Total de presos provisórios masculinos
# --------------------------
colunas_provisorios_masc = [
    "4.1.1.M. População prisional | presos provisórios | MASCULINO | Justiça Estadual",
    "4.1.1.M. População prisional | presos provisórios | MASCULINO | Justiça Federal",
    "4.1.1.M. População prisional | presos provisórios | MASCULINO | Outros (Justiça do Trabalho, Cível)"
]
df["Total Provisórios Masculinos"] = df[colunas_provisorios_masc].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)

# --------------------------
# 9️⃣ Total de presos provisórios femininos
# --------------------------
colunas_provisorios_fem = [
    "4.1.1.F. População prisional | presos provisórios | FEMININO | Justiça Estadual",
    "4.1.1.F. População prisional | presos provisórios | FEMININO | Justiça Federal",
    "4.1.1.F. População prisional | presos provisórios | FEMININO | Outros (Justiça do Trabalho, Cível)"
]
df["Total Provisórios Femininos"] = df[colunas_provisorios_fem].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)

# --------------------------
# 10️⃣ Total de presos sentenciados masculinos
# --------------------------
colunas_sentenciados_masc = [
    "4.1.2.M. População prisional | regime fechado | MASCULINO | Justiça Estadual",
    "4.1.2.M. População prisional | regime fechado | MASCULINO | Justiça Federal",
    "4.1.2.M. População prisional | regime fechado | MASCULINO | Outros (Justiça do Trabalho, Cível)",
    "4.1.3.M. População prisional | regime semiaberto | MASCULINO | Justiça Estadual",
    "4.1.3.M. População prisional | regime semiaberto | MASCULINO | Justiça Federal",
    "4.1.3.M. População prisional | regime semiaberto | MASCULINO | Outros (Justiça do Trabalho, Cível)",
    "4.1.4.M. População prisional | regime aberto | MASCULINO | Justiça Estadual",
    "4.1.4.M. População prisional | regime aberto | MASCULINO | Justiça Federal",
    "4.1.4.M. População prisional | regime aberto | MASCULINO | Outros (Justiça do Trabalho, Cível)"
]

# Filtra apenas colunas que existem no df
colunas_sentenciados_masc = [c for c in colunas_sentenciados_masc if c in df.columns]

df["Total Sentenciados Masculinos"] = df[colunas_sentenciados_masc] \
    .apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)

# --------------------------
# 11️⃣ Total de presos sentenciados femininos
# --------------------------
colunas_sentenciados_fem = [
    "4.1.2.F. População prisional | regime fechado | FEMININO | Justiça Estadual",
    "4.1.2.F. População prisional | regime fechado | FEMININO | Justiça Federal",
    "4.1.2.F. População prisional | regime fechado | FEMININO | Outros (Justiça do Trabalho, Cível)",
    "4.1.3.F. População prisional | regime semiaberto | FEMININO | Justiça Estadual",
    "4.1.3.F. População prisional | regime semiaberto | FEMININO | Justiça Federal",
    "4.1.3.F. População prisional | regime semiaberto | FEMININO | Outros (Justiça do Trabalho, Cível)",
    "4.1.4.F. População prisional | regime aberto | FEMININO | Justiça Estadual",
    "4.1.4.F. População prisional | regime aberto | FEMININO | Justiça Federal",
    "4.1.4.F. População prisional | regime aberto | FEMININO | Outros (Justiça do Trabalho, Cível)"
]

# Filtra apenas colunas que existem no df
colunas_sentenciados_fem = [c for c in colunas_sentenciados_fem if c in df.columns]

df["Total Sentenciados Femininos"] = df[colunas_sentenciados_fem] \
    .apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)
"""
# --------------------------
# 12️⃣ Colunas de raça e sexo
# --------------------------
colunas_raca_masculino = [
    "5.2.1.M. Cor de pele/raça/etnia | MASCULINO | Branca",
    "5.2.1.M. Cor de pele/raça/etnia | MASCULINO | Preta",
    "5.2.1.M. Cor de pele/raça/etnia | MASCULINO | Parda",
    "5.2.1.M. Cor de pele/raça/etnia | MASCULINO | Amarela",
    "5.2.1.M. Cor de pele/raça/etnia | MASCULINO | Indígena"
]

colunas_raca_feminino = [
    "5.2.1.F. Cor de pele/raça/etnia | FEMININO | Branca",
    "5.2.1.F. Cor de pele/raça/etnia | FEMININO | Preta",
    "5.2.1.F. Cor de pele/raça/etnia | FEMININO | Parda",
    "5.2.1.F. Cor de pele/raça/etnia | FEMININO | Amarela",
    "5.2.1.F. Cor de pele/raça/etnia | FEMININO | Indígena",
]

for col in colunas_raca_masculino:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].median())
for col in colunas_raca_feminino:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].median())

novos_nomes_masc = {col: col.split("|")[1].strip() + " Masculino" for col in colunas_raca_masculino}
novos_nomes_fem = {col: col.split("|")[1].strip() + " Feminino" for col in colunas_raca_feminino}
df.rename(columns={**novos_nomes_masc, **novos_nomes_fem}, inplace=True)

colunas_raca_masculino = list(novos_nomes_masc.values())
colunas_raca_feminino = list(novos_nomes_fem.values())
"""
"""
# --------------------------
# 13️⃣ Colunas de estado civil
# --------------------------
colunas_estado_civil_masc = [
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Swifiolteiro/a | Masculino",
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | União estável/ amasiado | Masculino",
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Casado/a | Masculino",
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Separado/a judicialmente | Masculino",
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Divorciado/a | Masculino",
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Viúvo/a | Masculino"
]

colunas_estado_civil_fem = [
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Solteiro/a | Feminino",
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | União estável/ amasiado | Feminino",
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Casado/a | Feminino",
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Separado/a judicialmente | Feminino",
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Divorciado/a | Feminino",
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Viúvo/a | Feminino"
]

for col in colunas_estado_civil_masc:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].median())
for col in colunas_estado_civil_fem:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].median())

novos_nomes_masc = {col: col.split("|")[1].strip() + " Masculino" for col in colunas_estado_civil_masc}
novos_nomes_fem = {col: col.split("|")[1].strip() + " Feminino" for col in colunas_estado_civil_fem}
df.rename(columns={**novos_nomes_masc, **novos_nomes_fem}, inplace=True)

colunas_estado_civil_masc = list(novos_nomes_masc.values())
colunas_estado_civil_fem = list(novos_nomes_fem.values())
"""

# Seleciona todas as colunas que começam com '5.3.M.'
colunas_estado_civil_masc = [
    col for col in df.columns 
    if col.startswith("5.3.M.") 
    and col != "5.3.M. Estado civil | MASCULINO | Estado civil não informado"
]
print(colunas_estado_civil_masc)

# --------------------------
# 18️⃣ Selecionar colunas finais
# --------------------------
final_df = df[
    [
        "UF","Sexo","Capacidade Total","Tipo de Gestão","Concebido ou Adaptado","Consultório Médico", "Total Provisórios Masculinos", "Total Provisórios Femininos", "Total Sentenciados Masculinos", "Total Sentenciados Femininos",
    ] 
    # + colunas_raca_masculino + colunas_raca_feminino

]


# --------------------------
# 19️⃣ Salvar CSV final
# --------------------------
final_df.to_csv("csv_2015", index=False)
print("CSV gerado com sucesso!")

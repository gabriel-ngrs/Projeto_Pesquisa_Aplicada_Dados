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
    "4.1.2.M. População prisional | regime fechado | MASCULINO | Justiça Estadual",
    "4.1.2.M. População prisional | regime fechado | MASCULINO | Justiça Federal",
    "4.1.2.M. População prisional | regime fechado | MASCULINO | Outros (Justiça do Trabalho, Cível)",
    "4.1.3.M. População prisional | regime semiaberto | MASCULINO | Justiça Estadual",
    "4.1.3.M. População prisional | regime semiaberto | MASCULINO | Justiça Federal",
    "4.1.3.M. População prisional | regime semiaberto | MASCULINO | Outros (Justiça do Trabalho, Cível)",
    "4.1.4.M. População prisional | regime aberto | MASCULINO | Justiça Estadual",
    "4.1.4.M. População prisional | regime aberto | MASCULINO | Justiça Federal",
    "4.1.4.M. População prisional | regime aberto    | MASCULINO | Outros (Justiça do Trabalho, Cível)"
]
df["Total Sentenciados Masculinos"] = df[colunas_sentenciados_masc].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)






















# --------------------------
# 18️⃣ Selecionar colunas finais
# --------------------------
final_df = df[
    [
        "UF","Sexo","Capacidade Total","Tipo de Gestão","Concebido ou Adaptado","Consultório Médico"
    ]
]


# --------------------------
# 19️⃣ Salvar CSV final
# --------------------------
final_df.to_csv("csv_2015", index=False)
print("CSV gerado com sucesso!")

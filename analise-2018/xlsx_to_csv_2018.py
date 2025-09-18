import pandas as pd
import numpy as np

# --------------------------
# 1️⃣ Carregar planilha
# --------------------------
df = pd.read_excel("C:\Programacao\Projeto Pesquisa Aplicada - Análise de Dados/analise-2018/5o-ciclo-base-de-dados-2018-2-semestre.xlsx")

# --------------------------
# 2️⃣ Estado do presídio
# --------------------------
df["UF"] = df["UF"].ffill().str.strip().str.lower()

# --------------------------
# 3️⃣ Sexo do estabelecimento
# --------------------------
df["Sexo"] = df[
    "1.1 Estabelecimento originalmente destinado a pessoa privadas de liberdade do sexo"
].fillna("desconhecido").str.strip().str.lower()

# --------------------------
# 4️⃣ Capacidade total
# --------------------------
colunas_capacidade = [col for col in df.columns if col.startswith("1.3") and col != "1.3 Capacidade do estabelecimento | Outro(s). Qual(is)?"]
for col in colunas_capacidade:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df["Capacidade Total"] = df[colunas_capacidade].sum(axis=1, skipna=True)

# --------------------------
# 5️⃣ Tipo de gestão
# --------------------------
df["Tipo de Gestão"] = df["1.4 Gestão do estabelecimento"].fillna("desconhecido") \
    .str.split("(", n=1).str[0].str.strip().str.lower()

# --------------------------
# 7️⃣ Consultório médico
# --------------------------
df["Consultório Médico"] = df[
    "2.4 Módulo de saúde | Consultório médico"
].fillna("não").str.strip().str.lower().apply(lambda x: "sim" if x == "sim" else "não")

# --------------------------
# 8️⃣ Total de presos provisórios masculinos
# --------------------------
colunas_provisorios_masc = [
    col for col in df.columns
    if col.startswith("4.1 População prisional | Presos provisórios") and col.endswith("Masculino")
]
df["Total Provisórios Masculinos"] = df[colunas_provisorios_masc].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)


# --------------------------
# 9️⃣ Total de presos provisórios femininos
# --------------------------
colunas_provisorios_fem = [
   col for col in df.columns
        if col.startswith("4.1 População prisional | Presos provisórios") and col.endswith("Feminino")
]
df["Total Provisórios Femininos"] = df[colunas_provisorios_fem].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)


# --------------------------
# 10️⃣ Total de presos sentenciados masculinos
# --------------------------
colunas_sentenciados_masc = [
    col for col in df.columns
        if col.startswith("4.1 População prisional | Presos sentenciados") and col.endswith("Masculino")
]

df["Total Sentenciados Masculinos"] = df[colunas_sentenciados_masc].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)


# --------------------------
# 11️⃣ Total de presos sentenciados femininos
# --------------------------
colunas_sentenciados_fem = [
    col for col in df.columns
        if col.startswith("4.1 População prisional | Presos sentenciados") and col.endswith("Feminino")
]

df["Total Sentenciados Femininos"] = df[colunas_sentenciados_fem].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)


# --------------------------
# 12️⃣ Colunas de raça e sexo
# --------------------------
colunas_raca_masculino = [col for col in df.columns if col.startswith("5.2") and col.endswith("Masculino")]
colunas_raca_feminino = [col for col in df.columns if col.startswith("5.2") and col.endswith("Feminino")]

novos_nomes_masc = {col: col.split("|")[2].strip() + " " + col.split("|")[1].strip() for col in colunas_raca_masculino}
novos_nomes_fem = {col: col.split("|")[2].strip() + " " + col.split("|")[1].strip() for col in colunas_raca_feminino}

df.rename(columns={**novos_nomes_masc, **novos_nomes_fem}, inplace=True)

colunas_raca_masculino = list(novos_nomes_masc.values())
colunas_raca_feminino = list(novos_nomes_fem.values())

for col in colunas_raca_masculino:
    col_num = pd.to_numeric(df[col], errors='coerce')
    df[col] = col_num.fillna(col_num.median())
    
for col in colunas_raca_feminino:
    col_num = pd.to_numeric(df[col], errors='coerce')
    df[col] = col_num.fillna(col_num.median())


# --------------------------
# 14️⃣ Colunas de idade
# --------------------------
colunas_idade_masc = [
    col for col in df.columns 
    if col.startswith("5.1 Quantidade de pessoas privadas de liberdade por faixa etária") 
    and col.endswith("Masculino")
]

colunas_idade_fem = [
    col for col in df.columns 
    if col.startswith("5.1 Quantidade de pessoas privadas de liberdade por faixa etária") 
    and col.endswith("Feminino")
]

novos_nomes_idade_masc = {}
for col in colunas_idade_masc:
    partes = col.split("|")
    if len(partes) == 3:
        faixa_etaria = partes[1].strip()
        sexo = partes[2].strip()
        novos_nomes_idade_masc[col] = f"{sexo} {faixa_etaria}"

novos_nomes_idade_fem = {}
for col in colunas_idade_fem:
    partes = col.split("|")
    if len(partes) == 3:
        faixa_etaria = partes[1].strip()
        sexo = partes[2].strip()
        novos_nomes_idade_fem[col] = f"{sexo} {faixa_etaria}"

df.rename(columns={**novos_nomes_idade_masc, **novos_nomes_idade_fem}, inplace=True)

colunas_idade_masc_renomeadas = list(novos_nomes_idade_masc.values())
colunas_idade_fem_renomeadas = list(novos_nomes_idade_fem.values())

for col in colunas_idade_masc_renomeadas:
    if col in df.columns:
        serie = df[col].apply(lambda x: str(x).replace(",", "."))
        df[col] = pd.to_numeric(serie, errors='coerce')
        df[col] = df[col].fillna(df[col].median())

for col in colunas_idade_fem_renomeadas:
    if col in df.columns:
        serie = df[col].apply(lambda x: str(x).replace(",", "."))
        df[col] = pd.to_numeric(serie, errors='coerce')
        df[col] = df[col].fillna(df[col].median())


# --------------------------
# 15️⃣ Criar coluna de presos totais
# --------------------------
df["Qtd_Presos"] = df["Total Provisórios Masculinos"] + df["Total Provisórios Femininos"] + df["Total Sentenciados Masculinos"] + df["Total Sentenciados Femininos"]


# --------------------------
# 16️⃣ Colunas de crimes
# --------------------------
np.random.seed(42)
crimes = ["Tráfico de Drogas", "Crimes Contra Patrimônio", "Crimes Contra a Vida"]

def distribuir_crimes(total):
    if total == 0:
        return [0]*len(crimes)
    proporcoes = np.random.dirichlet(np.ones(len(crimes)), size=1)[0]
    numeros = np.floor(proporcoes * total).astype(int)
    while numeros.sum() < total:
        idx = np.random.randint(0, len(crimes))
        numeros[idx] += 1
    while numeros.sum() > total:
        idx = np.random.randint(0, len(crimes))
        if numeros[idx] > 0:
            numeros[idx] -= 1
    return numeros

for crime in crimes:
    df[crime] = 0
df[crimes] = df["Qtd_Presos"].apply(lambda x: pd.Series(distribuir_crimes(x)))


# --------------------------
# 17️⃣ Coluna de reincidência criminal
# --------------------------
def gerar_reincidencia(total):
    if total == 0:
        return 0
    return np.random.randint(0, total)

df["Reincidencia Criminal"] = df["Qtd_Presos"].apply(gerar_reincidencia)


# --------------------------
# 18️⃣ Selecionar colunas finais
# --------------------------
final_df = df[
    [
        "UF", "Sexo", "Capacidade Total", "Tipo de Gestão", "Consultório Médico",
        "Total Provisórios Masculinos", "Total Provisórios Femininos", "Total Sentenciados Masculinos", "Total Sentenciados Femininos", "Qtd_Presos", "Reincidencia Criminal"
    ] + colunas_raca_masculino + colunas_raca_feminino
      + colunas_idade_masc_renomeadas + colunas_idade_fem_renomeadas

]

# --------------------------
# 19️⃣ Salvar CSV final
# --------------------------
final_df.to_csv("csv_2018", index=False)
print("CSV gerado com sucesso!")
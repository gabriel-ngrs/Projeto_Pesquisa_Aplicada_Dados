import pandas as pd
import numpy as np

# --------------------------
# 1️⃣ Carregar planilha
# --------------------------
df = pd.read_excel("base-de-dados-infopen-2014.xlsx")

# --------------------------
# 2️⃣ Estado do presídio
# --------------------------
df["UF"] = df["Invite: UF"].ffill().str.strip().str.lower()

# --------------------------
# 3️⃣ Sexo do estabelecimento
# --------------------------
df["Sexo"] = df[
    "1.1. Estabelecimento originalmente destinado a pessoa privadas de liberdade do sexo:"
].fillna("desconhecido").str.strip().str.lower()

# --------------------------
# 4️⃣ Capacidade total
# --------------------------
colunas_capacidade = [col for col in df.columns if col.startswith("1.3. C")]
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
    "2.4. Módulo de saúde: | Consultório médico | O espaço está disponível no estabelecimento?"
].fillna("não").str.strip().str.lower().apply(lambda x: "sim" if x == "sim" else "não")

# --------------------------
# 8️⃣ Total de presos provisórios masculinos
# --------------------------
colunas_provisorios_masc = [
    "[Q_4_1.0.0] 4.1. População prisional: | Presos provisórios (sem condenação)** | Justiça Estadual Masculino",
    "[Q_4_1.2.0] 4.1. População prisional: | Presos provisórios (sem condenação)** | Justiça Federal Masculino",
    "[Q_4_1.4.0] 4.1. População prisional: | Presos provisórios (sem condenação)** | Outros  (Justiça do Trabalho, Cível) Masculino"
]
df["Total Provisórios Masculinos"] = df[colunas_provisorios_masc].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)

# --------------------------
# 9️⃣ Total de presos provisórios femininos
# --------------------------
colunas_provisorios_fem = [
    "[Q_4_1.1.0] 4.1. População prisional: | Presos provisórios (sem condenação)** | Justiça Estadual Feminino",
    "[Q_4_1.3.0] 4.1. População prisional: | Presos provisórios (sem condenação)** | Justiça Federal Feminino",
    "[Q_4_1.5.0] 4.1. População prisional: | Presos provisórios (sem condenação)** | Outros  (Justiça do Trabalho, Cível) Feminino"
]
df["Total Provisórios Femininos"] = df[colunas_provisorios_fem].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)

# --------------------------
# 10️⃣ Total de presos sentenciados masculinos
# --------------------------
colunas_sentenciados_masc = [
    "[Q_4_1.0.1] 4.1. População prisional: | Presos sentenciados - regime fechado | Justiça Estadual Masculino",
    "[Q_4_1.2.1] 4.1. População prisional: | Presos sentenciados - regime fechado | Justiça Federal Masculino",
    "[Q_4_1.4.1] 4.1. População prisional: | Presos sentenciados - regime fechado | Outros  (Justiça do Trabalho, Cível) Masculino",
    "[Q_4_1.0.2] 4.1. População prisional: | Presos sentenciados - regime semiaberto | Justiça Estadual Masculino",
    "[Q_4_1.2.2] 4.1. População prisional: | Presos sentenciados - regime semiaberto | Justiça Federal Masculino",
    "[Q_4_1.4.2] 4.1. População prisional: | Presos sentenciados - regime semiaberto | Outros  (Justiça do Trabalho, Cível) Masculino",
    "[Q_4_1.0.3] 4.1. População prisional: | Presos sentenciados - regime aberto | Justiça Estadual Masculino",
    "[Q_4_1.2.3] 4.1. População prisional: | Presos sentenciados - regime aberto | Justiça Federal Masculino",
    "[Q_4_1.4.3] 4.1. População prisional: | Presos sentenciados - regime aberto | Outros  (Justiça do Trabalho, Cível) Masculino"
]
df["Total Sentenciados Masculinos"] = df[colunas_sentenciados_masc].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)

# --------------------------
# 11️⃣ Total de presos sentenciados femininos
# --------------------------
colunas_sentenciados_fem = [
    "[Q_4_1.1.1] 4.1. População prisional: | Presos sentenciados - regime fechado | Justiça Estadual Feminino",
    "[Q_4_1.3.1] 4.1. População prisional: | Presos sentenciados - regime fechado | Justiça Federal Feminino",
    "[Q_4_1.5.1] 4.1. População prisional: | Presos sentenciados - regime fechado | Outros  (Justiça do Trabalho, Cível) Feminino",
    "[Q_4_1.1.2] 4.1. População prisional: | Presos sentenciados - regime semiaberto | Justiça Estadual Feminino",
    "[Q_4_1.3.2] 4.1. População prisional: | Presos sentenciados - regime semiaberto | Justiça Federal Feminino",
    "[Q_4_1.5.2] 4.1. População prisional: | Presos sentenciados - regime semiaberto | Outros  (Justiça do Trabalho, Cível) Feminino",
    "[Q_4_1.1.3] 4.1. População prisional: | Presos sentenciados - regime aberto | Justiça Estadual Feminino",
    "[Q_4_1.3.3] 4.1. População prisional: | Presos sentenciados - regime aberto | Justiça Federal Feminino",
    "[Q_4_1.5.3] 4.1. População prisional: | Presos sentenciados - regime aberto | Outros  (Justiça do Trabalho, Cível) Feminino"
]
df["Total Sentenciados Femininos"] = df[colunas_sentenciados_fem].apply(pd.to_numeric, errors='coerce').fillna(0).sum(axis=1)

# --------------------------
# 12️⃣ Colunas de raça e sexo
# --------------------------
colunas_raca_masculino = [
    "5.2.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Branca | Masculino",
    "5.2.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Negra | Masculino",
    "5.2.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Parda | Masculino",
    "5.2.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Amarela | Masculino",
    "5.2.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Indígena | Masculino"
]

colunas_raca_feminino = [
    "5.2.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Branca | Feminino",
    "5.2.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Negra | Feminino",
    "5.2.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Parda | Feminino",
    "5.2.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Amarela | Feminino",
    "5.2.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Indígena | Feminino",
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

# --------------------------
# 13️⃣ Colunas de estado civil
# --------------------------
colunas_estado_civil_masc = [
    "5.3.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Solteiro/a | Masculino",
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

# --------------------------
# 14️⃣ Colunas de idade
# --------------------------
colunas_idade_masc = [
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | 18 a 24 anos | Masculino",
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | 25 a 29 anos | Masculino",
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | 30 a 34 anos | Masculino",
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | 35 a 45 anos | Masculino",
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | 46 a 60 anos | Masculino",
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | 61 a 70 anos | Masculino",
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Mais de 70 anos | Masculino"
]

colunas_idade_fem = [
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | 18 a 24 anos | Feminino",
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | 25 a 29 anos | Feminino",
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | 30 a 34 anos | Feminino",
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | 35 a 45 anos | Feminino",
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | 46 a 60 anos | Feminino",
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | 61 a 70 anos | Feminino",
    "5.1.a. Em caso positivo, total ou parcialmente, preencha as informações abaixo: | Mais de 70 anos | Feminino"
]

for col in colunas_idade_masc:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].median())
for col in colunas_idade_fem:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].median())

novos_nomes_masc = {col: col.split("|")[1].strip() + " Masculino" for col in colunas_idade_masc}
novos_nomes_fem = {col: col.split("|")[1].strip() + " Feminino" for col in colunas_idade_fem}
df.rename(columns={**novos_nomes_masc, **novos_nomes_fem}, inplace=True)

colunas_idade_masc = list(novos_nomes_masc.values())
colunas_idade_fem = list(novos_nomes_fem.values())

# --------------------------
# 15️⃣ Criar coluna de presos totais
# --------------------------
df["Qtd_Presos"] = df["Total Provisórios Masculinos"] + df["Total Provisórios Femininos"] + \
                   df["Total Sentenciados Masculinos"] + df["Total Sentenciados Femininos"]

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
        "UF", "Sexo", "Capacidade Total", "Tipo de Gestão",
        "Concebido ou Adaptado", "Consultório Médico",
        "Total Provisórios Masculinos", "Total Provisórios Femininos",
        "Total Sentenciados Masculinos", "Total Sentenciados Femininos",
        "Qtd_Presos", "Reincidencia Criminal"
    ]
    + crimes
    + colunas_raca_masculino + colunas_raca_feminino
    + colunas_idade_masc + colunas_idade_fem
    + colunas_estado_civil_masc + colunas_estado_civil_fem
]

# --------------------------
# 19️⃣ Salvar CSV final
# --------------------------
final_df.to_csv("csv_2014", index=False)
print("CSV gerado com sucesso!")

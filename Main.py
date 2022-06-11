# pip install pandas
# pip install numpy
# pip install plotly

import numpy as np
import pandas as pd
import plotly.express as px

# Ler o arquivo txt e praparar o dataframe
df = pd.read_fwf('usuarios.txt', names=["Usuário", "   Espaço utilizado"]) # Ler o arquivo e nomear as colunas
df.index = np.arange(1, len(df) + 1) # Iniciar o index das linhas com 1 em vez de 0
df.index.name = 'Nr.' # Nome do Index
df.columns.name = df.index.name # Alinha o index.name
df.index.name = None # Alinha o index.name
df["  % do uso"] = " " # Cria coluna '% do uso'
df["   Espaço utilizado"] = pd.to_numeric(df["   Espaço utilizado"], errors="coerce") # Converte para numerico
df["  % do uso"] = pd.to_numeric(df["  % do uso"], errors="coerce") # Converte para numerico

# function para converter de bytes para MegaBytes (1 mb = 1048576 bytes ou 2^20)
df['   Espaço utilizado'] = df['   Espaço utilizado'].map(lambda bytes: bytes/1048576)

# function para calcular Espaço total ocupado
totalOcupado = df['   Espaço utilizado'].sum(axis=0)

# function para calcular porcentagem
df["  % do uso"] = df['   Espaço utilizado'].map(lambda porcentagem: porcentagem/totalOcupado)

# function para calcular Espaço médio ocupado
mediaOcupado = df['   Espaço utilizado'].mean(axis=0)

# Ordenar os usuários pelo percentual de espaço ocupado
df = df.sort_values(by="   Espaço utilizado", ascending=True)

# Gerar a saída numa página html
# Mostrar apenas os n primeiros em uso definido pelo usuário
fig = px.pie(df, values='   Espaço utilizado', names='Usuário', title='Relatório: Espaço utilizado por cada usuário', hover_data=['   Espaço utilizado'])
fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=20)
fig.show()

# format das colunas
df['   Espaço utilizado'] = df['   Espaço utilizado'].map("{0:.2f}".format) + " MB"
df["  % do uso"] = df["  % do uso"].map("{:.2%}".format)

# Reordena o arquivo pelo index (voltar ao estado original)
df = df.sort_index()

# Cria e passa o dataframe para o aquirvo relatório.txt
arquivo = open('relatório.txt', 'a')
arquivo.write("ACME Inc.           Uso do espaço em disco pelos usuários\n")
arquivo.write("---------------------------------------------------------\n\n")
arquivo.write(df.to_string())
arquivo.write("\n\nEspaço total ocupado: " + "{0:.2f}".format(totalOcupado) + "MB")
arquivo.write("\nEspaço médio ocupado: " + "{0:.2f}".format(mediaOcupado) + "MB")
arquivo.close()

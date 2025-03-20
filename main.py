#Leitura e Inspeção Inicial dos Dados
import pandas as pd 

#Análise Exploratória de Dados (EDA) com Pandas Profiling
from ydata_profiling import ProfileReport

df = pd.read_csv('precos-glp-02_2025.csv', sep=";", encoding="utf-8", skipinitialspace=True, decimal=",", engine='python')
profile = ProfileReport(df, title="Análise das vendas de GLP no Brasil em FEV-25")
profile.to_file("output.html")
#Leitura e Inspeção Inicial dos Dados
import pandas as pd 

#Análise Exploratória de Dados (EDA) com Pandas Profiling
from ydata_profiling import ProfileReport

df = pd.read_csv('precos-glp-02_2025_edit.csv', sep=";", encoding="utf-8", skipinitialspace=True, decimal=",", engine='python')
profile = ProfileReport(df, title="Profiling Report")
profile.to_file("output.html")
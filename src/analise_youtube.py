import pandas as pd
import numpy as np

# 1. Carregar o dataset global
df = pd.read_csv('../data/raw/global_top4k.csv')

# 2. Filtrar apenas o Brasil (código 'BR')
df_brasil = df[df['Country'] == 'BR'].copy()

# 3. Limpeza de Dados
# Remover duplicatas pelo ID do canal para garantir integridade
df_brasil = df_brasil.drop_duplicates(subset=['Channel ID'])

# Tratar valores nulos na descrição
df_brasil['Description'] = df_brasil['Description'].fillna('Sem descrição disponível')

# Garantir que métricas sejam numéricas e remover dados zerados
df_brasil = df_brasil[df_brasil['Subscribers'] > 0]

# 4. Engenharia de Recursos
# Criar métrica de eficiência tratando divisão por zero
df_brasil['Views_por_Inscrito'] = np.where(
    df_brasil['Subscribers'] > 0, 
    df_brasil['Total Views'] / df_brasil['Subscribers'], 
    0
)

# Usar NumPy para classificar o Porte do Canal
conditions = [
    (df_brasil['Subscribers'] < 1000000),
    (df_brasil['Subscribers'] >= 1000000) & (df_brasil['Subscribers'] < 10000000),
    (df_brasil['Subscribers'] >= 10000000)
]
choices = ['Pequeno', 'Médio', 'Gigante']
df_brasil['Porte_do_Canal'] = np.select(conditions, choices, default='Outro')

# 5. Verificação Final e Exportação
print("Primeiras linhas da métrica calculada:")
print(df_brasil[['Channel Name', 'Views_por_Inscrito']].head())

# Salvar o dataset final "Gold" com ponto para decimal
df_brasil.to_csv('../data/processed/top_youtube_brasil_limpo.csv', index=False, sep=',', decimal='.')
print("\nArquivo 'top_youtube_brasil_limpo.csv' gerado com sucesso!")


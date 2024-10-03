import pandas as pd
import numpy as np
from auxiliar.conexoes import obter_dados

ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

try:
    print('Obtendo dados de ocorrências...')

    # parâmetros da função: (endereco_arquivo, nome_arquivo, tipo_arquivo, separador)
    df_ocorrencias = obter_dados(ENDERECO_DADOS, '', 'csv', ';')

    #print(df_ocorrencias.head()) #padrão são as 5 primeiras linhas

    print('Dados obtidos com sucesso!')
except Exception as e:
    print('Erro ao obter dados: ',e)
    exit()


# delimitar somente as variaveis solicitadas: mes-ano e estelionato
try:
    print('Iniciando a delimitação das variáveis...')
    #print(df_ocorrencias.columns) # Exibir as colunas do dataframe

    df_estelionato = df_ocorrencias[['mes_ano','estelionato']]
    #print(df_estelionato.head())

    # Agrupar mes-ano
    df_data_estelionato = df_estelionato.groupby('mes_ano').sum('estelionato').reset_index()
    #print(df_data_estelionato)

    print('Delimitação concluída!')
except Exception as e:
    print('Erro ao delimitar o dataframe: ', e)
    exit()



# Estudar o dado:
# importar numpy
# Obter os Quartis Identificar os meses e anos com menos(Q1-->25%) e aqueles com mais(Q3-->75%) estelionatos
try: 
    print('Obtendo maiores e menores quantidades de estelionatos...')

    #converter a variavel estelionato para array 
    array_estelionato = df_data_estelionato['estelionato'].to_numpy()

    # Calcular os quartis
    # Também chamadas de Medidas de posição (medidas de dispersão OU variabilidade)
    q1 = np.quantile(array_estelionato, 0.25, method='weibull')
    q2 = np.quantile(array_estelionato, 0.50, method='weibull')
    #mediana = np.median(array_roubo_veiculo) --> outra forma de fazer o Q2
    q3 = np.quantile(array_estelionato, 0.75, method='weibull')

    print('Quartis: ')
    print(20*'-')
    print('Q1: ',q1)
    print('Q3: ',q3)

    # Obter os meses e anos com MAIS estelionatos
    # Filtrando uma coluna dentro do dataframe e maior que q3
    df_mais_estelionatos = df_data_estelionato[df_data_estelionato['estelionato']>q3]
    print('\nMeses e Anos com mais estelionatos:')
    print(20*'-')
    print(df_mais_estelionatos.sort_values(by='estelionato', ascending=False))

    # Obter os meses e anos com MENOS estelionatos
    # Filtrando uma coluna dentro do dataframe --> menor que q1
    df_menos_estelionatos = df_data_estelionato[df_data_estelionato['estelionato']<q1]
    print('\nMeses e Anos com menos estelionatos:')
    print(20*'-')
    print(df_menos_estelionatos.sort_values(by='estelionato')) #padrão é crescente (ascending=true)

except Exception as e: 
    print('Erro ao obter quantidades de estelionatos: ',e)
    exit()
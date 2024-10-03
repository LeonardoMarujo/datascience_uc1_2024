import pandas as pd
import numpy as np
from auxiliar.conexoes import obter_dados

# Constante do endereço dos dados
ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

try:
    print('Obtendo dados de ocorrências...')

    # parâmetros da função: endereco_arquivo, nome_arquivo, tipo_arquivo, separador
    df_ocorrencias = obter_dados(ENDERECO_DADOS, '', 'csv', ';')

    #print(df_ocorrencias.head())

    print('Dados obtidos com sucesso!')
except Exception as e:
    print('Erro ao obter dados: ',e)
    exit()



# Delimitar as variaveis solicitadas
try:
    print('Iniciando a delimitação e totalização das variáveis...')
    #print(df_ocorrencias.columns) # Exibir as colunas do dataframe

    df_recup_veiculos = df_ocorrencias[['cisp','recuperacao_veiculos']]
    #print(df_recup_veiculos)

    df_total_recup_veiculos = df_recup_veiculos.groupby('cisp').sum('recuperacao_veiculos').reset_index()
    #print(df_total_recup_veiculos)
    print('Delimitação e totalização concluída!')
except Exception as e:
    print('Erro ao delimitar o dataframe: ', e)
    exit()



# Aprofundamento
# Calcular média e mediana --> ver a simetria ou assimetria --> 25% de proximidade pra mais e pra menos
# Calcular a Amplitude (maior valor - menor valor)
# Calcular IQR = Q3 - Q1
# Calcular Limite superior e limite Inferior
try:
    print('\nCalculando métricas...')
    array_recup_veiculos = df_total_recup_veiculos['recuperacao_veiculos'].to_numpy()

    media = np.mean(array_recup_veiculos)
    mediana = np.median(array_recup_veiculos)
    print('\nMedidas de tendencia central: ')
    print(30*'-')
    print('Média: ', media)
    print('Mediana: ', mediana)
    # Nota-se uma assimetria ao analisar os dados; Média > Mediana

    # Medidas de Dispersão
    print('\nMedidas de Dispersão:')
    print(30*'-')

    minimo = np.min(array_recup_veiculos)
    maximo = np.max(array_recup_veiculos)
    amplitude = maximo - minimo
    print('Mínimo:',minimo)
    print('Máximo:',maximo)
    print('Amplitude:', amplitude)

    # Obtendo os Quartis
    q1 = np.quantile(array_recup_veiculos,0.25, method='weibull')
    q2 = np.quantile(array_recup_veiculos,0.50, method='weibull')
    q3 = np.quantile(array_recup_veiculos,0.75, method='weibull')

    # IQR
    iqr = q3 - q1

    # Limites
    limite_inferior = q1-(1.5*iqr)
    limite_superior = q3+(1.5*iqr)

    # Medidas de posição
    print('\nMedidas de Posição: ')
    print(30*'-')
    print('IQR:', iqr)
    print('Limite Inferior:',limite_inferior)
    print('Q1: ',q1)
    print('Q2: ',q2)
    print('Q3: ',q3)
    print('Limite Superior:',limite_superior)

    # Exibindo as DPs Outliers (2 Pergunta da Questão)
    df_dps_outliers_max = df_total_recup_veiculos[df_total_recup_veiculos['recuperacao_veiculos']>limite_superior]
    print('\nOutliers max: ')
    print(30*'-')
    print(df_dps_outliers_max.sort_values(by='recuperacao_veiculos', ascending=False))

    # Exibindo DPs com menos recuperações(<q1) (3 Pergunta da Questão)
    df_dps_q1 = df_total_recup_veiculos[df_total_recup_veiculos['recuperacao_veiculos']< q1]
    print('\nDPs que menos recuperam: ')
    print(30*'-')
    print(df_dps_q1.sort_values(by='recuperacao_veiculos'))

except Exception as e:
    print('Erro ao calcular métricas', e)














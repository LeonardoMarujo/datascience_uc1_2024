import pandas as pd
import numpy as np
from auxiliar.conexoes import obter_dados


# Constante do endereço dos dados
ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

# Obter dados
# Comma Separete Values (CSV); É preciso verificar se está separado por virgula ou não
# Erro de decodificação
# UTF-8 (padrão de codificação no Brasil)
# Avisar que o separador é ;
# Ainda vai dar erro
# Mudar para iso-8859-1
# Editar a função que ja foi criada para poder ler csv
# Chama a função para obter os dados
try:
    print('Obtendo dados de ocorrências...')

    # parâmetros da função: endereco_arquivo, nome_arquivo, tipo_arquivo, separador
    df_ocorrencias = obter_dados(ENDERECO_DADOS, '', 'csv', ';')

    #print(df_ocorrencias.head()) #padrão são as 5 primeiras linhas

    print('Dados obtidos com sucesso!')
except Exception as e:
    print('Erro ao obter dados: ',e)
    exit()


# delimitar somente as variaveis solicitadas e totalizar: cidade e roubo de veiculos
try:
    print('Iniciando a delimitação e totalização das variáveis...')
    #print(df_ocorrencias.columns) # Exibir as colunas do dataframe
    df_roubo_veiculo = df_ocorrencias[['munic','roubo_veiculo']]
    #print(df_roubo_veiculo.head())

    # Totalizar o dataframe
    df_total_roubo_veiculo = df_roubo_veiculo.groupby('munic').sum('roubo_veiculo').reset_index()

    #print(df_total_roubo_veiculo)

    print('Delimitação e totalização concluída!')
except Exception as e:
    print('Erro ao delimitar o dataframe: ', e)
    exit()



# ARRAY: É uma estrutura de dados que potencializa(+Velocidade) os cálculos matemáticos e estatísticos; Muito utilizado para grandes volumes de dados;
# Instalar e importar a biblioteca NumPy (Numerical Python) --> Métodos matemáticos e estatísticos
# pip install numpy \ pip show numpy
# importar a biblioteca

# Obter os Quartis Identificar os municipios com menos(Q1-->25%) e aqueles com mais(Q3-->75%) roubos de veiculos
try:
    print('Obtendo maiores e menores municipios...')

    #converter a variavel roubo_veiculo para array 
    array_roubo_veiculo = df_total_roubo_veiculo['roubo_veiculo'].to_numpy()

    # Q1 - 25%
    # method='weibull' --> METODO CLASSICO
    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull')

    # Q2 - 50%
    # method='weibull' --> METODO CLASSICO
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull')
    #mediana = np.median(array_roubo_veiculo) --> outra forma de fazer o Q2

    # Q3 - 75%
    # method='weibull' --> METODO CLASSICO
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull')

    print('Q1: ',q1)
    print('Q2: ',q2)
    print('Q3: ',q3)


    # Obter os municipios com MAIS roubos de veiculos
    # Filtrando uma coluna dentro do dataframe e maior que q3
    df_munics_acima_q3 = df_total_roubo_veiculo[df_total_roubo_veiculo['roubo_veiculo']>q3]
    print('\nMunicipios com mais roubos de veiculos:')
    print(20*'-')
    print(df_munics_acima_q3.sort_values(by='roubo_veiculo', ascending=False))


    # Obter os municipios com MENOS roubos de veiculos
    # Filtrando uma coluna dentro do dataframe e menor que q1
    df_munics_abaixo_q1 = df_total_roubo_veiculo[df_total_roubo_veiculo['roubo_veiculo']<q1]
    print('\nMunicipios com menos roubos de veiculos:')
    print(20*'-')
    print(df_munics_abaixo_q1.sort_values(by='roubo_veiculo'))

except Exception as e: 
    print('Erro ao obter maiores e menores municipios: ',e)
    exit()
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
    df_munics_mais_roubos = df_total_roubo_veiculo[df_total_roubo_veiculo['roubo_veiculo']>q3]
    print('\nMunicipios com mais roubos de veiculos:')
    print(20*'-')
    print(df_munics_mais_roubos.sort_values(by='roubo_veiculo', ascending=False))

    # Obter os municipios com MENOS roubos de veiculos
    # Filtrando uma coluna dentro do dataframe e menor que q1
    df_munics_menos_roubos = df_total_roubo_veiculo[df_total_roubo_veiculo['roubo_veiculo']<q1]
    print('\nMunicipios com menos roubos de veiculos:')
    print(20*'-')
    print(df_munics_menos_roubos.sort_values(by='roubo_veiculo'))

except Exception as e: 
    print('Erro ao obter maiores e menores municipios: ',e)
    exit()




# EXEMPLO 02: APROFUNDAMENTO DOS DADOS
# Indentificar a simetria ou assimetria do conjnto de dados:
    
    # Simetria: Calcula-se a MÉDIA e a MEDIANA  
    # Média pode ser usada para resumir os dados
        # Se forem Iguais ou próximas, tendem a ser simétricos --> distribuição dos dados semelhantes --> tendem a não ter outlier
    
    # Assimetria: Calcula-se a MÉDIA e a MEDIANA 
    # Média NÃO é uma boa medida para resumir os dados, nesse caso, a Mediana é melhor
        # Se forem diferentes ou distantes, tendem a ser assimétrica
    
try:
    print('\nCalculando outliers...')

    media = np.mean(array_roubo_veiculo)

    mediana = np.median(array_roubo_veiculo)

    print('Medidas de tendência central: ')
    print(30*'-')
    print('Média', media)
    print('Mediana',mediana)

    # Olhar a amplitude (maior valor - menor valor)
    # MAIOR AMPLITUDE --> MAIOR DISPERSÃO dos dados, maior a VARIEDADE 

    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

    print('Máximo: ', maximo)
    print('Mínimo: ', minimo)
    print('Amplitude: ',amplitude)


    # Identificando Outliers
    # Trabalhar com o INTERQUARTIL (IQR) = Q3 - Q1 ; Identificar a dispersão entre os quartis ; MAIOR IQR, MAIS DISPERSO
        # Usado como base de cálculo para identificar os LIMITES (SUPERIOR E INFERIOR) dos OUTLIERS
    iqr = q3 - q1
    print('IQR: ', iqr)

    # Calculando LIMITE SUPERIOR DO OUTLIER --> separa os dados MAIORES (considerados "normais") dos discrepantes dos Outliers
    # Calculo Padrão do LIMITE SUPERIOR DO OUTLIER:
    limite_superior = q3 + (1.5*iqr)
    # Calculando LIMITE INFERIOR DO OUTLIER --> separa os dados MENORES (considerados "normais") dos discrepantes dos Outliers
    # Calculo Padrão do LIMITE INFEIOR DO OUTLIER:
    limite_inferior = q1 - (1.5*iqr)
    # Fora desse intervalo entre os limites superior e inferior são considerados outliers
    print('limite_superior: ',limite_superior)
    print('limite_inferior: ',limite_inferior)


    # Identificar os municipios outliers superiores
    df_munic_outliers_max = df_total_roubo_veiculo[df_total_roubo_veiculo['roubo_veiculo']>limite_superior]
    print('\nOutliers max: ')
    print(30*'-')
    if len(df_munic_outliers_max)>0:
        print(df_munic_outliers_max.sort_values(by='roubo_veiculo', ascending=False))
    else:
        print('Não existem municipios outliers para cima!')

    # Identificar os municipios outliers inferiores
    df_munic_outliers_min = df_total_roubo_veiculo[df_total_roubo_veiculo['roubo_veiculo']<limite_inferior]
    print('\nOutliers min: ')
    print(30*'-')
    if len(df_munic_outliers_min)>0:
        print(df_munic_outliers_min.sort_values(by='roubo_veiculo'))
    else:
        print('Não existem municipios outliers para baixo!')

except Exception as e:
    print('Erro ao calcular outliers!',e)
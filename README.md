# CryptoBot

## Requistos:
Instalar o pacote Price-Indices no ambiente do python (pasta de Libs)
Comandos:
- git clone https://github.com/dc-aichara/Price-Indices.git
- cd Price-Indices
- python setup.py install

## Como Executar:
1. Editar a configuraçoes
        COIN = "bitcoin"
        TESTING_YEARS = 2021  ## Testing sample. Remember to edit the BTC price for USD 1000 during first date of the year
        BEAR_TREND_LIMIT = 0  ## Porcentage of EMA140 offset
        TIMING = 3            ## Seconds delay for visualization purposes
    
    Some COIN samples used are:
	- bitcoin
    - ethereum
    - cardano
    - chainlink
    - binance-coin
    - polkadot
    - aave
    - pancakeswap
    - solana
    - polygon
    - chiliz
2. Rodar o arquivo controller usando o comando >>Python Controller.py
3. Comparar o lucro de Buy and HOLD com o lucro utilizando o robô

## Objetivo: 
Robô de investimentos de longo prazo no mercado de ativos digitais

## População-alvo: 
Ativos com maior histórico e Capitalização do mercado preferivelmente Bitcoin por ser o ativo principal e unico pareado com dollar

## Amostra: 
Coleta dos dados históricos diários (data, preço mais baixo, preço mais alto, preço de abertura, preço de fechamento, volume de transações) do ativo usando a API da CoinMarcketCap

## Técnicas de coleta de dados: 
Interfase de Programação de Aplicação: Chamadas em tempo real.
Amostra de treinamento: todo o historico desde 2013-04-28 ate a data de ontem
Amostra de teste: Um ano escolhido no arquivo Config.py TESTING_YEARS. e.g. 2021

## Técnicas de análise dos dados: 
Series Temporais com análise de das medias moveis exponenciais
Estrategia de curto prazo: Cruzamento de EMA9 vs EMA21
Estrategia de longo prazo: Distancia porcentual ate o suporte de EMA200

"The EMA is a moving average that places a greater weight and significance on the most recent data points.
Like all moving averages, this technical indicator is used to produce buy and sell signals based on crossovers and divergences from the historical average"
Traders often use several different EMA lengths, such as 10-day, 50-day, and 200-day moving averages.". https://www.investopedia.com/terms/e/ema.asp

## Desenho de pesquisa ou etapas a serem desenvolvidas:
1.	Descritiva e diagnostica (Colab: https://colab.research.google.com/drive/1scO6BFpCjc4moNkKmgT-3lqlNF85P579#scrollTo=raRu3jeVifVq)
	- Solicitação para autenticação da API numa aplicação de twitter em modo de leitura
	- Análise de sentimentos utilizando a API do Twitter tweepy 
	- Processamento simplificado de texto ou NLP utilizando textblob
2.	Preditiva
	- Captura dos dados usando a API coinbase para o ativo BTC (bitcoin)
	- Escolha e ajuste do modelo de series temporais
3.	Prescritiva
	- Análise de medias moveis exponenciais comparando a media de 9 com a media de 21 e achando os cruzamentos
    Similar à tecnica usada em açoes: https://www.youtube.com/watch?v=rrVgT6Q8CMM&ab_channel=DiogoMuryDiogoMury 
    Baseado na tecnica de Criptomoedas: https://www.youtube.com/watch?v=VpUEtF4NuZw&ab_channel=EdwardOrnelas
	- Análise de medo e ambição utilizando a API de Fear And Greed
	- Decidir momento de compra ou de venda

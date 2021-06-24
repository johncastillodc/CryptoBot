# CryptoBot

Objetivo: Robô de investimentos de longo prazo no mercado de ativos digitais

-Delineamento da pesquisa: Usar o histórico de vendas para construir o modelo.
-População-alvo: Ativos com maior histórico e Capitalização do mercado
-Amostra: Coleta dos dados históricos diários (data, preço mais baixo, preço mais alto, preço de abertura, preço de fechamento, volume de transações) do ativo usando a API da corretora Coinbase 
-Técnicas de coleta de dados: Interfase de Programação de Aplicação:  Coinbase API
-Técnicas de análise dos dados: DeepLearning usando Tensorflow API de Redes Neuronais artificiais para python: Keras
-Desenho de pesquisa ou etapas a serem desenvolvidas:
1.	Descritiva e diagnostica
•	Solicitação para autenticação da API numa aplicação de twitter em modo de leitura
•	Análise de sentimentos utilizando a API do Twitter tweepy 
•	Processamento simplificado de texto ou NLP utilizando textblob
2.	Preditiva
•	Captura dos dados usando a API coinbase para os ativos BTC (bitcoin), ETH (altcoin) e USDT (stable coin)
•	Escolha e ajuste do modelo de aprendizado com redes neuronais
3.	Prescritiva
1.	Análise de medias moveis exponenciais comparando a media de 9 com a media de 21 e achando os cruzamentos
https://www.youtube.com/watch?v=rrVgT6Q8CMM&ab_channel=DiogoMuryDiogoMury 
2.	Análise de medo e ambição utilizando a API de Fear And Greed
3.	Decidir momento de compra ou de venda

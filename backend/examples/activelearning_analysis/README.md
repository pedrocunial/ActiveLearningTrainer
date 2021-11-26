# Análise de desempenho do Active Learning

Para as análises de desempenho, foi utilizado o subset do Porco a partir do dataset da Pinacoteca disponibilizado pela IBM para esse projeto. Esse subset é o arquivo `porco.csv`.

## Utilização

Crie um arquivo chamado `credentials_nlc.txt` com a *Api Key* e *Url* de uma instância do NLC.

Exemplo:
```
8AlN9J8oEQ1_1YXaWsdfPEGVP9LSPDGVcIxpGeF5wSrr
https://gateway.watsonplatform.net/natural-language-classifier/api
```

Com essas credenciais, execute os scripts `test_al.py` e `test_random.py`. Eles fazem o processo de treinamento de classificadores para diferentes entradas, o primeiro utilizando Active Learning, e o seguindo de modo tradicional, com amostras aleatórias.

Os resultados dos testes são salvos respectivamente nos arquivos `results_al.txt` e `results_random.txt`.

Para visualizar os resultados, apenas execute o script `plot_results.py`, ele lê os arquivos de resultado e plota a análise de desempenho.
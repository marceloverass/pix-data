import requests
import pandas as pd
import json
import os

ano = input("Ano (ex: 2026): ")
mes = input("Mês (ex: 01): ")

competencia = f"{ano}{mes}"
pasta_destino = r"D:\projeto-pix"
nome_arquivo = f'EstatisticasTransacoesPix{competencia}.json'
caminho_completo = os.path.join(pasta_destino, nome_arquivo)

if os.path.exists(caminho_completo):
    print("Carregando dados do cache local...")
    
    df = pd.read_json(caminho_completo)
    if 'value' in df.columns:
         df = pd.json_normalize(df['value'])

else:
    print(f'Buscando dados da API do Banco Central para {competencia}')

    url = f"https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/EstatisticasTransacoesPix(Database=@Database)?@Database='{competencia}'&$filter=AnoMes eq {competencia}&$top=10000&$format=json&$select=AnoMes,PAG_PFPJ,REC_PFPJ,PAG_REGIAO,REC_REGIAO,PAG_IDADE,REC_IDADE,FORMAINICIACAO,NATUREZA,FINALIDADE,VALOR,QUANTIDADE"
    
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()

        with open(caminho_completo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        df = pd.DataFrame(dados['value'])
    else:
        print(f'Erro na API: {response.status_code}')
        df = pd.DataFrame()

print(df.head())
   
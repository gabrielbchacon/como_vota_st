import json
import requests
import pandas as pd

class get_data:

    def __init__(self, deputado_id=None):
        self.deputado_id = deputado_id
        self.deputado_data = None
        self.deputado_nome = None
        self.deputado_partido = None
        self.deputado_uf = None

    def get_deputado_data_all(self):
        if self.deputado_id == None:
            url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome'
            json_url = requests.get(url)
            data = json.loads(json_url.text)
            self.deputado_data = data

    def get_deputado_data(self):
        deputados_arquivo = './data/deputado_None'
        dados_deputados = None
        with open(deputados_arquivo, 'r') as f:
            dados_deputados = json.load(f)
        dados_deputado = next(item for item in dados_deputados['dados'] if item["id"] == self.deputado_id)
        self.deputado_data = dados_deputado
        self.deputado_nome = dados_deputado['nome']
        self.deputado_partido = dados_deputado['siglaPartido']
        self.deputado_uf = dados_deputado['siglaUf']
        return dados_deputado


    def get_deputado_despesas_per_page(self, url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        return data['dados']

    def get_deputado_despesas_all(self, check_all_pages=True):
        idx = 1
        url = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{self.deputado_id}/despesas?ano=2019&ano=2020&ano=2021&ano=2022&pagina={idx}&itens=100&ordem=ASC&ordenarPor=ano'
        dados = self.get_deputado_despesas_per_page(url)
        

        while(check_all_pages):
            idx += 1
            nexturl = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{self.deputado_id}/despesas?ano=2019&ano=2020&ano=2021&ano=2022&pagina={idx}&itens=100&ordem=ASC&ordenarPor=ano'
            next_dados = self.get_deputado_despesas_per_page(nexturl)
            if next_dados:
                for despesa in next_dados:
                    dados.append(despesa)
            else:
                break

        return dados

    def get_despesa_total(self):
        self.get_deputado_data()
        despesas_arquivo = f'./data/despesas/despesas_{self.deputado_id}'
        despesas_deputado = None
        with open(despesas_arquivo, 'r') as f:
            despesas_deputado = json.load(f)
        despesas_totais = 0
        if despesas_deputado:
            despesas_deputado_df = pd.DataFrame(despesas_deputado)
            despesas_totais = despesas_deputado_df['valorLiquido'].sum()
        return self.deputado_id, self.deputado_nome, self.deputado_partido, self.deputado_uf, despesas_totais

    def dump_deputados_base(self):
        path_ = './data/'
        filename = f'deputado_{self.deputado_id}'
        with open(path_ + filename, 'w') as f:
            json.dump(self.deputado_data, f, indent=4)
        
        print('file dumped to', filename)
    
    def dump_deputados_despesas(self):
        path_despesas = './data/despesas/'
        filename = f'despesas_{self.deputado_id}'
        with open(path_despesas + filename, 'w') as f:
            json.dump(self.get_deputado_despesas_all(), f, indent=4)
        
        print('file dumped to', filename)

    
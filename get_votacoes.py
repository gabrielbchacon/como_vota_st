import json
import requests
import pandas as pd
from tqdm import tqdm
import datetime

class get_votacoes:

    def __init__(self, votacao_id=None):
        self.votacao_id = votacao_id
        self.ano_legistatura_atual = [2019, 2020, 2021, 2022]
        self.votacao_data = None

# %%

    def get_votacoes_por_mes(self, mes, ano):
        if self.votacao_id == None:
            first_day = 1
            mounths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1]
            next_mounth = mounths.index(mes) + 1
            if mes != 12:
                last_day = datetime.date(ano, mounths[next_mounth], 1) - datetime.timedelta(days=1)
            else:
                last_day = datetime.date(ano+1, mounths[next_mounth], 1) - datetime.timedelta(days=1)
            mes = '{:>02d}'.format(mes)
            first_day = '{:>02d}'.format(first_day)
            url = f'https://dadosabertos.camara.leg.br/api/v2/votacoes?dataInicio={ano}-{mes}-{first_day}&dataFim={ano}-{mes}-{last_day.day}&ordem=DESC&ordenarPor=dataHoraRegistro'
            json_url = requests.get(url)
            data = json.loads(json_url.text)
            votacoes_todas = []
            page = 1
            print(url)
            last_page = data['links'][-1]['href'][-11]

            for page in tqdm(range(page, int(last_page)+1)):
                url = f'https://dadosabertos.camara.leg.br/api/v2/votacoes?ordem=DESC&ordenarPor=dataHoraRegistro&pagina={page}&itens=200'
                json_url_next = requests.get(url)
                data_next = json.loads(json_url_next.text)
                page += 1
                for votacao in tqdm(data_next['dados']):
                    votacoes_todas.append(votacao)
            
            self.votacao_data = votacoes_todas
        return self.votacao_data

    def votacoes_all(self):
        for ano in self.ano_legistatura_atual:
            #Não há votação em Janeiro por conta do recesso
            for mes in range(2, 13):
                self.get_votacoes_por_mes(mes, ano)
    
    def dump_votacoes(self):
        path_dump_votacoes = './data/votacoes/'
        filename = f'votacoes_todas'
        with open(path_dump_votacoes + filename, 'w') as f:
            json.dump(self.votacao_data, f, indent=4)
# %%

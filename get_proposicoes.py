import json
import requests
import pandas as pd
from tqdm import tqdm
import datetime
from datetime import date

class get_proposicoes:

    def __init__(self, proposicoes_id=None):
        self.proposicoes_id = proposicoes_id
        self.ano_legistatura_atual = [2019, 2020, 2021, 2022]
        self.proposicoes_data = []

    def get_proposicoes_all(self):
        if self.proposicoes_id == None:
            
            mes_atual = date.today().month
            ano_atual = date.today().year
            dia_atual = date.today().day -1
            first_day = 1
            first_year = self.ano_legistatura_atual[0]
            first_month = '01'
            mes_atual = '{:>02d}'.format(mes_atual)
            first_day = '{:>02d}'.format(first_day)
            url = f'https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio={first_year}-{first_month}-{first_day}&dataFim={ano_atual}-{mes_atual}-{dia_atual}&itens=100&ordem=ASC&ordenarPor=id'
            json_url = requests.get(url)
            data = json.loads(json_url.text)
            proposicoes_todas = []
            page = 1
            print(url)
            if data['dados']:
                last_page_url = data['links'][-1]['href']
                start = last_page_url.find('pagina=') + 7
                end = last_page_url.find('&itens=')
                last_page = last_page_url[start: end]


                for page in tqdm(range(page, int(last_page)+1)):
                    url = f'https://dadosabertos.camara.leg.br/api/v2/proposicoes?dataInicio={first_year}-{first_month}-{first_day}&dataFim={ano_atual}-{mes_atual}-{dia_atual}&itens=100&ordem=ASC&ordenarPor=id&pagina={page}'
                    json_url_next = requests.get(url)
                    data_next = json.loads(json_url_next.text)
                    page += 1
                    for proposicao in data_next['dados']:
                        proposicoes_todas.append(proposicao)
                        print(proposicao['id'])
                
                self.proposicoes_data.append(proposicoes_todas)
                
        return self.proposicoes_data



    def dump_proposicoes(self):
        path_dump_proposicoes = './data/proposicoes/'
        filename = f'proposicoes_todas'
        with open(path_dump_proposicoes + filename, 'w') as f:
            json.dump(self.proposicoes_data, f, indent=4)

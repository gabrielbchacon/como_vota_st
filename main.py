from get_data import get_data
from get_votacoes import get_votacoes
import json
import pandas as pd
from tqdm import tqdm


votacoes = get_votacoes()
votacoes.votacoes_all()
votacoes.dump_votacoes()

#Data Load and preparation
'''file = './data/deputado_None'
data = None
with open(file, 'r') as f:
    data = json.load(f)'''

'''df = pd.DataFrame(data['dados'])
ids = df['id'].tolist()

despesas_total_df = []
for deputado_id in tqdm(ids):
    data_got = get_data(deputado_id)
    id, nome,  partido, deputado_uf, total_despesas = data_got.get_despesa_total()
    despesas_total_df.append({'id': id, 'nome': nome, 'partido': partido, 'UF': deputado_uf, 'total_despesas': total_despesas})


path_despesas = './data/despesas/'
filename = 'despesas_totais'
with open(path_despesas + filename, 'w') as f:
    json.dump(despesas_total_df, f, indent=4)
'''

'''for deputado_id in tqdm(ids):
    data_got = get_data(deputado_id)
    data_got.dump_deputados_despesas()'''


